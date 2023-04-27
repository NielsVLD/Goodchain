from userActions.TransferCoins import *
class Daemon:

    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'

    def remove_invalid_transactions_from_pool(self, username):
        sender_prv, sender_pbc = transferCoins(username).get_sender_credentials()
        transactions = []
        index = 0
        file = open(self.path_pool, "rb")

        try:
            while True:
                data = pickle.load(file)
                transactions.append(data)
        except:
            pass
        
        for transaction in transactions:
            for valid in transaction.isValidTx:
                if valid == False and transaction.inputs[0][0] == sender_pbc:
                    transactions.pop(index)
                    print("Daemon removed invalid transactions from pool\n")
            index += 1
        
        f1 = open(self.path_pool, 'rb+')
        f1.seek(0)
        f1.truncate()

        for transaction in transactions:
            file2 = open(self.path_pool, "ab+")
            pickle.dump(transaction, file2)
