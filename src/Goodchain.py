from BlockChain import CBlock
import socket
import threading
import json
from Signature import generate_keys, sign, verify
from Transaction import Tx
from TxBlock import TxBlock
from userInterface import *
from pathlib import Path
import pathlib
import pickle
from P2P import server

if __name__ == "__main__":
    # start server
    
    # Make files
    pathlib.Path('data').mkdir(parents=True, exist_ok=True)
    pathlib.Path('data/blockchain.dat').touch()
    pathlib.Path('data/pool.dat').touch()
    pathlib.Path('data/transactionHistory.dat').touch()
    pathlib.Path('data/userDatabase.db').touch()
    pathlib.Path('data/blockchainHash.txt').touch()
    pathlib.Path('data/poolHash.txt').touch()
    pathlib.Path('data/transactionHistory.txt').touch()
    

    with open("data/blockchainHash.txt", "r") as f:
        if f.read() == '':
            Helper().create_hash('data/blockchain.dat')

    if not Helper().check_hash('data/blockchain.dat'):
            exit("Tampering with the blockchain detected!")
            
    database = Database("userDatabase.db")
    database.check_migrations()
    database.close()

    UserInterface().main_screen()