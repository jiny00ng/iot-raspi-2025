import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="iotuser",
        password="iotpassword",
        database="warehouse_monitor"
    )
