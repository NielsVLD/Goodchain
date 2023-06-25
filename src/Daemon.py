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
        Helper().create_hash('data/blockchain.dat')

    def validate_pending_blocks_in_chain(self, username):
        blockchain = Helper().get_blockchain()
        print(blockchain)
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
                                print("Daemon validated a pending block true")
                            else:
                                block.isValidBlock.append(False)
                                block.validatedByUser.append(username)
                                print("Daemon validated a pending block false")
                        else:
                            print("not user")
                            print(foundUser)
                        if len(block.isValidBlock) != 0:
                            if block.isValidBlock[-1] and block.isValidBlock.count(True) == 3 and block.validBlock == False:
                                block.validBlock = True
                                self.create_mining_reward(block)

                            f1 = open(self.path_blockchain, 'rb+')
                            f1.seek(0)
                            f1.truncate()
                            f1.close()

                            file2 = open(self.path_blockchain, "ab+")
                            pickle.dump(block, file2)
                            file2.close()
        Helper().create_hash('data/blockchain.dat')


    def remove_invalid_block(self, username):
        # Remove transactions and add back to pool
        blockchain = Helper().get_blockchain()
        for block in blockchain:
            if block.validatedByUser != []:
                if not block.isValidBlock[-1] and block.isValidBlock.count(False) == 3:
                    for transaction in block.data:
                        if not transaction.is_valid():
                            transaction.add_status(False)
                            print("Daemon spotted a invalid transaction ")

                    for transaction in block.data:
                        if transaction.is_valid():
                            file2 = open(self.path_pool, "ab+")
                            pickle.dump(transaction, file2)
                else:
                    f1 = open(self.path_blockchain, 'rb+')
                    f1.seek(0)
                    f1.truncate()
                    file2 = open(self.path_blockchain, "ab+")
                    pickle.dump(block, file2)
                    Helper().create_hash('data/blockchain.dat')

    def create_mining_reward(self, block):
        receiver = block.createdBy
        amount = 50
        transaction_fee = 0
        Tx2 = transferCoins("system")
        
        reward_transaction = Tx2.create_transaction(receiver, amount, transaction_fee)
        Tx2.save_transaction_in_pool(reward_transaction)
        Helper().create_hash('data/pool.dat')