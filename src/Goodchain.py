from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from Transaction import Tx
from TxBlock import TxBlock
from userInterface import *
from pathlib import Path
import pathlib
import pickle

if __name__ == "__main__":
    # Make files
    pathlib.Path('data').mkdir(parents=True, exist_ok=True)
    pathlib.Path('data/blockchain.dat').touch()
    pathlib.Path('data/pool.dat').touch()
    pathlib.Path('data/transactionHistory.dat').touch()
    pathlib.Path('data/userDatabase.db').touch()
    pathlib.Path('data/blockchainHash.txt').touch()
    pathlib.Path('data/poolHash.txt').touch()
    pathlib.Path('data/transactionHistory.txt').touch()


    # try:
    #     file = open('data/poolHash.txt', "rb+")
    #     storedPoolHash = pickle.load(file)
    # except:
    #     Helper().create_hash('data/pool.dat')
    # try:
    #     file = open('data/blockchainHash.txt', "rb+")
    #     storedBlockchainHash = pickle.load(file)
    # except:
    #     Helper().create_hash('data/blockchain.dat')

    f = open("data/blockchainHash.txt", "r")
    if f.read() == '':
        Helper().create_hash('data/blockchain.dat')


    # try:
    #     file = open('data/transactionHistory.txt', "rb+")
    #     storedPoolHash = pickle.load(file)
    #     file.close()
    # except:
    #     Helper().create_hash('data/transactionHistory.dat')

    database = Database("userDatabase.db")
    database.check_migrations()
    database.close()

    UserInterface().main_screen()