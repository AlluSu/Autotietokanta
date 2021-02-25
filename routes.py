from app import app
from flask import redirect, render_template, request, session, make_response, abort, flash
from werkzeug.security import generate_password_hash
from db import db
import users
import cars
import ads
import equipment

@app.route("/")
def index():
    car_list = ads.get_essential_car_data()
    admin = users.is_admin(users.get_user_id())
    return render_template("index.html", cars=car_list, admin=admin)

@app.route("/login_user", methods=["POST"])
def login_as_user():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        flash("Kirjautuminen onnistui! Kirjauduit käyttäjänä " + username)
        return redirect("/")
    else:
        return render_template("error.html", error="Tarkista käyttäjätunnus tai salasana!")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/new")
def new_car_form():
    all_equipment = equipment.get_all_car_equipment()
    return render_template("car_form.html", equipment=all_equipment)

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
    car_id = cars.add_car_and_return_id(brand.strip(), model.strip(), chassis, fuel, drive, transmission, mileage,
                year, price, color.strip(), engine, power, legal)

    info = request.form["info"]
    if len(info) > 5000:
        return render_template("error.html", error="Teksti on liian pitkä")
    try:
        ad_id = ads.add_ad_and_return_id(info, car_id)
    except:
        return render_template("error.html", error="Virhe lisätessä ilmoitusta!")
    try:
        ads.create_reference(car_id, ad_id)
    except:
        return render_template("error.html", error="Virhe luodessa viitettä!")

    checked_equipment = request.form.getlist("eq")
    try:
        equipment.create_reference(checked_equipment, car_id)
    except:
        return render_template("error.html", error="Virhe luodessa viitettä!")

    file = request.files["file"]
    name = file.filename
    if file:
        if not name.endswith(".jpg"):
            return render_template("error.html", error="Väärä tiedostopääte")
        data = file.read()
        if len(data) > 100*1024:
            return render_template("error.html", error="Liian iso tiedosto")
        try:
            ads.add_image(name, data, ad_id)
        except:
            return render_template("error.html", error="Kuvan lisäämisessä tapahtui virhe!")   
    flash("Uusi ilmoitus " + brand + " " + model + " lisätty onnistuneesti!")
    return redirect("/")


@app.route("/logout")
def logout():
    try:
        users.logout()
        flash("Kirjauduttu ulos onnistuneesti!")
        return redirect("/")
    except:
        return render_template("error.html", error="Virhe uloskirjautuessa!")

@app.route("/ad/<int:id>")
def ad_page(id):
    ad_data = ads.get_add_data_by_id(id)
    car_id = cars.get_car_id_by_ad_id(id)
    car_data = cars.get_all_car_info_by_id(car_id)
    seller_id = ads.get_user_id_by_ad_id(id)
    seller_data = users.get_user_info_by_id(seller_id)
    cars_equipment = equipment.get_car_equipment_by_id(car_id)
    logged = users.get_user_id()
    admin = users.is_admin(users.get_user_id())
    return render_template("ad_info.html",
        specs=car_data, info=ad_data, seller=seller_data, logged=logged, id=seller_id,
        equipment=cars_equipment, admin=admin)

@app.route("/ad_image/<int:id>")
def show(id):
    #TODO: FIX AND REMOVE TO OWN MODULE
    sql = "SELECT image_id FROM ad_images WHERE ad_images.ad_id=:id"
    result = db.session.execute(sql, {"id":id})
    image_id = result.fetchone()[0]
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql,{"id":image_id})
    image = result.fetchone()[0]
    response = make_response(bytes(image))
    print(response)
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/register", methods=["GET","POST"])
def register():
    return render_template("user_form.html")

@app.route("/new_user", methods=["POST"])
def create_new_user():
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
        users.create_new_user(username.strip(), first_name.strip(), last_name.strip(), phone.strip(),
                        email.strip(), location.strip(), hash_value)
        flash("Uusi käyttäjä " + username + " luotu onnistuneesti!")
        return redirect("/")
    except:
        return render_template("error.html", error="Käyttäjää luodessa tapahtui virhe!")

@app.route("/userinfo")
def show_user_data():
    user = users.get_user_info_by_id(users.get_user_id())
    return render_template("user_data.html", user=user)

@app.route("/update_user_info", methods=["POST"])
def update_user_info():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    first_name = request.form["fname"]
    last_name = request.form["sname"]
    location = request.form["location"]
    phone = request.form["tel"]
    email = request.form["email"]
    try:
        users.update_user_info(users.get_user_id(), first_name.strip(), last_name.strip(), location.strip(),
                               phone.strip(), email.strip())
        flash("Käyttäjätiedot päivitetty onnistuneesti!")
        return redirect("/")
    except:
        return render_template("error.html", error="Tapahtui virhe päivittäessä käyttäjätietoja!")

@app.route("/remove_ad/<int:id>", methods=["POST"])
def remove_ad(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if users.is_admin(users.get_user_id()):
        try:
            ads.remove_ad_as_admin(id)
        except:
            return render_template("error.html", error="Virhe ilmoitusta poistettaessa!")
        flash("Ilmoitus poistettu onnistuneesti!")
        return redirect("/")
    try:
        ads.remove_ad(id, users.get_user_id())
        flash("Ilmoitus poistettu onnistuneesti!")
        return redirect("/")
    except:
        return render_template("error.html", error="Virhe ilmoitusta poistettaessa!")

@app.route("/update_car_info/<int:id>", methods=["POST"])
def edit_car_info(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    all_equipment = equipment.get_all_car_equipment()
    car_spesific_equipment = equipment.get_car_equipment_by_id(id)
    logged = users.get_user_id()
    ad_data = ads.get_logged_users_ad_data(id, logged)
    return render_template("car_data.html", data=ad_data, equipment=all_equipment,
                            car_spesific_equipment=car_spesific_equipment)

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
    if int(mileage) > 10000000 or int(mileage) < 0:
        return render_template("error.html", error="Mittarilukema ei ole sallitulla välillä!")
    year = request.form["year"]
    if int(year) > 2021 or int(year) < 1900:
        return render_template("error.html", error="Vuosimalli ei ole sallitulla välillä!")
    price = request.form["price"]
    if int(price) > 10000000 or int(price) < 1:
        return render_template("error.html", error="Hinta ei ole sallitulla välillä!")
    color = request.form["color"]
    if len(color.strip()) < 1:
        return render_template("error.html", error="Väri ei voi olla tyhjä!")
    engine = request.form["engine"]
    if int(engine) > 10000 or int(engine) < 100:
        return render_template("error.html", error="Moottorin tilavuus ei ole sallitulla välillä!")
    power = request.form["power"]
    if int(power) > 2000 or int(power) < 0:
        return render_template("error.html", error="Teho ei ole sallitulla välillä!")
    legal = request.form["legal"]
    info = request.form["info"]
    checked_equipment = request.form.getlist("varusteet")
    if len(info.strip()) > 5000:
        return render_template("error.html", error="Liikaa tekstiä tekstikentässä!")
    try:
        cars.update_car_data(brand.strip(), model.strip(), chassis, fuel, drive, transmission, mileage, year,
                            price, color.strip(), engine, power, legal, id)
    except:
        return render_template("error.html", error="Tapahtui virhe lisätessä autoa!")
    try:
        ads.update_info(info.strip(), id)
    except:
        return render_template("error.html", error="Tapahtui virhe lisätessä autoa!")
    try:
        equipment.update_equipment(checked_equipment, id)
    except:
        return render_template("error.html", error="Tapahtui virhe lisätessä autoa!")
    flash("Ilmoituksen " + brand + " " + model + " päivitys onnistui!")
    return redirect("/")

@app.route("/search")
def result():
    query = request.args["query"]
    car_ads = ads.get_data_by_query(query)
    admin = users.is_admin(users.get_user_id())
    return render_template("index.html", admin=admin, cars=car_ads)

@app.route("/sort")
def sort():
    option = request.args["options"]
    admin = users.is_admin(users.get_user_id())
    car_ads = ads.get_data_by_option(str(option))
    return render_template("/index.html", admin=admin, cars=car_ads)

@app.route("/own_ads")
def show_logged_users_ads():
    unactive_ads = ads.ads_by_user_id(users.get_user_id(), False)
    active_ads = ads.ads_by_user_id(users.get_user_id(), True)
    return render_template("own_ads.html", unactive=unactive_ads, active=active_ads)