from data.database import *

def __init__(self, connection, username, password):
        self.connection = connection
        self.username = username
        self.password = password

def sign_up():
        database = Database("userDatabase.db")

        username = input("What is your username: ")
        password = input("What is your password: ")
        try:
                database.create_user(username, password)
                database.commit()
                database.close()
                print("User succesfully added\n")
        except:
                print("Error when creating user\n")
        
def login():
        database = Database("userDatabase.db")
        username = input("What is your username: ")
        password = input("What is your password: ")

        try:
                login = database.login(username=username, password=password)
                if(login):
                        print("Loggin succesful")
                        return True
                else:   
                        print("Username or password incorrect")
                        return False 
        except:
                print("Unknown error")




