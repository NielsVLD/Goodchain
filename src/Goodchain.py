from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from Transaction import Tx
from TxBlock import TxBlock
from userInterface import *

if __name__ == "__main__":
    UserInterface().main_screen()