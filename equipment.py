from db import db

def get_all_car_equipment():
    sql = "SELECT * FROM equipment ORDER BY name"
    result = db.session.execute(sql)
    equipment = result.fetchall()
    db.session.commit()
    return equipment

def get_car_equipment_by_id(id):
    sql = "SELECT e.name FROM equipment e, car_equipment ce WHERE ce.car_id=:id AND e.id=ce.equipment_id ORDER BY e.name"
    result = db.session.execute(sql, {"id":id})
    equipment = result.fetchall()
    db.session.commit()
    return equipment

def get_equipment_id_by_name(name):
    sql = "SELECT id FROM equipment WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    name = result.fetchone()[0]
    db.session.commit()
    return name

def create_reference(checked_equipment, car_id):
    equipment_dict = {}
    for i in range(0, len(checked_equipment)):
        equipment_dict[i] = checked_equipment[i]
    sql = "INSERT INTO car_equipment (car_id, equipment_id) VALUES (:car_id, :equipment_id)"
    for name in equipment_dict:
        eq = equipment_dict[name]
        db.session.execute(sql, {"car_id":car_id, "equipment_id":get_equipment_id_by_name(eq)})
    db.session.commit()

def update_equipment(equipment, id):
    sql = "DELETE FROM car_equipment WHERE car_id=:id"
    db.session.execute(sql, {"id":id})
    for i in equipment:
        sql = "INSERT INTO car_equipment (car_id, equipment_id) VALUES (:car_id, :equipment_id)"
        db.session.execute(sql, {"car_id":id, "equipment_id":get_equipment_id_by_name(i)})
    db.session.commit()