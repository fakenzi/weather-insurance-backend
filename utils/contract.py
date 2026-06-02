import json
from web3 import Web3

from config import settings

# =========================
# Web3 初始化
# =========================
w3 = Web3(
    Web3.HTTPProvider(settings.RPC_URL)
)

# =========================
# 合约地址
# =========================
CONTRACT_ADDRESS = Web3.to_checksum_address(
    settings.CONTRACT_ADDRESS
)

# =========================
# 读取 ABI
# =========================
with open("abi/WeatherInsurance.json", "r") as f:
    ABI = json.load(f)

# =========================
# 合约实例
# =========================
contract = w3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=ABI
)

print("✅ Contract 初始化完成")