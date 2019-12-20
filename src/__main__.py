from functools import reduce
from hash_util import hash_block
import json
# import pickle

from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10
MINING_SENDER = 'MINING'

owner = 'Dima'


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

        genesis_block = Block(index=0, previous_hash='', transactions=[], proof=100)

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


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not Verification.valid_proof(open_transactions, last_hash, proof):
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


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = Transaction(sender, recipient, amount)

    if Verification.verify_transaction(transaction, get_balances):
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


verification = Verification()



print('Quit')
