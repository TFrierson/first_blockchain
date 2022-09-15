from blockchain import Blockchain
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create a blockchain
blockchain = Blockchain()       # This will also create our Genesis block


@app.route('/mine_block', methods=['GET'])       # http://127.0.0.1:5000/mine_block
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200


# Get the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'blockchain_valid': chain_valid}
    
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=3000)
    
