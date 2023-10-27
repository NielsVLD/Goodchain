from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import random
from Helper import *

REWARD_VALUE = 50
leading_zeros = 2
next_char_limit = 20
isValidBlock = None
validatedByUser = None
validBlock = None

class TxBlock (CBlock):

    def __init__(self, previousBlock):
        self.nonce = "A random nonce"
        self.isValidBlock = []
        self.validatedByUser = []
        self.validBlock = False
        self.createdBy = ""
        super(TxBlock, self).__init__([], previousBlock)

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                total_in = total_in + amt
            for addr, amt in tx.outputs:
                total_out = total_out + amt
        return total_in, total_out
    
    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        
        total_in, total_out = self.__count_totals()
        
        Tx_Balance = round(total_out - total_in, 10)
        
        if  Tx_Balance > REWARD_VALUE:
            return False
        return True

    def good_nonce(self):
        return False

    def find_nonce(self):
        return None

        
    def mine_block(self, username):
        try:
            start_time = time.time()
            target_time = round(random.uniform(10.33, 19.66), 2)
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(bytes(str(self.data), 'utf8'))
            digest.update(bytes(str(self.previousHash), 'utf8'))

            found = False
            nonce = 0
            while not found:
                temp = digest.copy()
                temp.update(bytes(str(nonce), 'utf8'))
                hash = temp.finalize()
                zeros = bytes('0' * leading_zeros, 'utf8')
                elapsed_time = time.time() - start_time
                if elapsed_time < target_time:
                    zeros = bytes('0' * (leading_zeros + 1), 'utf8')
                else:
                    zeros = bytes('0' * (leading_zeros - 1), 'utf8')
                if hash.startswith(zeros):
                    found = True
                    self.nonce = nonce
                nonce += 1
                del temp
                print(f'trying nonce: {nonce}', end='\r')

            self.blockHash = self.computeHash()
            self.createdBy = username
            return True
        except:
            return False