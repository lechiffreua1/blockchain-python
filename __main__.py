MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

blockchain = [genesis_block]
open_transactions = []

owner = 'Dima'
participants = {owner}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balances(participant):
    amount_sent = 0
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    tx_open_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]

    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    for tx in tx_open_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    amount_received = 0
    tx_recipient =\
        [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]

    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]

    return amount_received - amount_sent


def get_last_blockchain_item():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balances(transaction['sender'])

    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    if verify_transaction(transaction):
        participants.add(recipient)
        participants.add(sender)

        open_transactions.append(transaction)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }

    open_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }

    blockchain.append(block)
    return True


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
    print(participants)
    for (index, block) in enumerate(blockchain):
        print('BLOCK', block)
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False

    return True


waiting_for_input = True

while waiting_for_input:
    print('Make your choice: ')
    print('1: Add transaction')
    print('2: Mine block')
    print('3: Print blockchain blocks')
    print('4: Print participants')
    print('h: Manipulate block')
    print('q: Quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_data()
        recipient, amount = tx_data

        add_transaction(recipient, amount=amount)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_items()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        if len(blockchain) > 0:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{
                    'sender': 'Test',
                    'recipient': 'Test',
                    'amount': 10
                }]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Unknown')

    if not verify_chain():
        print_blockchain_items()

        print('Invalid blockchain')

        break

    print('BALANCE - ', get_balances('Dima'))

print('Quit')
