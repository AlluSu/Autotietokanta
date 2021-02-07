from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv, urandom
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

def create_session_token():
    return urandom(16).hex()

@app.route("/")
def index():
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year FROM cars c, ads a WHERE c.id=a.car_id AND a.visible=True"
    result = db.session.execute(sql)
    cars = result.fetchall()

    sql = "SELECT id FROM ads WHERE user_id=:id AND visible=:visible"
    result = db.session.execute(sql, {"id":user_id(), "visible":True})
    owner_id = result.fetchone()
    return render_template("index.html", cars=cars, owner=owner_id)

@app.route("/login_user", methods=["POST"])
def login_as_user():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return render_template("error.html", user=username)
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

def user_id():
    return session.get("user_id", 0)

def logged_user():
    return session.get("username",0)

@app.route("/new")
def new_car_form():
    sql = "SELECT name FROM equipment"
    result = db.session.execute(sql)
    equipment = result.fetchall()
    print(equipment)
    return render_template("car_form.html", equipment=equipment)

@app.route("/result", methods=["POST"])
def car_added():
    brand = request.form["brand"]
    model = request.form["model"]
    chassis = request.form["chassis"]
    fuel = request.form["fuel"]
    drive = request.form["drive"]
    transmission = request.form["transmission"]
    mileage = request.form["mileage"]
    year = request.form["year"]
    price = request.form["price"]
    color = request.form["color"]
    engine = request.form["engine"]
    power = request.form["power"]
    legal = request.form["legal"]
    info = request.form["info"]
    return render_template("result.html", brand=brand,
    model=model, chassis=chassis, fuel=fuel, drive=drive,
    transmission=transmission, mileage=mileage, year=year, price=price,
    color=color, engine=engine, power=power,
    legal=legal, info=info)

@app.route("/send", methods=["POST"])
def send():
    brand = request.form["brand"]
    model = request.form["model"]
    chassis = request.form["chassis"]
    fuel = request.form["fuel"]
    drive = request.form["drive"]
    transmission = request.form["transmission"]
    mileage = request.form["mileage"]
    year = request.form["year"]
    price = request.form["price"]
    color = request.form["color"]
    engine = request.form["engine"]
    power = request.form["power"]
    legal = request.form["legal"]

    #Car data
    sql = "INSERT INTO cars (brand, model, chassis, fuel, drive, transmission, mileage, year, price, color, engine, power, street_legal) VALUES (:brand, :model, :chassis, :fuel, :drive, :transmission, :mileage, :year, :price, :color, :engine, :power, :street_legal) RETURNING id"
    result = db.session.execute(sql, {"brand":brand, "model":model, "chassis":chassis,
    "fuel":fuel, "drive":drive, "transmission":transmission, "mileage":mileage,
    "year":year, "price":price, "color":color, "engine":engine, "power":power,
    "street_legal":legal})
    car_id = result.fetchone()[0]
    db.session.commit()

    #Ad data
    info = request.form["info"]
    sql = "INSERT INTO ads (info, created, visible, user_id, car_id) VALUES (:info, NOW(), :visible, :user_id, :car_id) RETURNING id"
    result = db.session.execute(sql, {"info":info, "visible":True, "user_id":user_id(), "car_id":car_id})
    ad_id = result.fetchone()[0]
    db.session.commit()

    #Creating a reference between ad and car
    sql = "INSERT INTO car_ad (car_id, ad_id) VALUES (:car_id, :ad_id)"
    db.session.execute(sql, {"car_id":car_id, "ad_id":ad_id})
    db.session.commit()

    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/ad/<int:id>")
def ad_page(id):
    #Ad info
    sql = "SELECT id, info, created, user_id, car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ad_data = result.fetchall()

    #Car_id
    sql = "SELECT car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    car_id = result[0]

    #Car info
    sql = "SELECT * FROM cars WHERE id=:id"
    result = db.session.execute(sql, {"id":car_id})
    car_data = result.fetchall()

    #Seller id
    sql = "SELECT user_id FROM ads a WHERE a.id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    seller_id = result[0]

    #Seller info
    sql = "SELECT u.firstname, u.surname, u.telephone, u.email, u.location FROM users u WHERE u.id=:id"
    result = db.session.execute(sql, {"id":seller_id})
    seller_data = result.fetchall()

    return render_template("ad_info.html", specs=car_data, info=ad_data, seller=seller_data, logged=user_id(), id=seller_id)

@app.route("/register", methods=["GET","POST"])
def register():
    return render_template("user_form.html")

@app.route("/new_user", methods=["GET","POST"])
def create_new_user():
    username = request.form["username"]
    password = request.form["password"]
    first_name = request.form["fname"]
    last_name = request.form["sname"]
    location = request.form["location"]
    phone = request.form["tel"]
    email = request.form["email"]
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, firstname, surname, telephone, email, location, admin, password) VALUES (:username, :firstname, :surname, :telephone, :email, :location, :admin, :password)"
        db.session.execute(sql, {"username":username,"firstname":first_name,"surname":last_name,"telephone":phone,"email":email, "location":location, "admin":False, "password":hash_value})
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error.html")

@app.route("/userinfo", methods=["GET", "POST"])
def show_user_data():
    sql = "SELECT firstname, surname, telephone, email, location FROM users WHERE id=:id"
    logged = user_id()
    result = db.session.execute(sql, {"id":logged})
    user_data = result.fetchall()
    print(user_data)
    return render_template("user_data.html", user=user_data)

@app.route("/update_user_info", methods=["POST"])
def update_user_info():
    first_name = request.form["fname"]
    last_name = request.form["sname"]
    location = request.form["location"]
    phone = request.form["tel"]
    email = request.form["email"]
    sql = "UPDATE users SET firstname=:firstname, surname=:surname, telephone=:telephone, email=:email, location=:location WHERE id=:id"
    db.session.execute(sql, {"id":user_id(), "firstname":first_name, "surname":last_name, "telephone":phone, "email":email, "location":location})
    db.session.commit()
    return redirect("/userinfo")

@app.route("/remove_ad/<int:id>", methods=["POST"])
def remove_ad(id):
    sql = "UPDATE ads SET visible=False WHERE user_id=:logged AND ads.id=:id"
    #print(user_id())
    db.session.execute(sql, {"logged":user_id(), "id":id})
    db.session.commit()
    return redirect("/")

@app.route("/update_car_info/<int:id>", methods=["GET","POST"])
def edit_car_info(id):
    sql = "SELECT c.id, c.brand, c.model, c.chassis, c.fuel, c.drive, c.transmission, c.mileage, c.year, c.price, c.color, c.engine, c.power, c.street_legal, a.info FROM cars c, ads a WHERE c.id=:id AND a.user_id=:logged AND a.visible=:visible"
    result = db.session.execute(sql, {"id":id, "logged":user_id(), "visible":True})
    ad_data = result.fetchall()
    print(ad_data)
    db.session.commit()
    return render_template("car_data.html", data=ad_data)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    brand = request.form["brand"]
    model = request.form["model"]
    chassis = request.form["chassis"]
    fuel = request.form["fuel"]
    drive = request.form["drive"]
    transmission = request.form["transmission"]
    mileage = request.form["mileage"]
    year = request.form["year"]
    price = request.form["price"]
    color = request.form["color"]
    engine = request.form["engine"]
    power = request.form["power"]
    legal = request.form["legal"]
    info = request.form["info"]

    #car data
    sql = "UPDATE cars SET brand=:brand, model=:model, chassis=:chassis, fuel=:fuel, drive=:drive, transmission=:transmission, mileage=:mileage, year=:year, price=:price, color=:color, engine=:engine, power=:power, street_legal=:legal WHERE id=:id"
    db.session.execute(sql, {"brand":brand, "model":model, "chassis":chassis, "fuel":fuel, "drive":drive, "transmission":transmission, "mileage":mileage, "year":year, "price":price, "color":color, "engine":engine, "power":power, "legal":legal, "id":id})
    
    #ad data
    sql = "UPDATE ads SET info=:info WHERE ads.car_id=:id"
    db.session.execute(sql, {"info":info, "id":id})

    db.session.commit()
    return redirect("/")
