import pickle
class Helper:

    path_pool = 'data/pool.dat'
    
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