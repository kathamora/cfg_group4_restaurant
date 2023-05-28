CREATE DATABASE restaurant_app;

USE restaurant_app;

CREATE TABLE users (
   user_ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   name VARCHAR(50) NOT NULL,
   username VARCHAR(50) NOT NULL,
   password VARCHAR(50) NOT NULL,
   food_preferences VARCHAR(200),
   dietary_restrictions VARCHAR(200)
);


