from sql_connection import mydb
import streamlit as st
import re

class UserNotFoundError(Exception):
    pass
class UserAuthenticator:
    def __init__(self, mydb):
        self.mydb = mydb

    def validate_email(self, email):
        pattern = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        return re.match(pattern, email)

    def validate_username(self, username):
        # accepts A-Z, a-z, 0-9
        pattern = r"^[A-Za-z][A-Za-z0-9_]{7,29}$"
        return re.match(pattern, username)

    # password contains at least one uppercase letter, one lowercase letter, and one digit
    def validate_password(self, password):
        # Check password length
        if len(password) < 8:
            return False
        return True

    def check_email_exists(self, email):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        result = mycursor.fetchone()
        return result is not None


    def check_username_exists(self, username):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        result = mycursor.fetchone()
        return result is not None

    def signup(self, email, username, password):
        if not self.validate_email(email):
            raise ValueError("Invalid email format")

        if not self.validate_username(username):
            raise ValueError("Invalid username format")

        if not self.validate_password(password):
            raise ValueError("Invalid password format")

        if self.check_email_exists(email):
            raise ValueError("Email already exists")

        if self.mydb is None:  # Check if mydb is None
            raise ValueError("Database connection not established")

        mycursor = self.mydb.cursor()
        mycursor.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)",
                         (email, username, password))
        self.mydb.commit()
        return username, password, email

    def login(self, username, password):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = mycursor.fetchone()
        if result:
            return username, password
        else:
            raise ValueError("Incorrect username or password")

    def get_user_info(self, field, value):
        if field == "email" and not self.validate_email(value):
            raise ValueError("Invalid email format")

        if field == "username" and not self.validate_username(value):
            raise ValueError("Invalid username format")
        print(f"Field: {field}, Value: {value}")

        mycursor = self.mydb.cursor()
        query = "SELECT * FROM users WHERE {} = %s".format(field)
        print(query)
        mycursor.execute(query, (value,))
        result = mycursor.fetchone()

        if result:
            user_id = result[0]
            username = result[1]
            email = result[2]
            password = result[3]
            return user_id, username, email, password
        else:
            raise ValueError("User not found")
