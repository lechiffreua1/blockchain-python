class Node:
    @staticmethod
    def get_transaction_data():
        tx_recipient = input('Enter transaction recipient: ')
        tx_amount = float(input('Enter transaction amount: '))

        return tx_recipient, tx_amount

    @staticmethod
    def get_user_choice():
        return input('Your choice: ')

    @staticmethod
    def print_blockchain_items(blockchain):
        for block in blockchain:
            print('Block: ' + str(block))

    def list_for_input(self, add_transaction):
        waiting_for_input = True

        while waiting_for_input:
            print('Make your choice: ')
            print('1: Add transaction')
            print('2: Mine block')
            print('3: Print blockchain blocks')
            print('4: Check transaction validity')
            print('q: Quit')

            user_choice = Node.get_user_choice()

            if user_choice == '1':
                tx_data = Node.get_transaction_data()
                recipient, amount = tx_data

                add_transaction(recipient, amount=amount)

            elif user_choice == '2':
                if mine_block():
                    open_transactions = []
                    save_data()

            elif user_choice == '3':
                print_blockchain_items()

            elif user_choice == '4':
                if verification.verify_transactions(open_transactions.copy(), get_balances):
                    print('All transactions are valid')
                else:
                    print('Transactions are invalid')

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print('Unknown')

            if not verification.verify_chain(blockchain.copy()):
                print_blockchain_items()

                print('Invalid blockchain')

                break

            print('User - {}, balance - {:.2f}'.format(owner, get_balances(owner)))