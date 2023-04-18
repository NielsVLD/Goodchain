from data.database import *


class UserInterface:
    def main_screen(self):
        database = Database("userDatabase.db")
        database.check_migrations()
        database.close()