import json

from eth_account import Account
from web3 import Web3, contract

# 连接到以太坊节点
infura_url = "https://goerli.infura.io/v3/22b26b228b004ccc9325066db8b5c468"
w3 = Web3(Web3.HTTPProvider(infura_url))
Account.enable_unaudited_hdwallet_features()
acct, mnemonic = Account.create_with_mnemonic()
print(acct.address)
print(mnemonic)
print(acct == Account.from_mnemonic(mnemonic))

# 批量生成钱包
iterator = 0
for i in range(10):
    acct = Account.from_mnemonic(mnemonic,
        account_path=f"m/44'/60'/0'/0/{iterator}")
    iterator = iterator + 1
    print("第"+str(i)+"个钱包地址"+acct.address)


# 打印钱包账户私钥
print(acct.key.hex())
# 加密 JSON 用的密码
password = "password"

# 生成加密 JSON
encrypted_json = Account.encrypt(acct.key.hex(), password)
json_string = json.dumps(encrypted_json,indent=4)
print("钱包的加密 JSON：")
print(json_string)
# 解密 JSON 用的密码
password = "password"

# 将加密 JSON 转换为字符串
json_string = json.dumps(encrypted_json)

# 从加密 JSON 读取钱包
private_key = w3.eth.account.decrypt(json_string, password)

print("从加密 JSON 读取账户私钥：")
print(private_key.hex())

