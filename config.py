import os
import json
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class Settings:
    CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY")
    ENTITY_SECRET = os.getenv("ENTITY_SECRET")
    AGENT_WALLET_ID = os.getenv("AGENT_WALLET_ID")

    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    RPC_URL = "https://rpc.testnet.arc.network"
    BLOCKCHAIN = "ARC-TESTNET"

    DEFAULT_CITY = "Tokyo"
    TEST_USER_ADDRESS = os.getenv("TEST_USER_ADDRESS")

    CITIES: Dict[str, dict] = {}

    def __init__(self):
        self.CITIES = self.load_cities()

    def load_cities(self) -> Dict[str, dict]:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "cities.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                cities = json.load(f)
            print(f"✅ 已成功加载 {len(cities)} 个城市配置")
            return cities
        except Exception as e:
            print(f"❌ 加载 cities.json 失败: {e}")
            return {}

    def get_city_config(self, city: str) -> Optional[dict]:
        if not city or not self.CITIES:
            return self.CITIES.get(self.DEFAULT_CITY)

        city_lower = city.strip().lower()
        for name, config in self.CITIES.items():
            if name.lower() == city_lower:
                return config
        return self.CITIES.get(self.DEFAULT_CITY)

    def get_all_cities(self):
        return list(self.CITIES.keys())


settings = Settings()