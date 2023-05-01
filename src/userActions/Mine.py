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
                while index < 5:
                    if transactions[index].is_valid():
                        genesisBlock.addTx(transactions[index])
                        index += 1
                    else: 
                        transactions[index].add_status(False)
                        genesisBlock.addTx(transactions[index])
                        print("Invalid transaction detected!")
                        index += 1

                f1 = open(self.path_pool, 'rb+')
                f1.seek(0)
                f1.truncate()

                for transaction in transactions:
                    file2 = open(self.path_pool, "ab+")
                    pickle.dump(transaction, file2)
                
                #self.add_block_to_blockchain(block)
                self.mine_block(genesisBlock)
            else:
                prevBlock = Helper().get_previous_block()
                block = TxBlock(prevBlock)
                index = 0
                while index < 5:
                    if transactions[index].is_valid():
                        block.addTx(transactions[index])
                        index += 1
                    else: 
                        transactions[index].add_status(False)
                        block.addTx(transactions[index])
                        print("Invalid transaction detected!")
                        index += 1

                f1 = open(self.path_pool, 'rb+')
                f1.seek(0)
                f1.truncate()

                for transaction in transactions:
                    file2 = open(self.path_pool, "ab+")
                    pickle.dump(transaction, file2)
                
                #self.add_block_to_blockchain(block)
                self.mine_block(block)
    
    def add_block_to_blockchain(self, block):
        file = open(self.path_blockchain, "ab+")
        pickle.dump(block, file)
        file.close()
        print("Block added to blockchain")

    def mine_block(self, block):
            block.mine_block(self.username)
            self.add_block_to_blockchain(block)
            for transaction in block.data:
                Helper().delete_transaction_in_pool(transaction)



