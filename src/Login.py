from database import *
from userActions import TransferCoins
from userActions.Mine import Mine


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
              
                        database.create_timer_user(username)
                        database.create_user(username, password)
                        database.commit()
                        database.close()
                        print("User succesfully added\n")
                        
                        amount = 50
                        receiver = username
                        tx1 = TransferCoins.transferCoins("system").create_signup_reward(receiver, amount)
                        print(tx1)
                        Mine("system").add_system_block_to_chain(tx1)

               
                        print("Error when creating user\n")
        
        def login(self):
                database = Database("userDatabase.db")
                username = input("What is your username: ")
                password = input("What is your password: ")

                try:
                        login = database.login(username=username, password=password)
                        if(login):
                                return username
                        else:   
                                print("Username or password incorrect")
                                return False 
                except:
                        print("Username or password incorrect")




