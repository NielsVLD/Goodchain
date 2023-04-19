import sqlite3
from Signature import generate_keys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hashlib
import bcrypt

class Database:
    def __init__(self, name=None):
        self.conn = None
        self.cursor = None
        if name:
            self.open(name)
    
    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
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
        username = 'admin'
        password = b"123"
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password, salt)
        
        self.cursor.execute(
            "INSERT INTO users VALUES (:username, :password,:private_key,:public_key)",
            {"username": username, "password": hash_password, "private_key": private_key, "public_key": public_key})
        self.commit()

    def computeHash(self):
        password = "123"
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(password),'utf8'))
        return digest.finalize()

    def check_migrations(self):
        # Make and fill database
        try:
            self.query(
                "CREATE TABLE 'users' ('username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT "
                "NULL, 'private_key' VARCHAR NOT NULL, 'public_key' VARCHAR NOT NULL )")
        except:
            Exception("Error while creating tables")
        self.create_super_admin()
        self.open("userDatabase.db")
        self.commit()
