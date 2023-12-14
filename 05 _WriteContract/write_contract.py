from web3 import Web3
from eth_account import Account

bsc_test = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
print(bsc_test.is_connected())
private_key = "e08ca922fedbc3d37fa677f1d8f7e8fcbe42d031186bcbbc763d20cbdac81f9d"
# 创建钱包对象
wallet = Account.from_key(private_key)
# 定义钱包地址
address = wallet.address

contract_address_test = '0x2faf6cc1165e4d8a4aa28582c268d9a15f71ecb7'
# 获取合约地址
checksum_contract_address_test = Web3.to_checksum_address(contract_address_test)

contract_abi = [
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"},
    {

        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# 创建 ERC20 合约对象

contract_bbq = bsc_test.eth.contract(address=checksum_contract_address_test, abi=contract_abi)
info=contract_bbq.functions.symbol().call()
print(info)
balance_bbq = contract_bbq.functions.balanceOf(address).call()
balance_bbq = Web3.from_wei(balance_bbq, 'ether')

print('该账户bbqCoin：', balance_bbq)

# 指定转账目标地址和转账金额
recipient_address = '0x19AbF5261c1a8a7882Ba8bE2F554C17C5036E94C'
amount_in_ether = 100
# 指定转账参数
nonce = bsc_test.eth.get_transaction_count(address)
gas_price = bsc_test.eth.gas_price
gas_limit = 100000
tx = contract_bbq.functions.transfer(recipient_address, Web3.to_wei(amount_in_ether, 'ether')).build_transaction(
    {
        'from': address,
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas_limit
    })

# 使用钱包对象进行交易签名
signed_txn = wallet.sign_transaction(tx)

tx_hash = bsc_test.eth.send_raw_transaction(signed_txn.rawTransaction)

print('转账交易已经提交，交易哈希为：', tx_hash.hex())
balance_bbq = contract_bbq.functions.balanceOf(address).call()
balance_bbq = Web3.from_wei(balance_bbq, 'ether')

print('该账户转账后bbqCoin：', balance_bbq)
