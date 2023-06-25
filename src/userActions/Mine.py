import pickle
from TxBlock import *
from Helper import *
from userActions.TransferCoins import transferCoins
from BlockChain import CBlock
import time
from time import sleep
class Mine:
    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'

    def __init__(self, username):
        self.username = username

    def mine_ui(self):
        if self.check_user_can_mine_block():
            self.new_block()
        else:
            print("You cannot mine a block right now. wait a minimum of three minutes in between mining.")

    def new_block(self):
        try:
            if not Helper().check_hash('data/blockchain.dat'):
                exit("Tampering with the blockchain detected!")
            transactions = Helper().get_pool()
            blockchain = Helper().get_blockchain()
            if len(transactions) < 5:
                print("There are not enough transactions in the pool to mine a block \n")
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
                    
                    self.mine_block(block)
        except:
            print("Error while making a transaction block for mining")
    def add_block_to_blockchain(self, block):
        try:
            if not Helper().check_hash('data/blockchain.dat'):
                exit("Tampering with the blockchain detected!")
            file = open(self.path_blockchain, "ab+")
            pickle.dump(block, file)
            file.close()
            print("Block added to blockchain\n")
        except:
            print("Error while trying to add a block to the chain")

    def mine_block(self, block):
            if self.check_if_chain_is_valid():
                try:     
                    start_time = time.time()
                    if block.mine_block(self.username):
                        pass
                        if time.time() - start_time < 10:
                            sleep(10 - int(time.time() - start_time))
                        elapsed = time.time() - start_time
                        current_time = time.time()
                        print("Success! blocked mined in {:0.2f} seconds".format(elapsed))
                    else:
                        print("Error while trying to mine block")

                    self.add_block_to_blockchain(block)
                    Helper().create_hash('data/blockchain.dat')
                    
                    for transaction in block.data:
                        Helper().delete_transaction_in_pool(transaction)
                    database = Database("userDatabase.db")
                    database.set_time_when_mined(current_time, self.username)
                    database.close()
                except:
                    print("Error while trying to mine a block")
            else:
                print("Cannot mine a block. Chain is not valid.")

    def check_user_can_mine_block(self):
        database = Database("userDatabase.db")
        time_when_last_mined = database.get_time_when_mined(self.username)
        current_time = time.time()
        if time_when_last_mined == None:
            return True
        else:
            if current_time < (time_when_last_mined + float(180)):
                return False
        return True

    def check_if_chain_is_valid(self):
        chain = Helper().get_blockchain()
        if chain == []:
            return True
        else:
            if chain[-1].validBlock:
                return True
            else:
                return False
            
    def add_system_block_to_chain(self, transaction):
        blockchain = Helper().get_blockchain()
        if blockchain == []:
                    loop = 0
                    genesisBlock = TxBlock(None)
                    genesisBlock.addTx(transaction)
                    
                    while loop < 4:
                        tx2 = transferCoins("system").create_mock_transaction("system", 0)
                        genesisBlock.addTx(tx2)
                        loop += 1

                    self.system_mine_block(genesisBlock)
        else:
                    loop = 0
                    prevBlock = Helper().get_previous_block()
                    block = TxBlock(prevBlock)
                    block.addTx(transaction)

                    while loop < 4:
                        tx2 = transferCoins("system").create_mock_transaction("system", 0)
                        block.addTx(tx2)
                        loop += 1

                    self.system_mine_block(block)

    def system_mine_block(self, block):
            if self.check_if_chain_is_valid():
                    start_time = time.time()
                    if block.mine_block(self.username):
                        pass
                        if time.time() - start_time < 10:
                            sleep(10 - int(time.time() - start_time))
                        elapsed = time.time() - start_time
                        current_time = time.time()
                        print("Success! blocked mined in {:0.2f} seconds".format(elapsed))
                    else:
                        print("Error while trying to mine block")

                    block.validBlock = True
                    self.add_block_to_blockchain(block)
                    Helper().create_hash('data/blockchain.dat')
              
                    print("Error while trying to mine a block")
            else:
                print("Cannot mine a block. Chain is not valid.")
