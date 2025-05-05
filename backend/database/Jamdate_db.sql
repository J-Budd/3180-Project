CREATE DATABASE jamdate_db; 

USE jamdate_db;
-- USERS table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    photo TEXT,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PROFILE table
CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id_fk INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    parish VARCHAR(255) NOT NULL,
    biography TEXT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    race VARCHAR(50) NOT NULL,
    birth_year INTEGER NOT NULL,
    height FLOAT NOT NULL,
    fav_cuisine VARCHAR(255) NOT NULL,
    fav_colour VARCHAR(255) NOT NULL,
    fav_school_sibject VARCHAR(255) NOT NULL,
    political BOOLEAN NOT NULL,
    religious BOOLEAN NOT NULL,
    family_oriented BOOLEAN NOT NULL
);

-- FAVOURITE table
CREATE TABLE favourite (
    id SERIAL PRIMARY KEY,
    user_id_fk INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    fav_user_id_fk INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
