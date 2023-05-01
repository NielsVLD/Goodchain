from userActions.TransferCoins import *
class Daemon:

    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'


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

    def validate_pending_blocks_in_chain(self, username):
        blockchain = Helper().get_blockchain()
        validTransactions = True
        if blockchain != []:
            for block in blockchain:
                if username != block.createdBy:
                    foundUser = False
                    for user in block.validatedByUser:
                        if user == username:
                            print("cannot validate block, has been done already")
                            foundUser = True
                    if not foundUser:
                        for transaction in block.data:
                            if not transaction.is_valid():
                                validTransactions = False
                        if validTransactions and block.is_valid():
                            block.isValidBlock.append(True)
                            block.validatedByUser.append(username)
                            print("Valid Block")
                        else:
                            block.isValidBlock.append(False)
                            block.validatedByUser.append(username)
                            print("Invalid block")

                f1 = open(self.path_blockchain, 'rb+')
                f1.seek(0)
                f1.truncate()

                for block in blockchain:
                    file2 = open(self.path_blockchain, "ab+")
                    pickle.dump(block, file2)

        # Remove transactions and add back to pool
        blockchain = Helper().get_blockchain()
        for block in blockchain:
            if block.validatedByUser[-1] == username and not block.isValidBlock[-1]:
                for transaction in block.data:
                    if not transaction.is_valid():
                        transaction.add_status(False)

                for transactions in block.data:
                    file2 = open(self.path_pool, "ab+")
                    pickle.dump(transactions, file2)