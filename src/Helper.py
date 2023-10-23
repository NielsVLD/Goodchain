import pickle
from database import *
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import filecmp
from pathlib import Path
import pathlib
class Helper:

    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'
    path_poolHash = 'data/poolHash.txt'
    path_blockchainHash = 'data/blockchainHash.txt'

    path_test = 'data/test.dat'

    def print_pool(self):
        pool = []
        total = 0
        with open(self.path_pool, "rb+") as file:
            try:
                while True:
                    data = pickle.load(file)
                    pool.append(data)
                    total += 1
            except EOFError:
                pass
        
        for transaction in pool:
            print(f"{transaction}\n")
        
        print(f"Total in pool = {total}\n")


    def is_pool_empty(self):
        pool = []
        with open(self.path_pool, "rb") as file:
            try:
                while True:
                    data = pickle.load(file)
                    pool.append(data)
            except EOFError:
                pass
            
        if pool == []:
            return True
        else:
            return False
    
    def see_history_transactions(self, username):
        pool = []
        total = 0
        with open(self.path_transactionHistory, "rb") as file:
            try:
                while True:
                    data = pickle.load(file)
                    pool.append(data)
            except:
                pass
        for transaction in pool:
            if(transaction.username[0] == username):
                print(f"{transaction}\n")
                total += 1
        
        print(f"Total transactions made = {total}\n")
        
    def get_pool(self):
        transactions = []
        with open(self.path_pool, "rb+") as file:
            try:
                while True:
                    data = pickle.load(file)
                    transactions.append(data)
            except EOFError:
                pass
    
        return transactions
    
    def get_blockchain(self):
        blockchain = []
        with open(self.path_blockchain, "rb+") as file:
            try:
                while True:
                    data = pickle.load(file)
                    blockchain.append(data)
            except EOFError:
                pass
        
        file.close()
        return blockchain
    
    def print_blockchain(self):
        blockchain = self.get_blockchain()
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
                            number = int(input("What block do you want to see? Choose a number: "))
                            if number == 0:
                                print("Pick a number from the list")
                            else:
                                if blockchain[number-1].validBlock:
                                    for transaction in blockchain[number-1].data:
                                        print(transaction)
                                        total +=1 
                                    print(f"Block Id: {blockchain[number-1].blockId}")
                                    print(f"Total transactions = {total}\n")
                                    print(f"Block has been validated: {blockchain[number-1].validBlock}")
                            break
                        else:
                            print("Chain is empty\n")
                            break
                except:
                    print("Pick a number from the list")
    def print_last_block_in_chain(self):
        blockchain = self.get_blockchain()
        if blockchain == []:
            print("Chain is empty")
        else:
            if len(blockchain) == 1:
                    print(f"Genesis block with ID: {blockchain[-1].blockId}")
                    print("\n")
            else:

                print(f"Block with ID: {blockchain[-1].blockId}")
                print("\n")
            while True:
                try:
                    total = 0
                    for transaction in blockchain[-1].data:
                        print(transaction)
                        total +=1 
                    print(f"Block Id: {blockchain[-1].blockId}")
                    print(f"Total transactions = {total}")
                    print(f"Block has been validated: {blockchain[-1].validBlock}\n")

                    break
                except:
                    print("Error when getting blockchain")

    def get_previous_block(self):
        block = []
        index = 0
        with open(self.path_blockchain, "rb") as file:
            try:
                while True:
                    data = pickle.load(file)
                    block.append(data)
                    index += 1
            except EOFError:
                pass
        
        file.close()
        return block[index-1]

    def delete_transaction_in_pool(self, block):
        new_pool = []
        pool = self.get_pool()

        for transaction in pool:
            if transaction not in block.data:
                new_pool.append(transaction)


        with open(self.path_pool, 'wb') as file:
            file.truncate()
            file.close()

        # for transaction in new_pool:
        #     pickle.dump(transaction, f1)
        # else:
        #     f1.close()



        # new_pool = []
        # for transaction_pool in pool:
        #     if transaction_pool.id != transaction.id:
        #         new_pool.append(transaction_pool)

        # f1 = open(self.path_pool, 'rb+')
        # f1.seek(0)
        # f1.truncate()
        # for i in range(len(new_pool)):
        #     pickle.dump(new_pool[i], f1)
        # else:
        #     f1.close()
        # self.create_hash(self.path_pool)
    
    def calculate_balance(self, username):

        blockchain = self.get_blockchain()
        pool = self.get_pool()
        database = Database("userDatabase.db")
        result = database.get_credentials(username)
        user_pbc = result[1].encode("utf-8")
        input = 0
        output = 0

        for block in blockchain:
            for transaction in block.data:
                for addr, amount in transaction.inputs:
                    if addr == user_pbc:
                        input += amount
                for addr, amount in transaction.outputs:
                        if addr == user_pbc:
                            output += amount
                
        
        for transaction in pool:
            for addr, amount in transaction.inputs:
                    if addr == user_pbc:
                        input += amount
            for addr, amount in transaction.outputs:
                    if addr == user_pbc:
                        output += amount
        
        total_input = input
        total_output = output

        return total_input, total_output

    def create_hash(self, path):
        pool = self.get_pool()
        blockchain = self.get_blockchain()
        history = self.get_history()

        if path == self.path_pool:
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(bytes(str(pool),'utf8'))
            hashed_pool = digest.finalize()

            file = open(self.path_poolHash, "wb")
            pickle.dump(hashed_pool, file)
            file.close()
    

        if path == self.path_blockchain:
            with open(self.path_blockchain, "rb") as file:
                sha256 = hashlib.sha256()
                for block in iter(lambda: file.read(4096), b""):
                    sha256.update(block)
                hashed_blockchain = sha256.hexdigest()

           
            file = open(self.path_blockchainHash, "w")
            file.write(hashed_blockchain)
            file.close()


    def check_hash(self, path):
        pool = self.get_pool()
        blockchain = self.get_blockchain()
        history = self.get_history()
        if path == self.path_pool:
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(bytes(str(pool),'utf8'))
            hashed_pool = digest.finalize()
            
            file = open(self.path_poolHash, "rb+")
            storedPoolHash = pickle.load(file)
            file.close()
            
            result = hashed_pool == storedPoolHash
            return result

        if path == self.path_blockchain:
            with open(self.path_blockchain, "rb") as file:
                sha256 = hashlib.sha256()
                for block in iter(lambda: file.read(4096), b""):
                    sha256.update(block)
                hashed_blockchain = sha256.hexdigest()
            
            with open(self.path_blockchainHash, "r") as file:
                storedBlockchainHash = file.read()

            result = hashed_blockchain == storedBlockchainHash
            return True


    def get_history(self):
        transactions = []
        with open(self.path_transactionHistory, "rb+") as file:
            try:
                while True:
                    data = pickle.load(file)
                    transactions.append(data)
            except EOFError:
                pass
        
        return transactions
    
