from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from Transaction import Tx
from TxBlock import TxBlock
from userInterface import *
from pathlib import Path
import pathlib

if __name__ == "__main__":
    # Make files
    pathlib.Path('data').mkdir(parents=True, exist_ok=True)
    pathlib.Path('data/blockchain.dat').touch()
    pathlib.Path('data/pool.dat').touch()
    pathlib.Path('data/transactionHistory.dat').touch()
    pathlib.Path('data/userDatabase.db').touch()


    database = Database("userDatabase.db")
    database.check_migrations()
    database.close()

    #UserInterface().main_screen()
    UserInterface().logged_in_screen("niels")