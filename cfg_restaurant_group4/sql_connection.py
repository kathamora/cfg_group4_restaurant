import mysql.connector
from config import USER, PASSWORD, HOST

class DbConnectionError(Exception):
    pass

try:
   mydb = mysql.connector.connect(
     host=HOST,
     user=USER,
     password=PASSWORD,
     database='restaurant_app',
   )
except mysql.connector.Error as error:
   raise DbConnectionError(error.msg)

