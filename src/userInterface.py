from database import *
from Login import Login
from userActions import TransferCoins
from Helper import Helper
from Daemon import Daemon
from userActions.Mine import Mine
from Validation import Validation
from Notifications import Notification

class UserInterface:
    def main_screen(self):
        choice: int = self.choices(["Login", "Explore the blockchain", "Sign up", "Exit"])
        if choice == 1:
               user = Login().login()
               if(user):
                   self.logged_in_screen(user)
        if choice == 2:
            print("1. See whole chain")
            print("2. See last block")
            try:
                number = int(input("Which option do you want to choose?: "))
                if number == 1:
                    Helper().print_blockchain()        
                if number == 2:
                    Helper().print_last_block_in_chain()
                else:
                    print("Please choose one of the options:\n")
            except:
                print("Please choose one of the options:\n")
        if choice == 3:
            Login().sign_up()
        if choice == 4:
            exit("Goodbye")
        else:
            self.main_screen()

    def logged_in_screen(self, user):
        # Automatic stuff
        if not Helper().check_hash('data/blockchain.dat'):
            exit("Tampering with the blockchain detected!")
            
        Daemon().validate_pending_blocks_in_chain(user)
        Daemon().remove_invalid_transactions_from_pool(user)
        # Daemon().remove_invalid_block(user)

        while True:
            input_amount, output_amount = Helper().calculate_balance(user)
            print(f"\nWelcome {user}! | Balance: {output_amount - input_amount}\n")

            Notification(user).show_notifications()

            choice: int = self.choices(["Transfer coins", "Check the balance", "Explore the blockchain", "Check the pool", "Cancel a transaction", "Modify a transaction in the pool", "See history of transactions", "Mine a block", "Validate", "Logout", "Exit"])
        
            if choice == 1:
                TransferCoins.transferCoins(user).transfer_coins_ui()
            if choice == 2:
                total_input, output = Helper().calculate_balance(user)
                print(f"Total balance = {output - total_input}")

            if choice == 3:
                print("1. See whole chain")
                print("2. See last block")
                try:
                    number = int(input("Which option do you want to choose?: "))
                    if number == 1:
                        Helper().print_blockchain()        
                    if number == 2:
                        Helper().print_last_block_in_chain()
                    else:
                        print("Please choose one of the options:\n")
                        continue
                except:
                    print("Please choose one of the options:\n")




            if choice == 4:
                # Mine(user).new_block()
                Helper().print_pool()
            if choice == 5:
                TransferCoins.transferCoins(user).cancel_transaction_in_pool()
            if choice == 6:
                TransferCoins.transferCoins(user).modify_transaction_in_pool()
            if choice == 7:
                 Helper().see_history_transactions(user)
            if choice == 8:
                Mine(user).mine_ui()
            if choice == 9:
                Validation().validation_ui(user)
            if choice == 10:
                self.main_screen()
            if choice == 11:
                exit("Goodbye")
            else:
                self.logged_in_screen






    def choices(self, choices, question="Which option do you want to choose?: "):
        for idx, choice in enumerate(choices):
            print(f"{idx + 1}. {choice}")
        c = input(question)

        if c.isnumeric() and len(choices) >= int(c) > 0:
            return int(c)
        else:
            print("Please choose one of the options:\n")
            self.choices(choices, question)