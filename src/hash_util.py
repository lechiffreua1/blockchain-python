import hashlib
import json


def hash_sha256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    block_dict = block.__dict__.copy()
    block_dict['transactions'] = [tx.to_ordered_dict() for tx in block_dict['transactions']]

    return hash_sha256(json.dumps(block_dict, sort_keys=True).encode(encoding='utf_8'))
