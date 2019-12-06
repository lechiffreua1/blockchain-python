import hashlib


def hash_sha256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(string):
    return hash_sha256(string.encode(encoding='utf_8'))
