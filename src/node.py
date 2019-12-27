from flask import Flask, jsonify
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    blockchain.hoisting_node = wallet.public_key

    return '', 201


@app.route('/wallet', methods=['GET'])
def load_keys():
    wallet.load_keys()
    blockchain.hoisting_node = wallet.public_key

    return '', 204


@app.route('/mine', methods=['POST'])
def mine_block():
    mined_block = blockchain.mine_block()

    if mined_block is None:
        response = {
            'message': 'Adding a block failed',
            'is_wallet_set_up': wallet.public_key is not None
        }

        return jsonify(response), 500
    else:
        dict_block = mined_block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]

        response = {
            'message': 'Block has been successfully added',
            'block': dict_block
        }

        return response, 201


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [chain_item.__dict__.copy() for chain_item in chain_snapshot]

    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]

    return jsonify(dict_chain), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
