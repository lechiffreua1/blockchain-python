genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

blockchain = [genesis_block]
open_tranactions = []

owner = 'Dima'


def get_last_blockchain_item():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(recipient, sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_tranactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = '-'.join([str(last_block[key]) for key in last_block])

    print(hashed_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_tranactions
    }

    blockchain.append(block)

    open_tranactions.clear()


def get_transaction_data():
    tx_recipient = input('Enter transaction recipient: ')
    tx_amount = float(input('Enter transaction amount: '))

    return tx_recipient, tx_amount


def get_user_choice():
    return input('Your choice: ')


def print_blockchain_items():
    for block in blockchain:
        print('Block: ' + str(block))


def verify_chain():
    is_valid = True

    for blockchain_index in range(len(blockchain)):
        if blockchain_index == 0:
            continue

        if blockchain[blockchain_index][0] != blockchain[blockchain_index - 1]:
            is_valid = False
            break

    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Make your choice: ')
    print('1: Add transaction')
    print('2: Mine block')
    print('3: Print blockchain blocks')
    print('h: Manipulate block')
    print('q: Quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_data()
        tx_recipient, tx_amount = tx_data
        add_value(tx_recipient, amount=tx_amount)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_items()
    elif user_choice == 'h':
        if len(blockchain) > 0:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Unknown')

    # if not verify_chain():
    #     print_blockchain_items()
    #
    #     print('Invalid blockchain')
    #
    #     break

print('Quit')
