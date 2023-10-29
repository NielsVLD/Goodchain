import pickle
from database import *
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import filecmp
from pathlib import Path
import pathlib
from Helper import Helper

class Notification:
    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'
    path_poolHash = 'data/poolHash.txt'
    path_blockchainHash = 'data/blockchainHash.txt'

    def __init__(self, user):
        self.user = user

    def show_notifications(self):
        self.show_mined_block_status()

    def show_blockchain_size(self):
        # Show amount blocks, transactions, general blockchain info
        blockchain = Helper().get_blockchain()
        

    def show_mined_block_status(self):
        # Users’ mined block status (if a user already mined a block and the block was on pending for verification by other nodes
        blockchain = Helper().get_blockchain()
        for block in blockchain:
            if not block.validBlock and block.createdBy == self.user:
                print(f"Your block {block.blockId} waiting for validation.\n")

    def show_pending_block_status(self):
        # Any block which was on pending and is confirmed or rejected by this user after login
        pass

    def show_reward(self):
        # Reward notification if there was any reward pending for confirmation from other nodes
        pass

    def show_new_added_blocks(self):
        # New added block(s) since the last login (already confirmed by other nodes or waiting for a confirmation)
        pass

    def show_rejected_transactions(self):
        # Rejected transactions of the user
        pass

    def show_successfull_transactions(self):
        # Successful transactions of the user
        pass

    def show_received_coins(self):
        # Show who send the logged in user coins and how much
        pass