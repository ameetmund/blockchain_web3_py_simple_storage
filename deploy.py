# In order to compile the solidity using python we need to import the following
# packages from py-solc-x (pip install py-solc-x).
# Please import both compile_standard and install_solc
from solcx import compile_standard, install_solc

# In order to generate abi's
import json

# Import web3 to interact with web3 components. Please ensure that 'pip install web3'
# is done before the code is executed in python environment
from web3 import Web3

# For using environment variables
import os

# python library to load the environemt variables. Please do 'pip install python-dotenv'
# before this being used
from dotenv import load_dotenv

# load_dotenv will look for env file in this script and automatically loads it
load_dotenv()

# In this part we are using a solidity code for usage
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile solidity code using python. It's very important that install_solc code with
# right version is present, else code will not work.
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

# This is take the compiled_sol variable and dump it into the file as a json object
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["Storage"]["evm"]["bytecode"][
    "object"
]

# abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["Storage"]["abi"]

# print(abi)

# Connecting to ganache through web3
# IMPORTANT - Please don't hard code the private key in the code. There are other
# ways to do it. But as long as it's a fake key, it's fine. But for real world apps
# follow other ways to use private keys. This is only for testing purpose.
#
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
network_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = "b227aa55a9786185c36fbbe69170eb0b99b7d55ad6ac09b4234fdddcd4d1431c"
private_key = os.getenv("PRIVATE_KEY")
# print(private_key)

# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# Get the number of transaction blocks
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# Deploy a SimpleStorage contract
# Build Transaction --> Sign Transaction --> Send Transaction
# 1. Build Transaction
print("Deploying SimpleStorage Contract....")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": network_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2. Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send the signed transaction to block chain
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# 4. Wait for the transaction receipt confirmation. It's part of a good practice
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Deployed SimpleStorage Contract..... :-)")

# Working with SimpleStorage contract
# For that we need Contract address and contract ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# The following print statement will return -- > <Function retrieve() bound to ()>

# When making a transaction with a blockchain, we can interact with them in two
# ways.
#   1. Call - Simulate making the call and getting a return value. These don't make
#             a state change to the blockchain
#   2. Transact - Makes a state change for a blockchain
# print(simple_storage.functions.retrieve())
print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(7).call())

# Please ensure that nonce value is not same as earlier. That's why it's incremented by 1
print("Storing new value in SimpleStorage Contract....")
store_transaction = simple_storage.functions.store(7).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": network_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

sign_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

txn_hash_store = w3.eth.send_raw_transaction(sign_store_transaction.rawTransaction)
txn_receipt_store = w3.eth.wait_for_transaction_receipt(txn_hash_store)
# print(simple_storage.functions.retrieve().call())
print(
    f"Stored new value {simple_storage.functions.retrieve().call()} in SimpleStorage Contract...."
)


# We may opt out of using ganache gui and instead use ganache-cli. So for that following must
# be installed.
#   1. Check 'node --version'. If not present then install nodejs from nodejs.org. You
#      can download specific version of node. For this I have used 12.18.4 by using
#      the command 'nvm install 12.18.4'. You can use any other version by typing
#      command 'nvm use version'. For example 'nvm use 9' to use version 9.
#   2. Check 'yarn --version'. If not present then do 'npm install --global yarn'
#   3. Add ganache-cli by typing 'yarn global add ganache-cli'. If there is an error
#      durinig this installation then do the following -
#           - 'sudo apt remove cmdtest'
#           - 'sudo apt remove yarn'
#           - 'npm install -g yarn'
#           - 'yarn install'
#           - 'yarn global add ganache-cli'
#   4. Check the ganache version with 'ganache-cli --version'. Sometimes this doesn't work
#      In those cases, please do the following -
#           - 'npm install -g ganache-cli'
#           - 'ganache-cli --version'

# We can start ganache by 'ganache-cli -d'. -d option will ensure that everytime the accounts
# remain same. Update the http link in the code, as well as the accounts.
