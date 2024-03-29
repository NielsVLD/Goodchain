from userActions.TransferCoins import *
class Daemon:

    path_pool = 'data/pool.dat'
    path_transactionHistory = 'data/transactionHistory.dat'
    path_blockchain = 'data/blockchain.dat'


    def remove_invalid_transactions_from_pool(self, username):
        sender_prv, sender_pbc = transferCoins(username).get_sender_credentials()
        transactions = []
        index = 0
        with open(self.path_pool, "rb") as file:
            try:
                while True:
                    data = pickle.load(file)
                    transactions.append(data)
            except EOFError:
                pass
        
        for transaction in transactions:
            for valid in transaction.isValidTx:
                if valid == False and transaction.inputs[0][0] == sender_pbc:
                    transactions.pop(index)
                    print("Daemon removed invalid transactions from pool\n")
            index += 1
        
        with open(self.path_pool, 'rb+') as f1:
            f1.seek(0)
            f1.truncate()

        for transaction in transactions:
            with open(self.path_pool, "ab+") as file2:
                pickle.dump(transaction, file2)
        Helper().create_hash('data/blockchain.dat')

    def validate_pending_blocks_in_chain(self, username):
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
                                self.create_mining_reward(block)   
                            with open(self.path_blockchain, 'rb+') as f1:
                                f1.seek(0)
                                f1.truncate()
                            for block in blockchain2:
                                with open(self.path_blockchain, "ab+") as file2:
                                    pickle.dump(block, file2)
        
        Helper().create_hash('data/blockchain.dat')
        server.send_blockchain_data()
        server.send_blockchain_tamper_data()


    def remove_invalid_block(self, username):
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
                            file2.close()
                else:
                    f1 = open(self.path_blockchain, 'rb+')
                    f1.seek(0)
                    f1.truncate()
                    f1.close()
                    file2 = open(self.path_blockchain, "ab+")
                    pickle.dump(block, file2)
                    file2.close()
                    Helper().create_hash('data/blockchain.dat')

    def create_mining_reward(self, block):
        receiver = block.createdBy
        amount = 50
        input_amt = 0
        output_amt = 0
        transaction_fee = 0
        Tx2 = transferCoins("system")

        for transaction in block.data:
            for addr, amt in transaction.inputs:
                input_amt += amt

            for addr, amt in transaction.outputs:
                output_amt += amt
        
        amount = amount + (input_amt - output_amt)

        reward_transaction = Tx2.create_transaction(receiver, amount, transaction_fee)
        Tx2.save_transaction_in_pool(reward_transaction)
        Helper().create_hash('data/pool.dat')
        server.send_pool_data()