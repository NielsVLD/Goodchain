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
            receiver = input("What is the username of the receiver of the transaction?: ")
            amount = float(input("What is the amount to be send?: "))
            transaction_fee = float(input("What is the transaction fee?: "))
            balance = self.check_balance(amount, transaction_fee)

            transaction = self.create_transaction(receiver, amount, transaction_fee)
            self.save_transaction_in_pool(transaction)

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
        else:
            Tx1.add_status(False)
        return Tx1


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
    
    def check_balance(self, amount, transaction_fee):
        pool = []
        total = 0
        file = open(self.path_pool, "rb")
        try:
            while True:
                data = pickle.load(file)
                pool.append(data)
                total += 1
        except:
            pass

    def save_transaction_in_pool(self, transaction):
        file = open(self.path_pool, "ab")
        pickle.dump(transaction, file)
        file.close()

        file = open(self.path_transactionHistory, "ab")
        pickle.dump(transaction, file)
        file.close()

    def cancel_transaction_in_pool(self):
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
                    
                else:
                    print("Choose a number from the list\n")
                    continue
                
            f1 = open(self.path_pool, 'rb+')
            f1.seek(0)
            f1.truncate()

            for transaction in transactions:
                        file2 = open(self.path_pool, "ab+")
                        pickle.dump(transaction, file2)
        else:       
            print("Pool is empty, cannot cancel a transaction\n")