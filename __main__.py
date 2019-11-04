from functools import reduce

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
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    tx_open_sender = [[tx['amount'] for tx in open_transactions if tx['sender'] == participant]]

    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    amount_sent =\
        reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_open_sender, amount_sent)

    tx_recipient =\
        [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]

    amount_received =\
        reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received - amount_sent


def get_last_blockchain_item():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balances(transaction['sender'])

    return sender_balance >= transaction['amount']


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


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

    copied_open_transactions = open_transactions[:]
    copied_open_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_open_transactions
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
    for (index, block) in enumerate(blockchain):
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
    print('5: Check transaction validity')
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
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('Transactions are invalid')
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

    print('User - {}, balance - {:.2f}'.format(owner, get_balances(owner)))

print('Quit')
