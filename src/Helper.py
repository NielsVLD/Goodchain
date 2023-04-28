import pickle
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