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

CREATE TABLE ads (
    id SERIAL PRIMARY KEY,
    info TEXT,
    created TIMESTAMP,
    visible BOOLEAN
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

/*
CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    name UNIQUE,
);

CREATE TABLE car_equipment (
    car_id REFERENCES cars,
    equipment_id REFERENCES equipment
);

CREATE TABLE car_ad (
    car_id REFERENCES cars,
    ad_id REFERENCES ads
);
*/
