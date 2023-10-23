import pickle
from time import sleep
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from Transaction import *
from database import *
from TxBlock import TxBlock
from Helper import Helper
class transferCoins:
    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'

    def __init__(self, sender):
        self.sender = sender
    
    def transfer_coins_ui(self):
            try:
                receiver = input("What is the username of the receiver of the transaction?: ")
                amount = float(input("What is the amount to be send?: "))
                transaction_fee = float(input("What is the transaction fee?: "))
                total_input, total_output = Helper().calculate_balance(self.sender)
                balance = total_output - total_input
                #transaction = self.create_transaction(receiver, amount, transaction_fee)


                if receiver == self.sender:
                    print("Cannot make a transaction to yourself\n")
                else:
                    if amount == 0:
                        print("Amount to be send needs to be bigger than 0 to make a transaction\n")
                    else:
                        if balance <= 0 or amount + transaction_fee > balance:
                            print(f"Balance too low to make a transaction. Balance is: {float(balance)}")
                        else:
                            transaction = self.create_transaction(receiver, amount, transaction_fee)
                            if transaction == None:
                                print("Transaction is not valid\n")
                            else:
                                self.save_transaction_in_pool(transaction)
                                Helper().create_hash(self.path_pool)
                                print("Transaction successfully created and added to pool\n")
            except:
                print("Error when creating transaction")

    def create_transaction(self, receiver, amount, transaction_fee):
        try:
            Tx1 = Tx()
            sender_prv, sender_pbc = self.get_sender_credentials()
            receiver_prv, receiver_pbc = self.get_receiver_credentials(receiver)

            Tx1.add_input(sender_pbc, amount + transaction_fee)
            Tx1.add_output(receiver_pbc, amount)
            Tx1.sign(sender_prv)
            Tx1.add_username(self.sender)

            if Tx1.is_valid():
                Tx1.add_status(True)
                return Tx1
            else:
                return None
        except:
            print("Error while creating transaction\n")


    def get_sender_credentials(self):
        try:

            database = Database("userDatabase.db")
            result = database.get_credentials(self.sender)

            sender_prv = result[0]
            sender_pbc = result[1]

            sender_prv_encoded = sender_prv.encode('UTF-8')
            sender_pbc_encoded = sender_pbc.encode('UTF-8')
            
            sender_prv_deserialized = load_pem_private_key(sender_prv_encoded, password=None)
            return sender_prv_deserialized, sender_pbc_encoded
        except:
            print("Error while trying to get sender credentails\n")

    def get_receiver_credentials(self, receiver):
        try:

            database = Database("userDatabase.db")
            result = database.get_credentials(receiver)

            sender_prv = result[0]
            sender_pbc = result[1]

            sender_prv_encoded = sender_prv.encode('UTF-8')
            sender_pbc_encoded = sender_pbc.encode('UTF-8')
            sender_prv_deserialized = load_pem_private_key(sender_prv_encoded, password=None)
            
            return sender_prv_deserialized, sender_pbc_encoded 
        except:
            print("Error while trying to get receiver credentials\n")

    def save_transaction_in_pool(self, transaction):
        try:

            file = open(self.path_pool, "ab")
            pickle.dump(transaction, file)
            file.close()

            file = open(self.path_transactionHistory, "ab")
            pickle.dump(transaction, file)
            file.close()
        except:
            print("Error while trying to save a transaction in the pool")

    def cancel_transaction_in_pool(self):
        try:
            if not Helper().is_pool_empty():
                sender_prv, sender_pbc = self.get_sender_credentials()
                transactions = []
                transactions_to_delete = []
                index = 0
                with open(self.path_pool, "rb") as file:
                    try:
                        while True:
                            data = pickle.load(file)
                            transactions.append(data)
                            transactions_to_delete.append(data.inputs)

                    except:
                        pass
                
                for transaction in transactions:
                    print(f"Transaction {index}: \n {transaction}")
                    index += 1
                
                while True:
                    try:
                        num = int(input("What transaction do you want to delete?: "))
                    except:
                        print("Please choose one of the options:\n")
                        continue
                    index = 0
                    if type(num) == int and num < len(transactions):
                        
                        if transactions_to_delete[num][0][0] == sender_pbc:
                            transactions.pop(num)
                            print("Transaction removed from pool\n")
                            break
                        else:
                            print("You can only delete your own transactions\n")
                            break
                    else:
                        print("Please choose one of the options:\n")
                        break
                    
                with open(self.path_pool, 'rb+') as f1:
                    f1.seek(0)
                    f1.truncate()

                for transaction in transactions:
                            with open(self.path_pool, "ab+") as file2:
                                pickle.dump(transaction, file2)
                Helper().create_hash(self.path_pool)
            else:       
                print("Pool is empty, cannot cancel a transaction\n")
        except:
            print("Error while trying to cancel a transaction")
    def modify_transaction_in_pool(self):
        try:
            if not Helper().is_pool_empty():
                sender_prv, sender_pbc = self.get_sender_credentials()
                transactions = []
                transactions_to_update = []
                index = 0
                with open(self.path_pool, "rb") as file:
                    try:
                        while True:
                            data = pickle.load(file)
                            transactions.append(data)
                            transactions_to_update.append(data.inputs)

                    except:
                        pass
                
                for transaction in transactions:
                    print(f"Transaction {index}: \n {transaction}")
                    index += 1
                
                while True:
                    try:
                        num = int(input("What transaction do you want to update?: "))
                    except:
                        print("Please choose one of the options:\n")
                        continue
                    index = 0
                    if type(num) == int and num < len(transactions):
                        if transactions_to_update[num][0][0] == sender_pbc:
                            receiver = input("What is the username of the receiver of the transaction?: ")
                            amount = float(input("What is the amount to be send?: "))
                            transaction_fee = float(input("What is the transaction fee?: "))
                            receiver_prv, receiver_pbc = self.get_receiver_credentials(receiver)
                            
                            transaction.inputs = []
                            transaction.outputs = []
                            transaction.sigs = []
                            transaction.inputs = [(sender_pbc, amount)]
                            transaction.outputs = [(receiver_pbc, amount - transaction_fee)]
                            transaction.sign(sender_prv)
                            transaction.isValidTx = []

                            if transaction.is_valid():
                                transaction.add_status(True)
                                print("Valid transaction added to the pool, waiting for mining")
                            else:
                                transaction.add_status(False)
                                print("Invalid transaction, try again")
                            with open(self.path_pool, 'rb+') as f1:
                                f1.seek(0)
                                f1.truncate()

                            for transaction in transactions:
                                        with open(self.path_pool, "ab+") as file2:
                                            pickle.dump(transaction, file2) 
                            Helper().create_hash(self.path_pool)
                        else:
                            print("You can only update your own transactions\n")
                        break
                    else:
                        print("Please choose one of the options:\n")
                        continue
            else:       
                print("Pool is empty, cannot cancel a transaction\n")
        except:
            print("Error while trying to modify a transaction")

    def create_signup_reward(self, receiver, amount):
        try:
            Tx1 = Tx()
            sender_prv, sender_pbc = self.get_sender_credentials()
            receiver_prv, receiver_pbc = self.get_receiver_credentials(receiver)

            Tx1.add_input(sender_pbc, amount)
            Tx1.add_output(receiver_pbc, amount)
            Tx1.sign(sender_prv)
            Tx1.add_username(self.sender)

            if Tx1.is_valid():
                Tx1.add_status(True)
                self.save_transaction_in_pool(Tx1)
                Helper().create_hash(self.path_pool)
            else:
                print("Invalid transaction")
        except:
            print("Error while trying to create a signup reward")