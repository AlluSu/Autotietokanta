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
    sql = "SELECT id, brand, model, mileage, year FROM cars"
    result = db.session.execute(sql)
    cars = result.fetchall()
    return render_template("index.html", cars=cars)

@app.route("/login_user", methods=["POST"])
def login_as_user():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return render_template("no_user.html", user=user)
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            return redirect("/")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

def user_id():
    return session.get("user_id", 0)

@app.route("/new")
def new_car_form():
    return render_template("car_form.html")

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
    sql = "INSERT INTO cars (brand, model, chassis, fuel, drive, transmission, mileage, year, price, color, engine, power, street_legal) VALUES (:brand, :model, :chassis, :fuel, :drive, :transmission, :mileage, :year, :price, :color, :engine, :power, :street_legal)"
    db.session.execute(sql, {"brand":brand, "model":model, "chassis":chassis,
    "fuel":fuel, "drive":drive, "transmission":transmission, "mileage":mileage,
    "year":year, "price":price, "color":color, "engine":engine, "power":power,
    "street_legal":legal})
    db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

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
