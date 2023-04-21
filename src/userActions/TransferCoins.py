import pickle
from time import sleep
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from Transaction import *
from data.database import *


class transferCoins:
    def __init__(self, sender, receiver="", amount=0, transactionfee=0):
            self.sender = sender
            self.receiver = receiver
            self.amount = amount
            self.transactionfee = transactionfee

    def create_transaction(self):
        Tx1 = Tx()
        sender_prv, sender_pbc = self.get_sender_credentials()
        receiver_prv, receiver_pbc = self.get_key_credentials_current_user()

    def get_sender_credentials(self):
        database = Database("userDatabase.db")
        return database.get_credentials(self.sender)


