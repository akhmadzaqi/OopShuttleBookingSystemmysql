import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pbo',
            port= 3300
        )
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()
