from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv, urandom
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

def create_session_token():
    return urandom(16).hex()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #TODO: check username and password
    session["username"] = username
    return redirect("/")

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
    year = request.form["year"]
    price = request.form["price"]
    color = request.form["color"]
    engine = request.form["engine"]
    power = request.form["power"]
    legal = request.form["legal"]
    info = request.form["info"]
    return render_template("result.html", brand=brand,
    model=model, chassis=chassis, fuel=fuel, drive=drive,
    transmission=transmission, year=year, price=price,
    color=color, engine=engine, power=power,
    legal=legal, info=info)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    return redirect("/")
