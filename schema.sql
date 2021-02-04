CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    brand TEXT,
    model TEXT,
    chassis TEXT,
    fuel TEXT,
    drive TEXT,
    transmission TEXT,
    mileage INTEGER,
    year INTEGER,
    price INTEGER,
    color TEXT,
    engine INTEGER,
    power INTEGER,
    street_legal BOOLEAN
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    firstname TEXT,
    surname TEXT,
    telephone TEXT,
    email TEXT,
    location TEXT,
    admin BOOLEAN,
    password TEXT
);

CREATE TABLE ads (
    id SERIAL PRIMARY KEY,
    info TEXT,
    created TIMESTAMP,
    visible BOOLEAN,
    user_id INTEGER REFERENCES users,
    car_id INTEGER REFERENCES cars
);

CREATE TABLE car_ad (
    car_id INTEGER REFERENCES cars,
    ad_id INTEGER REFERENCES ads
);

CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

/* Hard coded equipment */
INSERT INTO equipment (name) VALUES ('Nahkaverhoilu');
INSERT INTO equipment (name) VALUES ('Ilmastointi');
INSERT INTO equipment (name) VALUES ('Vakionopeudensäädin');
INSERT INTO equipment (name) VALUES ('Kattoluukku');
INSERT INTO equipment (name) VALUES ('Keskuslukitus'); 
INSERT INTO equipment (name) VALUES ('Ilmajouset');
INSERT INTO equipment (name) VALUES ('Vetokoukku');
INSERT INTO equipment (name) VALUES ('Huoltokirja');
INSERT INTO equipment (name) VALUES ('Luistonestojärjestelmä');
INSERT INTO equipment (name) VALUES ('ABS-jarrut');
INSERT INTO equipment (name) VALUES ('Pysäköintitutka');
INSERT INTO equipment (name) VALUES ('Sähkösäätöiset penkit');

CREATE TABLE car_equipment (
    car_id INTEGER REFERENCES cars,
    equipment_id INTEGER REFERENCES equipment
);
