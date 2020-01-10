from functools import reduce
import json
# import pickle

from block import Block
from transaction import Transaction

from utility.hash_util import hash_block
from utility.verification import Verification
from wallet import Wallet

MINING_REWARD = 10
MINING_SENDER = 'MINING'


class Blockchain:
    def __init__(self, hoisting_node_id):
        genesis_block = Block(index=0, previous_hash='', transactions=[], proof=100)

        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.hoisting_node = hoisting_node_id

        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, value):
        self.__chain = value

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('./blockchain.txt', mode='r') as f:
                file_content = f.readlines()

                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []

                for block in blockchain:
                    converted_tx = [
                        Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']
                    ]

                    updated_block = Block(
                        index=block['index'],
                        previous_hash=block['previous_hash'],
                        transactions=converted_tx,
                        proof=block['proof'],
                        timestamp=block['timestamp']
                    )

                    updated_blockchain.append(updated_block)

                self.__chain = updated_blockchain

                open_transactions = json.loads(file_content[1])
                updated_open_transactions = []

                for tx in open_transactions:
                    updated_tx = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])

                    updated_open_transactions.append(updated_tx)

                self.__open_transactions = updated_open_transactions
        except (IOError, IndexError):
            print('File not found!')
        finally:
            print('Finally')

    def save_data(self):
        with open('./blockchain.txt', mode='w') as f:
            converted_blockchain = [
                block.__dict__ for block in [
                    Block(
                        block_el.index,
                        block_el.previous_hash,
                        [tx.__dict__ for tx in block_el.transactions],
                        block_el.proof,
                        block_el.timestamp
                    ) for block_el in self.__chain]
            ]

            print(converted_blockchain)

            f.write(json.dumps(converted_blockchain))
            f.write('\n')

            converted_transactions = [tx.__dict__ for tx in self.__open_transactions]
            f.write(json.dumps(converted_transactions))

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof

    def get_balance(self):
        if self.hoisting_node is None:
            return None

        participant = self.hoisting_node

        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        tx_open_sender = [[tx.amount for tx in self.__open_transactions if tx.sender == participant]]

        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        amount_sent =\
            reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_open_sender, amount_sent)

        tx_recipient =\
            [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]

        amount_received =\
            reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

        return amount_received - amount_sent

    def get_last_blockchain_item(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        transaction = Transaction(sender, recipient, signature, amount)

        if self.hoisting_node is None:
            return False

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            return True
        return False

    def mine_block(self):
        if self.hoisting_node is None:
            return None

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)

        proof = self.proof_of_work()

        reward_transaction = Transaction(MINING_SENDER, self.hoisting_node, '', MINING_REWARD)

        copied_open_transactions = self.__open_transactions[:]

        for tx in copied_open_transactions:
            if not Wallet.verify_transaction(tx):
                return None

        copied_open_transactions.append(reward_transaction)

        block = Block(
            index=len(self.__chain),
            previous_hash=hashed_block,
            transactions=copied_open_transactions,
            proof=proof
        )

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        return block
