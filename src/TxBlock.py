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
        #user_pbc = 
        # for tx in self.data:
        #     for addr, amt in tx.inputs:
        #         if addr == user_pbc:
        #             total_in = total_in + amt
        #     for addr, amt in tx.outputs:
        #         if addr == user_pbc:
        #             total_out = total_out + amt
        # return total_in, total_out
    
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
    
    # def calculate_balance(self,input, output, user_pbc):
    #     if input and output == None:
    #         input = []
    #         output = []

    #     total_in, total_out = self.__count_totals(user_pbc)

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
        
    def mine_block(self, username):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))

        found = False
        nonce = 0
        while not found:
            digest_temp = digest.copy()
            digest_temp.update(bytes(str(nonce), 'utf8'))
            hash = digest_temp.finalize()
            zeros = bytes('0' * leading_zeros, 'utf8')
            if hash[:leading_zeros] == zeros:
                found = True
                self.nonce = nonce
            nonce += 1
            del digest_temp
            print(f'trying nonce: {nonce}', end='\r')

        self.blockHash = self.computeHash()
        self.createdBy = username
