import pickle
from database import *
from cryptography.hazmat.primitives.serialization import load_pem_private_key
class Helper:

    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'

    def print_pool(self):
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
        
        for transaction in pool:
            print(f"{transaction}\n")
        
        print(f"Total in pool = {total}\n")
        
    def is_pool_empty(self):
        pool = []
        file = open(self.path_pool, "rb")
        try:
            while True:
                data = pickle.load(file)
                pool.append(data)
        except:
            pass
            
        if pool == []:
            return True
        else:
            return False
    
    def see_history_transactions(self, username):
        pool = []
        total = 0
        file = open(self.path_transactionHistory, "rb")
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
        file = open(self.path_pool, "rb")
        try:
            while True:
                data = pickle.load(file)
                transactions.append(data)
        except:
            pass
        
        return transactions
    
    def get_blockchain(self):
        blockchain = []
        file = open(self.path_blockchain, "rb")
        try:
            while True:
                data = pickle.load(file)
                blockchain.append(data)
        except:
            pass

        return blockchain
    
    def print_blockchain(self):
        blockchain = self.get_blockchain()
        if blockchain == []:
            print("Chain is empty")
        else:
            index = 1
            for block in blockchain:
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
                    total = 0
                    number = int(input("What block do you want to see? Choose a number: "))
                    if number-1 == 0:
                        print("Pick a number from the list")
                        for transaction in blockchain[number-1].data:
                            print(transaction)
                            total +=1 
                        print(f"Block Id: {blockchain[number-1].blockId}")
                        print(f"Total transactions = {total}\n")
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
                    print(f"Total transactions = {total}\n")
                    break
                except:
                    print("Error")

    def get_previous_block(self):
        block = []
        index = 0
        file = open(self.path_blockchain, "rb")
        try:
            while True:
                data = pickle.load(file)
                block.append(data)
                index += 1
        except:
            pass
        
        return block[index-1]

    def delete_transaction_in_pool(self, transaction):
        pool = self.get_pool()
        new_pool = []
        for transaction_pool in pool:
            if transaction_pool.id != transaction.id:
                new_pool.append(transaction_pool)

        f1 = open(self.path_pool, 'rb+')
        f1.seek(0)
        f1.truncate()
        f1.close()

        file2 = open(self.path_pool, "ab+")
        for transaction in range(len(new_pool)):
            pickle.dump(new_pool[transaction], file2)
        file2.close()
    
    def calculate_balance(self, username):
        blockchain = self.get_blockchain()
        database = Database("userDatabase.db")
        result = database.get_credentials(username)
        user_pbc = result[1].encode("utf-8")
        input = 0
        output = 0
        start_amount = 50

        for block in blockchain:
            print(block)
            for transaction in block.data:
                for addr, amount in transaction.inputs:
                    if addr == user_pbc:
                        input += amount
                for addr, amount in transaction.outputs:
                        if addr == user_pbc:
                            output += amount
                  
        total_input = input
        total_output = output

        return total_input, total_output






    # def calculate_balance(self,input, output, user_pbc):
    #     if input and output == None:
    #         input = []
    #         output = []

        # total_in, total_out = self.__count_totals(user_pbc)

    #     input.append(total_in)
    #     output.append(total_out)
    #     if self.previousBlock is None:
    #         received = 50
    #         spent = 0
    #         for coins in input:
    #             spent += coins
    #         for coins in output:
    #             received += coins
    #         return received - spent
    #     else:
    #         return self.previousBlock.calculate_balance(input, output, user_pbc)