from hash_util import hash_block, hash_sha256


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_sha256(guess)

        print(guess_hash)

        return guess_hash[0:2] == '00'

    @staticmethod
    def verify_transaction(transaction, get_balances):
        sender_balance = get_balances(transaction.sender)

        return sender_balance >= transaction.amount

    def verify_chain(self, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof not valid')

                return False

        return True

    def verify_transactions(self, open_transactions, get_balances):
        return all([self.verify_transaction(tx, get_balances) for tx in open_transactions])

