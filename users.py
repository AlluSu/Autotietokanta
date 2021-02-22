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
    try:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
        return True
    except:
        return False

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