from flask import make_response
from db import db
import users

def remove_ad(ad_id, user_id):
    sql = "UPDATE ads SET visible=False WHERE user_id=:logged AND ads.id=:id"
    db.session.execute(sql, {"logged":user_id, "id":ad_id})
    db.session.commit()

def remove_ad_as_admin(ad_id):
    sql = "UPDATE ads SET visible=False WHERE ads.id=:id"
    db.session.execute(sql, {"id":ad_id})
    db.session.commit()

def add_ad_and_return_id(info, car_id):
    sql = "INSERT INTO ads (info, created, visible, user_id, car_id) VALUES " \
          "(:info, NOW(), :visible, :user_id, :car_id) RETURNING id"
    result = db.session.execute(sql, {"info":info, "visible":True, "user_id":users.get_user_id(), "car_id":car_id})
    ad_id = result.fetchone()[0]
    db.session.commit()
    return ad_id

def ads_by_user_id(id, status):
    sql = "SELECT c.brand, c.model, c.mileage, c.year, c.price, a.id, a.info, a.created FROM cars c, ads a WHERE " \
        "a.user_id=:id AND c.id=a.car_id AND a.visible=:visible ORDER BY created DESC"
    result = db.session.execute(sql, {"id":id, "visible":status})
    ads = result.fetchall()
    return ads

def get_essential_car_data():
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM " \
          "cars c, ads a WHERE c.id=a.car_id " \
          "AND a.visible=True ORDER BY a.created DESC"
    result = db.session.execute(sql)
    cars = result.fetchall()
    db.session.commit()
    return cars

def get_logged_users_ad_data(car_id, logged):
    sql = "SELECT c.id, c.brand, c.model, c.chassis, c.fuel, c.drive, c.transmission, c.mileage, c.year, " \
          "c.price, c.color, c.engine, c.power, c.street_legal, a.info FROM cars c, ads a WHERE " \
          "c.id=:id AND a.user_id=:logged AND a.visible=:visible AND a.car_id=:id"
    result = db.session.execute(sql, {"id":car_id, "logged":logged, "visible":True, "car_id":car_id})
    ad_data = result.fetchall()
    db.session.commit()
    return ad_data

def get_data_by_query(query):
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
          "c.id=a.car_id AND a.info ILIKE :query AND a.visible=True"
    result = db.session.execute(sql, {"query":'%'+query+'%'})
    ads = result.fetchall()
    db.session.commit()
    return ads

def get_data_by_option(option):
    ads = ""
    if option == "none":
        ads = get_essential_car_data()
    elif option == "year":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY year"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "year DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY year DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "brand":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY brand, model"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "brand DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY brand DESC, model DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "mileage":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY mileage"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "mileage DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY mileage DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "price":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY price"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "price DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY price DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "created":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY created"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()
    elif option == "created DESC":
        sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM cars c, ads a WHERE " \
              "c.id=a.car_id AND a.visible=True ORDER BY created DESC"
        result = db.session.execute(sql)
        ads = result.fetchall()
        db.session.commit()  
    return ads

def get_add_data_by_id(ad_id):
    sql = "SELECT id, info, created, user_id, car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":ad_id})
    data = result.fetchall()
    db.session.commit()
    return data

def get_user_id_by_ad_id(ad_id):
    sql = "SELECT user_id FROM ads a WHERE a.id=:id"
    result = db.session.execute(sql, {"id":ad_id}).fetchone()
    id = result[0]
    db.session.commit()
    return id

def update_info(info, car_id):
    sql = "UPDATE ads SET info=:info WHERE ads.car_id=:id"
    db.session.execute(sql, {"info":info, "id":car_id})

def show_ad_image(id):
    sql = "SELECT image_id FROM ad_images WHERE ad_images.ad_id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()
    rows = result.rowcount
    if rows < 1:
        return None
    image_id = result.fetchone()[0]
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":image_id})
    data = result.fetchone()[0]
    db.session.commit()
    if data:
        response = make_response(bytes(data))
        response.headers.set("Content-Type", "image/jpeg")
        return response

def add_image(name, data, ad_id):
    sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    result = db.session.execute(sql, {"name":name, "data":data})
    image_id = result.fetchone()[0]
    db.session.commit()
    sql = "INSERT INTO ad_images (image_id,ad_id) VALUES (:image_id,:ad_id)"
    db.session.execute(sql, {"image_id":image_id, "ad_id":ad_id})
    db.session.commit()

def image_exists(id):
    sql = "SELECT image_id FROM ad_images WHERE ad_images.ad_id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()
    rows = result.rowcount
    if rows < 1:
        return False
    image_id = result.fetchone()[0]
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":image_id})
    data = result.fetchone()[0]
    db.session.commit()
    if data:
        return True