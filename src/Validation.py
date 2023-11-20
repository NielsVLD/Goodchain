from Helper import Helper
from Daemon import Daemon
import pickle
from P2P import server
from Daemon import Daemon

class Validation:
    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'

    def validation_ui(self, user):
                print("\n1. Validate pending a block")
                print("2. Validate whole chain")


                try:
                    number = int(input("Which option do you want to choose?: "))
                    if number == 1:
                        self.validate_pending_block(user)
                    if number == 2:
                         self.validate_chain()
                    else:
                           print("Please choose one of the options:\n")
                except:
                    print("Please choose one of the options:\n")

    def validate_block_on_chain(self):
        blockchain = Helper().get_blockchain()
        if blockchain == []:
            print("Chain is empty")
        else:
            index = 1
            for block in blockchain:
                if block.validBlock:
                    if index == 1:
                        print(f"Genesis block {index} with ID: {block.blockId}")
                        print("\n")
                        index += 1
                    else:

                        print(f"Block {index} with ID: {block.blockId}")
                        print("\n")
                        index += 1
            while True:
                try:
                        if index != 1:
                            total = 0
                            print(f"Total number of blocks = {index - 1}")
                            number = int(input("What block do you want to validate? Choose a number: "))
                            if number == 0:
                                print("Pick a number from the list")
                            else:
                                if blockchain[number-1].is_valid():
                                    print(f"Block is valid\n")
                                    break
                                else:
                                    print(f"Block is valid\n")
                                    break
                        else:
                            print("Chain is empty\n")
                            break
                except:
                    print("Pick a number from the list")


    def validate_chain(self):
            blockchain = Helper().get_blockchain()
            if blockchain == []:
                print("Chain is empty")
            else:
                #print(f"\nTotal blocks in chain is {len(blockchain)}.")
                x = 0
                for block in blockchain:
                    if block.validBlock:
                        if block.is_valid():
                            print(f"Block with ID: {block.blockId} is valid.")
                        else:
                            print(f"Block with ID: {block.blockId} is invalid!")
                            x += 1
                if x == 0:
                    print("Chain is empty\n")

    def validate_pending_block(self, username):
        blockchain = Helper().get_blockchain()
        validTransactions = True
        if blockchain != []:
            for block in blockchain:
                if not block.validBlock:
                    if username != block.createdBy:
                        foundUser = False
                        for user in block.validatedByUser:
                            if user == username:
                                foundUser = True
                        if not foundUser:
                            for transaction in block.data:
                                if not transaction.is_valid():
                                    validTransactions = False
                            if validTransactions and block.is_valid():
                                block.isValidBlock.append(True)
                                block.validatedByUser.append(username)
                                print("Daemon validated a pending block True\n")
                            else:
                                block.isValidBlock.append(False)
                                block.validatedByUser.append(username)
                                print("Daemon validated a pending block False\n")
                        else:
                            print("\nError, pending block was already validated by you.")
                    else:
                        print("\nError, cannot validate own block.")
                  
                    with open(self.path_blockchain, 'rb+') as f1:
                        f1.seek(0)
                        f1.truncate()

                    for block in blockchain:
                        with open(self.path_blockchain, "ab+") as file2:
                            pickle.dump(block, file2)
                        
                    blockchain2 = Helper().get_blockchain()
                    for block in blockchain2:
                        if len(block.isValidBlock) != 0:
                            if block.isValidBlock[-1] and block.isValidBlock.count(True) == 3 and block.validBlock == False:
                                block.validBlock = True
                                Daemon().create_mining_reward(block)
                            with open(self.path_blockchain, 'rb+') as f1:
                                f1.seek(0)
                                f1.truncate()
                            for block in blockchain2:
                                with open(self.path_blockchain, "ab+") as file2:
                                    pickle.dump(block, file2)
        else:
            print("\nNo pending block in chain.")

        Helper().create_hash('data/blockchain.dat')
        server.send_blockchain_data()
        server.send_blockchain_tamper_data()