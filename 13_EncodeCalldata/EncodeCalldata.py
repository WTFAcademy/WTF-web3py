# coding=utf-8
import json

from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3, contract

# 连接到以太坊节点
infura_url = "https://goerli.infura.io/v3/22b26b228b004ccc9325066db8b5c468"
w3 = Web3(Web3.HTTPProvider(infura_url))

# 判断连接是否成功
if w3.is_connected():
    print("连接成功！")
else:
    print("连接失败！")
# 创建钱包对象
private_key = "e08ca922fedbc3d37fa677f1d8f7e8fcbe42d031186bcbbc763d20cbdac81f9d"
wallet = Account.from_key(private_key)

w3.eth.default_account = wallet.address


# WETH合约地址（Goerli测试网）
addressWETH = '0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6'
addressWETH=w3.to_checksum_address(addressWETH)
abiWETH = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs":[{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [], "name": "deposit", "outputs": [], "payable": True, "stateMutability": "payable", "type": "function"}
]
contract_instance = w3.eth.contract(address=addressWETH, abi=abiWETH)

# 编码查询余额调用数据
data= contract_instance.encodeABI(fn_name="balanceOf", args=[wallet.address])
print(f"编码结果: {data}")
# 创建查询交易
transaction = {
    "to": addressWETH,
    "data": data
}

# 发送交易并获取余额
balanceWETH_hex = w3.eth.call(transaction)
# 解码返回信息
balanceWETH = int.from_bytes(balanceWETH_hex, byteorder='big')
formatted_balance = w3.from_wei(balanceWETH, "ether")
print(f"存款前WETH持仓: {formatted_balance}")

# 编码余额转化调用数据
data_deposit= contract_instance.encodeABI(
    "deposit",
    []
)

# 获取发送者地址的交易序号
nonce = w3.eth.get_transaction_count(wallet.address)

# 创建交易
transaction_deposit= {
    'to': addressWETH,
    'data': data_deposit,
    'value': w3.to_wei(0.001, 'ether'),
    'gas': 28312,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce  # 添加 nonce 字段
}
# 估算交易gas
# gas=w3.eth.estimate_gas(transaction_deposit)
# print(gas)
# 发起交易
signed_txn = w3.eth.account.sign_transaction(transaction_deposit, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# 等待交易上链
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# 获取交易详情
print("交易详情：")
print(tx_receipt)


# 查询存款后的 WETH 持仓

# 发送交易并获取余额
balanceWETH_hex = w3.eth.call(transaction)
# 解码返回信息
balanceWETH = int.from_bytes(balanceWETH_hex, byteorder='big')
formatted_balance = w3.from_wei(balanceWETH, "ether")
print(f"存款后WETH持仓: {formatted_balance}")

