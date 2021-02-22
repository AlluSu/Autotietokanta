from app import app
from db import db
import users

def get_essential_car_data():
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM " \
          "cars c, ads a WHERE c.id=a.car_id " \
          "AND a.visible=True ORDER BY a.created DESC"
    result = db.session.execute(sql)
    cars = result.fetchall()
    db.session.commit()
    return cars

def get_car_id_by_ad_id(id):
    sql = "SELECT car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    db.session.commit()
    return result[0]

def get_all_car_info_by_id(id):
    sql = "SELECT * FROM cars WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    car_data = result.fetchall()
    db.session.commit()
    return car_data