from data.BlockChain import *
from data.Signature import generate_keys, sign, verify
from data.Transaction import Tx
from data.TxBlock import TxBlock

if __name__ == "__main__":
    print("Welcome to Goodchain!")

        # Make a keys
    alex_prv, alex_pbc = generate_keys()
    mike_prv, mike_pbc = generate_keys()

        # Make block
    Tx1 = Tx()
    Tx1.add_input(alex_pbc, 5)
    Tx1.add_output(mike_pbc, 1)
    Tx1.sign(alex_prv)

        # Verify

    if Tx1.is_valid():
        print("valid block")
