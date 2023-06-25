from Helper import Helper

class Validation:
    def validation_ui(self):
                print("\n1. Validate a block")
                print("2. Validate whole chain")


                try:
                    number = int(input("Which option do you want to choose?: "))
                    if number == 1:
                        self.validate_block_on_chain()
                    if number == 2:
                         self.validate_chain()
                    else:
                           print("Please choose one of the options:\n")
                except:
                    print("Please choose one of the options:\n")


    def validate_block_on_chain(self):
        blockchain = Helper().get_blockchain()
        if blockchain == []:
            print("Chain is empty")
        else:
            index = 1
            for block in blockchain:
                if block.validBlock:
                    if index == 1:
                        print(f"Genesis block {index} with ID: {block.blockId}")
                        print("\n")
                        index += 1
                    else:

                        print(f"Block {index} with ID: {block.blockId}")
                        print("\n")
                        index += 1
            while True:
                try:
                        total = 0
                        print(f"Total number of blocks = {index - 1}")
                        number = int(input("What block do you want to validate? Choose a number: "))
                        if number == 0:
                            print("Pick a number from the list")
                        else:
                            if blockchain[number-1].is_valid():
                                print(f"Block is valid\n")
                                break
                            else:
                                print(f"Block is valid\n")
                                break
                except:
                    print("Pick a number from the list")


    def validate_chain(self):
            blockchain = Helper().get_blockchain()
            if blockchain == []:
                print("Chain is empty")
            else:
                print(f"\nTotal blocks in chain is {len(blockchain)}.")
                x = 0
                for block in blockchain:
                    if block.is_valid():
                        print(f"Block with ID: {block.blockId} is valid.")
                    else:
                        print(f"Block with ID: {block.blockId} is invalid!")
                        x += 1
                if x != 0:
                    print("Chain is not valid!\n")

                    