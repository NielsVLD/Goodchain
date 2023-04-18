import sqlite3

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

    def check_migrations(self):

        try:
            self.query(
                "CREATE TABLE 'username' ('id' INTEGER PRIMARY KEY NOT NULL, 'password' VARCHAR(128) NOT "
                "NULL, 'private_key' VARCHAR(128) NOT NULL, 'public_key' VARCHAR(128) NOT NULL ")
        except:
            Exception("Error while creating tables")
        self.open("userDatabase.db")
        self.commit()
