import pickle
from TxBlock import *
from Helper import *
from userActions.TransferCoins import transferCoins
from BlockChain import CBlock
class Mine:
    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'

    def __init__(self, username):
        self.username = username

    def mine_ui(self):
        self.new_block()

    def new_block(self):
        transactions = Helper().get_pool()
        blockchain = Helper().get_blockchain()
        file_blockchain = open(self.path_blockchain, "rb")
        file_transactions = open(self.path_pool, "rb")
        sender_prv, sender_pbc = transferCoins(self.username).get_sender_credentials()
        if len(transactions) < 5:
            print("There are not enough transactions in the pool")
        else:
            if blockchain == []:
                genesisBlock = TxBlock(None)
                index = 0
                while index <= 5:
                    if transactions[index].is_valid():
                        print("Valid transaction")
                        genesisBlock.addTx(transactions[index])
                        index += 1
                    else: 
                        transactions[index].add_status(False)
                        print("Invalid transaction detected!")
                        index += 1
                self.add_block_to_blockchain(genesisBlock)
            else:
                prevBlock = CBlock.previousBlock
                print(prevBlock)
                block = TxBlock(prevBlock)
                index = 0
                while index <= 5:
                    block.addTx(transactions[index])
                    index += 1
                self.add_block_to_blockchain(block)
    
    def add_block_to_blockchain(self, block):
        file = open(self.path_blockchain, "ab+")
        pickle.dump(block, file)
        file.close()
        print("Block added to blockchain")
