from db import db
from flask import session
from os import urandom
from werkzeug.security import check_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    db.session.commit()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            return True

def get_user_id():
    return session.get("user_id", 0)

def get_logged_user():
    return session.get("username",0)

def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]

def is_admin(id):
    if id == 0:
        return False
    sql = "SELECT admin FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    admin = result.fetchone()[0]
    return admin

def get_user_info_by_id(id):
    sql = "SELECT firstname, surname, telephone, email, location FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    info = result.fetchall()
    db.session.commit()
    return info

def create_new_user(username, first_name, last_name, phone, email, location, hash_value):
    sql = "INSERT INTO users (username, firstname, surname, telephone, email, location, admin, password) " \
            "VALUES (:username, :firstname, :surname, :telephone, :email, :location, :admin, :password)"
    db.session.execute(sql, {"username":username,"firstname":first_name,"surname":last_name, "telephone":phone,
                    "email":email, "location":location, "admin":False, "password":hash_value})
    db.session.commit()

def update_user_info(user_id, first_name, last_name, location, phone, email):
    sql = "UPDATE users SET firstname=:firstname, surname=:surname, telephone=:telephone, email=:email, " \
            "location=:location WHERE id=:id"
    db.session.execute(sql, {"id":user_id, "firstname":first_name, "surname":last_name, "telephone":phone,
                             "email":email, "location":location})
    db.session.commit()