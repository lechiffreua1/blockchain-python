from blockchain import Blockchain

from utility.verification import Verification
from wallet import Wallet

owner = 'Test'


class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    @staticmethod
    def get_transaction_data():
        tx_recipient = input('Enter transaction recipient: ')
        tx_amount = float(input('Enter transaction amount: '))

        return tx_recipient, tx_amount

    @staticmethod
    def get_user_choice():
        return input('Your choice: ')

    def print_blockchain_items(self):
        for block in self.blockchain.chain:
            print('Block: ' + str(block))

    def list_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print('Make your choice: ')
            print('1: Add transaction')
            print('2: Mine block')
            print('3: Print blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')

            try:
                user_choice = self.get_user_choice()
            except KeyboardInterrupt:
                break

            if user_choice == '1':
                tx_data = self.get_transaction_data()
                recipient, amount = tx_data

                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)

                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Transaction added!')
                else:
                    print('Transaction failed')

                print(self.blockchain.get_open_transactions())

            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed! Got no wallet ?')

            elif user_choice == '3':
                self.print_blockchain_items()

            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balances):
                    print('All transactions are valid')
                else:
                    print('Transactions are invalid')

            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '7':
                self.wallet.save_keys()

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print('Unknown')

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_items()

                print('Invalid blockchain')

                break

            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balances()))


node = Node()
node.list_for_input()
