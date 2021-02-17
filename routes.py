from app import app
from flask import redirect, render_template, request, session, make_response, abort, flash
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

@app.route("/")
def index():
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM " \
          "cars c, ads a WHERE c.id=a.car_id " \
          "AND a.visible=True"
    result = db.session.execute(sql)
    cars = result.fetchall()

    #TODO: REMOVE IF UNNECESSARY
    #sql = "SELECT id FROM ads WHERE user_id=:id AND visible=:visible"
    #result = db.session.execute(sql, {"id":user_id(), "visible":True})
    #owner_id = result.fetchone()
    #, owner=owner_id

    db.session.commit()
    return render_template("index.html", cars=cars)

@app.route("/login_user", methods=["POST"])
def login_as_user():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return render_template("error.html", error="Tarkista käyttäjätunnus ja salasana!")
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            return redirect("/")
        else:
            return render_template("error.html", error="Tarkista käyttäjätunnus ja salasana!")


@app.route("/login")
def login():
    return render_template("login.html")

def user_id():
    return session.get("user_id", 0)

def logged_user():
    return session.get("username",0)

def get_all_car_equipment():
    sql = "SELECT * FROM equipment"
    result = db.session.execute(sql)
    equipment = result.fetchall()
    return equipment

def get_car_equipment_by_id(id):
    sql = "SELECT e.name FROM equipment e, car_equipment ce WHERE ce.car_id=:id AND e.id=ce.equipment_id"
    result = db.session.execute(sql, {"id":id})
    equipment = result.fetchall()
    return equipment

def get_equipment_id_by_name(name):
    sql = "SELECT id FROM equipment WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    name = result.fetchone()[0]
    db.session.commit()
    return name

def get_user_info_by_id(id):
    sql = "SELECT firstname, surname, telephone, email, location FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    info = result.fetchall()
    return info

@app.route("/new")
def new_car_form():

    # TODO: REMOVE IF UNNECESSARY
    #sql = "SELECT * FROM equipment"
    #result = db.session.execute(sql)
    #equipment = result.fetchall()
    return render_template("car_form.html", equipment=get_all_car_equipment())

@app.route("/send", methods=["POST"])
def send():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    brand = request.form["brand"]
    if len(brand.strip()) < 1:
        return render_template("error.html", error="Merkki ei voi olla tyhjä!")
    model = request.form["model"]
    if len(model.strip()) < 1:
        return render_template("error.html", error="Malli ei voi olla tyhjä!")
    chassis = request.form["chassis"]
    fuel = request.form["fuel"]
    drive = request.form["drive"]
    transmission = request.form["transmission"]
    mileage = request.form["mileage"]
    print(mileage)
    if int(mileage) < 1 or int(mileage) > 10000000:
        return render_template("error.html", error="Mittarilukema ei ole sallitulla välillä!")
    year = request.form["year"]
    if int(year) < 1900 or int(year) > 2021:
        return render_template("error.html", error="Vuosi ei ole sallitulla välillä!")
    price = request.form["price"]
    if int(price) < 1 or int(price) > 10000000:
        return render_template("error.html", error="Hinta ei ole sallitulla välillä!")
    color = request.form["color"]
    if len(color.strip()) < 1:
        return render_template("error.html", error="Väri ei voi olla tyhjä!")
    engine = request.form["engine"]
    if int(engine) < 100 or int(engine) > 10000:
        return render_template("error.html", error="Moottorin tilavuus ei ole sallitulla välillä!")
    power = request.form["power"]
    if int(power) < 0 or int(power) > 2000:
        return render_template("error.html", error="Moottorin teho ei ole sallitulla välillä!")
    legal = request.form["legal"]

    #Equipment as list
    equipment_list = request.form.getlist("eq")

    # Custom dictionary for each car and its equipment
    eq = get_all_car_equipment()
    eq_dict = {}
    for i in range(0, len(equipment_list)):
        eq_dict[i] = equipment_list[i]

    #Car data
    sql = "INSERT INTO cars (brand, model, chassis, fuel, drive, transmission, mileage, year, price, " \
          "color, engine, power, street_legal) VALUES " \
          "(:brand, :model, :chassis, :fuel, :drive, :transmission, :mileage, :year, :price, :color, " \
          ":engine, :power, :street_legal) RETURNING id"
    result = db.session.execute(sql, {"brand":brand.strip(), "model":model.strip(), "chassis":chassis,
                                      "fuel":fuel, "drive":drive, "transmission":transmission,
                                      "mileage":mileage, "year":year, "price":price, "color":color.strip(),
                                      "engine":engine, "power":power, "street_legal":legal})
    car_id = result.fetchone()[0]
    db.session.commit()

    #Ad data
    info = request.form["info"]
    if len(info) > 5000:
        return render_template("error.html", error="Teksti on liian pitkä")
    sql = "INSERT INTO ads (info, created, visible, user_id, car_id) VALUES " \
          "(:info, NOW(), :visible, :user_id, :car_id) RETURNING id"
    result = db.session.execute(sql, {"info":info, "visible":True, "user_id":user_id(), "car_id":car_id})
    ad_id = result.fetchone()[0]
    db.session.commit()

    #Creating a reference between ad and car
    sql = "INSERT INTO car_ad (car_id, ad_id) VALUES (:car_id, :ad_id)"
    db.session.execute(sql, {"car_id":car_id, "ad_id":ad_id})
    db.session.commit()

    #Creating a reference between car_id and equipment_id
    sql = "INSERT INTO car_equipment (car_id, equipment_id) VALUES (:car_id, :equipment_id)"
    for name in eq_dict:
        eq = eq_dict[name]
        result = db.session.execute(sql, {"car_id":car_id, "equipment_id":get_equipment_id_by_name(eq)})
    db.session.commit()

    #Image file data
    file = request.files["file"]
    #print("name", file.filename)
    #print("length", len(file.read()),"bytes")
    name = file.filename
    if file and not name.endswith(".jpg"):
        return render_template("error.html", error="Väärä tiedostopääte")
    data = file.read()
    if len(data) > 100*1024:
        return render_template("error.html", error="Liian iso tiedosto")
    sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    result = db.session.execute(sql, {"name":name, "data":data})
    image_id = result.fetchone()[0]
    db.session.commit()

    #Creating a relation between the image and the ad
    sql = "INSERT INTO ad_images (image_id,ad_id) VALUES (:image_id,:ad_id)"
    db.session.execute(sql, {"image_id":image_id, "ad_id":ad_id})
    db.session.commit()

    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

def get_car_id_by_ad_id(id):
    sql = "SELECT car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result[0]

def get_all_car_info_by_id(id):
    sql = "SELECT * FROM cars WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    car_data = result.fetchall()
    return car_data

@app.route("/ad/<int:id>")
def ad_page(id):
    #Ad info
    sql = "SELECT id, info, created, user_id, car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ad_data = result.fetchall()

    #TODO: REMOVE IF UNNECESSARY
    #Car_id
    #sql = "SELECT car_id FROM ads WHERE id=:id"
    #result = db.session.execute(sql, {"id":id}).fetchone()
    #car_id = result[0]

    #Car info
    sql = "SELECT * FROM cars WHERE id=:id"
    result = db.session.execute(sql, {"id":get_car_id_by_ad_id(id)})
    car_data = result.fetchall()

    #Seller id
    sql = "SELECT user_id FROM ads a WHERE a.id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    seller_id = result[0]

    #Seller info
    sql = "SELECT u.firstname, u.surname, u.telephone, u.email, u.location FROM users u WHERE u.id=:id"
    result = db.session.execute(sql, {"id":seller_id})
    seller_data = result.fetchall()

    #Equipment info
    sql = "SELECT e.name FROM equipment e, car_equipment ce WHERE ce.car_id=:id AND ce.equipment_id=e.id"
    result = db.session.execute(sql, {"id": get_car_id_by_ad_id(id)})
    cars_equipment = result.fetchall()

    db.session.commit()
    return render_template("ad_info.html",
        specs=car_data, info=ad_data, seller=seller_data, logged=user_id(), id=seller_id,
        equipment=cars_equipment, admin=is_admin(user_id()))

def is_admin(id):
    sql = "SELECT admin FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    admin = result.fetchone()[0]
    print(admin)
    return admin

@app.route("/ad_image/<int:id>")
def show(id):
    sql = "SELECT data FROM images, ad_images WHERE ad_images.ad_id=:id"
    result = db.session.execute(sql, {"id":id})
    image = result.fetchone()[0]
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/register", methods=["GET","POST"])
def register():
    return render_template("user_form.html")

@app.route("/new_user", methods=["GET","POST"])
def create_new_user():
    if session["csfr_token"] != request.form["csrf_token"]:
        abort(403)
    username = request.form["username"]
    if len(username.strip()) < 1:
        return render_template("error.html", error="Nimi ei voi olla tyhjä merkkijono!")
    password = request.form["password"]
    if len(password.strip()) < 1:
        return render_template("error.html", error="Salasana ei voi olla tyhjä merkkijono!")
    first_name = request.form["fname"]
    if len(first_name.strip()) < 1:
        return render_template("error.html", error="Nimi ei saa olla tyhjä")
    last_name = request.form["sname"]
    if len(last_name.strip()) < 1:
        return render_template("error.html", error="Sukunimi ei voi olla tyhjä!")
    location = request.form["location"]
    phone = request.form["tel"]
    email = request.form["email"]
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, firstname, surname, telephone, email, location, admin, password) " \
              "VALUES (:username, :firstname, :surname, :telephone, :email, :location, :admin, :password)"
        db.session.execute(sql, {"username":username,"firstname":first_name,"surname":last_name,
                                 "telephone":phone.strip(),"email":email.strip(), "location":location.strip(), "admin":False, "password":hash_value})
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error.html", error="Tapahtui virhe!")

@app.route("/userinfo")
def show_user_data():
    #TODO: REMOVE IF UNNECESSARY
    # sql = "SELECT firstname, surname, telephone, email, location FROM users WHERE id=:id"
    # result = db.session.execute(sql, {"id":user_id()})
    # user_data = result.fetchall()
    return render_template("user_data.html", user=get_user_info_by_id(user_id()))

@app.route("/update_user_info", methods=["POST"])
def update_user_info():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    first_name = request.form["fname"]
    last_name = request.form["sname"]
    location = request.form["location"]
    phone = request.form["tel"]
    email = request.form["email"]
    sql = "UPDATE users SET firstname=:firstname, surname=:surname, telephone=:telephone, email=:email, " \
          "location=:location WHERE id=:id"
    db.session.execute(sql, {"id":user_id(), "firstname":first_name.strip(), "surname":last_name.strip(), "telephone":phone.strip(),
                             "email":email.strip(), "location":location.strip()})
    db.session.commit()
    return redirect("/")

@app.route("/remove_ad/<int:id>", methods=["POST"])
def remove_ad(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    sql = "UPDATE ads SET visible=False WHERE user_id=:logged AND ads.id=:id"
    db.session.execute(sql, {"logged":user_id(), "id":id})
    db.session.commit()
    return redirect("/")

@app.route("/update_car_info/<int:id>", methods=["POST"])
def edit_car_info(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    sql = "SELECT c.id, c.brand, c.model, c.chassis, c.fuel, c.drive, c.transmission, c.mileage, c.year, " \
          "c.price, c.color, c.engine, c.power, c.street_legal, a.info FROM cars c, ads a WHERE " \
          "c.id=:id AND a.user_id=:logged AND a.visible=:visible AND a.car_id=:id"
    result = db.session.execute(sql, {"id":id, "logged":user_id(), "visible":True, "car_id":id})
    ad_data = result.fetchall()

    # TODO: REMOVE IF UNNECESSARY
    #All equipment
    #sql = "SELECT * FROM equipment"
    #result = db.session.execute(sql)
    #all_equipment = result.fetchall()

    # TODO: REMOVE IF UNNECESSARY
    #Car spesific equipment
    #sql = "SELECT e.name FROM equipment e, car_equipment ce WHERE ce.car_id=:id AND e.id=ce.equipment_id"
    #result = db.session.execute(sql, {"id":id})
    #equipment = result.fetchall()

    db.session.commit()
    return render_template("car_data.html", data=ad_data, equipment=get_all_car_equipment(),
    car_spesific_equipment=get_car_equipment_by_id(id))

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    brand = request.form["brand"]
    if len(brand.strip()) < 1:
        return render_template("error.html", error="Merkki ei voi olla tyhjä!")
    model = request.form["model"]
    if len(model.strip()) < 1:
        return render_template("error.html", error="Malli ei voi olla tyhjä!")
    chassis = request.form["chassis"]
    fuel = request.form["fuel"]
    drive = request.form["drive"]
    transmission = request.form["transmission"]
    mileage = request.form["mileage"]
    year = request.form["year"]
    price = request.form["price"]
    color = request.form["color"]
    if len(color.strip()) < 1:
        return render_template("error.html", error="Väri ei voi olla tyhjä!")
    engine = request.form["engine"]
    power = request.form["power"]
    legal = request.form["legal"]
    info = request.form["info"]
    if len(info.strip()) > 5000:
        return render_template("error.html", error="Liikaa tekstiä tekstikentässä!")

    # checked equipment as list
    eq = request.form.getlist("varusteet")

    #car data
    sql = "UPDATE cars SET brand=:brand, model=:model, chassis=:chassis, fuel=:fuel, drive=:drive, " \
          "transmission=:transmission, mileage=:mileage, year=:year, price=:price, color=:color, " \
          "engine=:engine, power=:power, street_legal=:legal WHERE id=:id"
    db.session.execute(sql, {"brand":brand.strip(), "model":model.strip(), "chassis":chassis, "fuel":fuel, "drive":drive,
                             "transmission":transmission, "mileage":mileage, "year":year, "price":price,
                             "color":color.strip(), "engine":engine, "power":power, "legal":legal, "id":id})
    
    #ad data
    sql = "UPDATE ads SET info=:info WHERE ads.car_id=:id"
    db.session.execute(sql, {"info":info.strip(), "id":id})

    #Equipment data
    sql = "DELETE FROM car_equipment WHERE car_id=:id"
    db.session.execute(sql, {"id":id})
    for i in eq:
        sql = "INSERT INTO car_equipment (car_id, equipment_id) VALUES (:car_id, :equipment_id)"
        db.session.execute(sql, {"car_id":id, "equipment_id":get_equipment_id_by_name(i)})
    db.session.commit()

    return redirect("/")

@app.route("/search")
def result():
    query = request.args["query"]
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
          "a.info LIKE :query AND a.visible=:visible"
    result = db.session.execute(sql, {"query":'%'+query+'%', "visible":True})
    ads = result.fetchall()
    return render_template("index.html", cars=ads)

@app.route("/sort")
def sort():
    option = request.args["options"]
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
          "c.id=a.car_id AND a.visible=True"
    result = db.session.execute(sql)
    ads = result.fetchall()
    db.session.commit()
    if option == "year":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY year"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "year DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY year DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "brand":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY brand"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "brand DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY brand DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "mileage":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY mileage"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "mileage DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY mileage DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "price":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY price"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "price DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY price DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "created":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY created"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)
    if option == "created DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY created DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        return render_template("/index.html", cars=ads)    
    else:
        return render_template("/index.html", cars=ads)

@app.route("/own_ads")
def show_logged_users_ads():
    sql = "SELECT c.brand, c.model, c.mileage, c.year, c.price, a.id, a.info, a.created FROM cars c, ads a WHERE " \
          "a.user_id=:id AND c.id=a.car_id AND a.visible=:visible"
    result = db.session.execute(sql, {"id":user_id(), "visible":False})
    unactive_ads = result.fetchall()
    result = db.session.execute(sql, {"id":user_id(), "visible":True})
    active_ads = result.fetchall()
    return render_template("own_ads.html", unactive=unactive_ads, active=active_ads)