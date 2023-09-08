import mysql.connector
import os
import dotenv

dotenv.load_dotenv()

CONNECTION = mysql.connector.connect(host=os.environ.get('DATABASE_URL'),
                                         database=os.environ.get('DATABASE_NAME'),
                                         user=os.environ.get('DATABASE_USER'),
                                         password=os.environ.get('DATABASE_PASSWORD'))

class Conn():
    def __init__(self):
        self.connection = CONNECTION
        self.cursor = CONNECTION.cursor()
    
    def get_cursor(self):
        return self.cursor
    
    def commit(self):
        self.connection.commit()