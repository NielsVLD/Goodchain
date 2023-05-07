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
                transaction = self.create_transaction(receiver, amount, transaction_fee)
                self.save_transaction_in_pool(transaction)
                Helper().create_hash(self.path_pool)


                # if balance <= 0:
                #     print(f"Balance too low to make transaction. Balance is: {float(balance)}")
                # else:
                #     transaction = self.create_transaction(receiver, amount, transaction_fee)
                #     if transaction == None:
                #         print("Transaction is not valid\n")
                #     else:
                #         self.save_transaction_in_pool(transaction)
                #         Helper().create_hash(self.path_pool)
                #         print("Transaction successfully created and added to pool\n")
            except:
                print("Error when creating transaction, try again")

    def create_transaction(self, receiver, amount, transaction_fee):
        Tx1 = Tx()
        sender_prv, sender_pbc = self.get_sender_credentials()
        receiver_prv, receiver_pbc = self.get_receiver_credentials(receiver)

        Tx1.add_input(sender_pbc, amount)
        Tx1.add_output(receiver_pbc, amount - transaction_fee)
        Tx1.sign(sender_prv)
        Tx1.add_username(self.sender)

        if Tx1.is_valid():
            Tx1.add_status(True)
            print("valid transaction")
            return Tx1
        else:
            print("Invalid transaction")
            return None


    def get_sender_credentials(self):
        database = Database("userDatabase.db")
        result = database.get_credentials(self.sender)

        sender_prv = result[0]
        sender_pbc = result[1]

        sender_prv_encoded = sender_prv.encode('UTF-8')
        sender_pbc_encoded = sender_pbc.encode('UTF-8')
        
        sender_prv_deserialized = load_pem_private_key(sender_prv_encoded, password=None)
        return sender_prv_deserialized, sender_pbc_encoded

    def get_receiver_credentials(self, receiver):
        database = Database("userDatabase.db")
        result = database.get_credentials(receiver)

        sender_prv = result[0]
        sender_pbc = result[1]

        sender_prv_encoded = sender_prv.encode('UTF-8')
        sender_pbc_encoded = sender_pbc.encode('UTF-8')
        sender_prv_deserialized = load_pem_private_key(sender_prv_encoded, password=None)
        
        return sender_prv_deserialized, sender_pbc_encoded
    
    # def check_balance(self, amount, transaction_fee):
    #     pool = []
    #     total = 0
    #     file = open(self.path_pool, "rb")
    #     try:
    #         while True:
    #             data = pickle.load(file)
    #             pool.append(data)
    #             total += 1
    #     except:
    #         pass

    def save_transaction_in_pool(self, transaction):
        if not Helper().check_hash('data/pool.dat'):
           exit("Tampering with pool detected!")
        file = open(self.path_pool, "ab")
        pickle.dump(transaction, file)
        file.close()

        file = open(self.path_transactionHistory, "ab")
        pickle.dump(transaction, file)
        file.close()

    def cancel_transaction_in_pool(self):
        if not Helper().check_hash('data/pool.dat'):
           exit("Tampering with pool detected!")
        if not Helper().is_pool_empty():
            sender_prv, sender_pbc = self.get_sender_credentials()
            transactions = []
            transactions_to_delete = []
            index = 0
            file = open(self.path_pool, "rb")
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
                    print("Choose a number from the list\n")
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
                    print("Choose a number from the list\n")
                    continue
                
            f1 = open(self.path_pool, 'rb+')
            f1.seek(0)
            f1.truncate()

            for transaction in transactions:
                        file2 = open(self.path_pool, "ab+")
                        pickle.dump(transaction, file2)
            Helper().create_hash(self.path_pool)
        else:       
            print("Pool is empty, cannot cancel a transaction\n")

    def modify_transaction_in_pool(self):
        if not Helper().check_hash('data/pool.dat'):
           exit("Tampering with pool detected!")
        if not Helper().is_pool_empty():
            sender_prv, sender_pbc = self.get_sender_credentials()
            transactions = []
            transactions_to_update = []
            index = 0
            file = open(self.path_pool, "rb")
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
                    print("Choose a number from the list\n")
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
                            print("valid transaction")
                        else:
                            transaction.add_status(False)
                            print("Invalid transaction")
                        f1 = open(self.path_pool, 'rb+')
                        f1.seek(0)
                        f1.truncate()

                        for transaction in transactions:
                                    file2 = open(self.path_pool, "ab+")
                                    pickle.dump(transaction, file2)  
                        Helper().create_hash(self.path_pool)
                    else:
                        print("You can only update your own transactions\n")
                    break
                else:
                    print("Choose a number from the list\n")
                    continue
        else:       
            print("Pool is empty, cannot cancel a transaction\n")
    
    def create_signup_reward(self, receiver, amount):
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