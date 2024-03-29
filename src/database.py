import sqlite3
from Signature import generate_keys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hashlib
import bcrypt
import time
from time import sleep

class Database:
    def __init__(self, name=None):
        self.conn = None
        self.cursor = None
        if name:
            self.open(name)
    
    def open(self, name):
        try:
            self.conn = sqlite3.connect(f"data/{name}")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def query(self, sql, values=None):
        if values is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, values)

    def create_super_admin(self):
        # Super admin for testing purpose
        private_key, public_key = generate_keys()
        private_key = private_key.decode("utf-8")
        public_key = public_key.decode("utf-8")
        username = 'system'
        password = b"123"
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password, salt)
        
        self.cursor.execute(
            "INSERT INTO users VALUES (:username, :password,:private_key,:public_key)",
            {"username": username, "password": hash_password, "private_key": private_key, "public_key": public_key})
        self.commit()

    def create_user(self, username, password):
        private_key, public_key = generate_keys()
        private_key = private_key.decode("utf-8")
        public_key = public_key.decode("utf-8")
        password = password.encode('UTF-8')
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password, salt)

        self.cursor.execute(
            "INSERT INTO users VALUES (:username, :password,:private_key,:public_key)",
            {"username": username, "password": hash_password, "private_key": private_key, "public_key": public_key})
        self.commit()


    def login(self, username, password):
        query = f"SELECT * FROM users WHERE username = ?"
        result = self.cursor.execute(query, (username,)).fetchone()

        db_password = result[1]
        hashed_password = password.encode('UTF-8')
        
        return bcrypt.hashpw(hashed_password, db_password) == db_password
            
    def get_credentials(self, username):
        query = f"SELECT private_key, public_key FROM users WHERE username = ?"
        result = self.cursor.execute(query, (username,)).fetchone()
        return result
    
    def is_unique_username(self, username):
        query = f"SELECT username FROM users WHERE username = ?"
        result = self.cursor.execute(query, (username,)).fetchone()

        if(result == None):
            return True
        else:
            return False

    def check_migrations(self):
        # Make and fill database
        try:
            self.query(
                "CREATE TABLE 'users' ('username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT "
                "NULL, 'private_key' VARCHAR NOT NULL, 'public_key' VARCHAR NOT NULL )")
            self.query(
                "CREATE TABLE 'timer' ('username' VARCHAR(128) NOT NULL, 'time' TIMESTAMP )")
        except:
            Exception("Error while creating tables")
        self.open("userDatabase.db")
        self.commit()
        if self.is_unique_username("system"):
            self.create_super_admin()
        self.commit()

    def get_username_by_pbc(self, pbc):
        query = f"SELECT username FROM users WHERE public_key = ?"
        result = self.cursor.execute(query, (pbc,)).fetchone()
        return result[0]
    
    def set_time_when_mined(self, time, username):
        query = 'UPDATE timer SET time = ? WHERE username = ? '
        self.cursor.execute(query, (time, username))
        self.commit()
    
    def create_timer_user(self, username):
        self.cursor.execute(
            "INSERT INTO timer VALUES (:username, :time)",
            {"username": username, "time": None})
        self.commit()

    def get_time_when_mined(self, username):
        query = f"SELECT time FROM timer WHERE username = ?"
        result = self.cursor.execute(query, (username,)).fetchone()
        return result[0]