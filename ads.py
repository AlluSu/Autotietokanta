from flask.templating import render_template
from db import db
import users

def add_ad_and_return_id(info, car_id):
    sql = "INSERT INTO ads (info, created, visible, user_id, car_id) VALUES " \
          "(:info, NOW(), :visible, :user_id, :car_id) RETURNING id"
    result = db.session.execute(sql, {"info":info, "visible":True, "user_id":users.get_user_id(), "car_id":car_id})
    ad_id = result.fetchone()[0]
    return ad_id

def create_reference(car_id, ad_id):
    sql = "INSERT INTO car_ad (car_id, ad_id) VALUES (:car_id, :ad_id)"
    db.session.execute(sql, {"car_id":car_id, "ad_id":ad_id})