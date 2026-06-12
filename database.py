import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="demo",
    database="college_assistant"
)

cursor = db.cursor()