from functools import reduce
from src.hash_util import hash_block, hash_sha256
import json
# import pickle

from src.block import Block
from src.transaction import Transaction

MINING_REWARD = 10
MINING_SENDER = 'MINING'

owner = 'Dima'
participants = {owner}


def load_data():
    global blockchain
    global open_transactions

    try:
        with open('./blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()

            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []

            for block in blockchain:
                converted_tx = [
                    Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']
                ]

                updated_block = Block(
                    index=block['index'],
                    previous_hash=block['previous_hash'],
                    transactions=converted_tx,
                    proof=block['proof'],
                    timestamp=block['timestamp']
                )

                updated_blockchain.append(updated_block)

            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            updated_open_transactions = []

            for tx in open_transactions:
                updated_tx = Transaction(tx['sender'], tx['recipient'], tx['amount'])

                updated_open_transactions.append(updated_tx)

            open_transactions = updated_open_transactions
    except (IOError, IndexError):
        print('File not found!')

        genesis_block = Block(index=0, previous_hash=hash_sha256(''.encode('utf_8')), transactions=[], proof=100)

        blockchain = [genesis_block]

        open_transactions = []
    finally:
        print('Finally')


load_data()


def save_data():
    with open('./blockchain.txt', mode='w') as f:
        converted_blockchain = [
            block.__dict__ for block in [
                Block(
                    block_el.index,
                    block_el.previous_hash,
                    [tx.__dict__ for tx in block_el.transactions],
                    block_el.proof,
                    block_el.timestamp
                ) for block_el in blockchain]
        ]

        f.write(json.dumps(converted_blockchain))
        f.write('\n')

        converted_transactions = [tx.__dict__ for tx in open_transactions]
        f.write(json.dumps(converted_transactions))

        # data_to_save = {
        #     'chain': blockchain,
        #     'ot': open_transactions
        # }
        #
        # f.write(pickle.dumps(data_to_save))


def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_sha256(guess)

    print(guess_hash)

    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def get_balances(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    tx_open_sender = [[tx.amount for tx in open_transactions if tx.sender == participant]]

    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    amount_sent =\
        reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_open_sender, amount_sent)

    tx_recipient =\
        [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]

    amount_received =\
        reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received - amount_sent


def get_last_blockchain_item():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balances(transaction.sender)

    return sender_balance >= transaction.amount


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = Transaction(sender, recipient, amount)

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()

        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    reward_transaction = Transaction(MINING_SENDER, owner, MINING_REWARD)

    copied_open_transactions = open_transactions[:]
    copied_open_transactions.append(reward_transaction)

    block = Block(
        index=len(blockchain),
        previous_hash=hashed_block,
        transactions=copied_open_transactions,
        proof=proof
    )

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
        print('Block: ' + str(block.__dict__))


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print('Proof not valid')

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
            save_data()

    elif user_choice == '3':
        print_blockchain_items()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('Transactions are invalid')

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
