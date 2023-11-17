from database import *
from userActions import TransferCoins
from Helper import Helper
class Login:
        def sign_up(self):
                database = Database("userDatabase.db")
                while True:
                        username = input("What is your username: ")
                        is_unique = database.is_unique_username(username)
                        if(is_unique):
                                break
                        else:
                                print("Username is not unique")
                password = input("What is your password: ")
                try:
                        database.create_timer_user(username)
                        database.create_user(username, password)
                        database.commit()
                        database.close()
                        print("User succesfully added\n")
                except:
                        print("Error when creating user\n")
        
        def login(self):
                database = Database("userDatabase.db")
                username = input("What is your username: ")
                password = input("What is your password: ")

                try:
                        login = database.login(username=username, password=password)
                        if(login):
                                chain = Helper().get_blockchain()
                                block_num = 0
                                transaction_num = 0
                                for block in chain:
                                        if block.validBlock:
                                                block_num += 1
                                                for transaction in block.data:
                                                        transaction_num += 1
                                return username
                        else:   
                                print("Username or password incorrect")
                                return False 
                except:
                        print("Username or password incorrect")




