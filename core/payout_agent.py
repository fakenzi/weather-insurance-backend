# # import sys
# # import os
# # import uuid
# # import time

# # # =========================
# # # 项目根目录
# # # =========================
# # sys.path.insert(
# #     0,
# #     os.path.dirname(
# #         os.path.dirname(
# #             os.path.abspath(__file__)
# #         )
# #     )
# # )

# # # =========================
# # # Imports
# # # =========================
# # from web3 import Web3
# # from eth_abi import encode

# # from circle.web3 import utils
# # from circle.web3 import developer_controlled_wallets

# # from config import settings
# # from core.weather_agent import get_rain
# # from utils.contract import contract


# # # =========================
# # # 全局变量
# # # =========================
# # client = None
# # tx_api = None
# # w3 = None


# # # =========================
# # # 初始化 Circle
# # # =========================
# # def init_circle():

# #     global client, tx_api, w3

# #     # 已初始化
# #     if client is not None:
# #         return

# #     print("🔄 初始化 Circle Client...")

# #     # Circle Client
# #     client = utils.init_developer_controlled_wallets_client(
# #         api_key=settings.CIRCLE_API_KEY,
# #         entity_secret=settings.ENTITY_SECRET
# #     )

# #     # Transaction API
# #     tx_api = developer_controlled_wallets.TransactionsApi(
# #         client
# #     )

# #     # Web3
# #     w3 = Web3(
# #         Web3.HTTPProvider(settings.RPC_URL)
# #     )

# #     # RPC 测试
# #     if w3.is_connected():

# #         print("✅ RPC 连接成功")

# #     else:

# #         print("❌ RPC 连接失败")

# #     print("✅ Circle Client 初始化完成")


# # # =========================
# # # 触发赔付
# # # =========================
# # def trigger_payout(
# #     policy_id: int,
# #     actual_rain: int
# # ):

# #     init_circle()

# #     print(
# #         f"\n🤖 Agent 调用合约"
# #         f" | Policy #{policy_id}"
# #         f" | Rain: {actual_rain}mm"
# #     )

# #     # triggerPayout(uint256,uint256)
# #     selector = Web3.keccak(
# #         text="triggerPayout(uint256,uint256)"
# #     )[:4]

# #     # ABI Encode
# #     args = encode(
# #         ["uint256", "uint256"],
# #         [policy_id, actual_rain]
# #     )

# #     calldata = "0x" + (selector + args).hex()

# #     print(f"📦 Calldata: {calldata}")

# #     # Circle 请求
# #     request = (
# #         developer_controlled_wallets
# #         .CreateContractExecutionTransactionForDeveloperRequest
# #         .from_dict({

# #             "idempotencyKey": str(uuid.uuid4()),

# #             "walletId": settings.AGENT_WALLET_ID,

# #             "contractAddress": settings.CONTRACT_ADDRESS,

# #             "callData": calldata,

# #             "feeLevel": "MEDIUM",

# #             "blockchain": settings.BLOCKCHAIN
# #         })
# #     )

# #     # 发送交易
# #     response = (
# #         tx_api
# #         .create_developer_transaction_contract_execution(
# #             create_contract_execution_transaction_for_developer_request=request
# #         )
# #     )

# #     data = response.model_dump()["data"]

# #     tx_id = data["id"]

# #     print("✅ 交易提交成功")
# #     print(f"🧾 Tx ID: {tx_id}")

# #     return tx_id


# # # =========================
# # # 自动扫描所有保单
# # # =========================
# # def run_agent():

# #     print("\n===================================")
# #     print("🔍 开始扫描链上 Policies")
# #     print("===================================")

# #     try:

# #         # 链上 policy 数量
# #         count = (
# #             contract
# #             .functions
# #             .policyCount()
# #             .call()
# #         )

# #         print(f"📦 当前 Policy 数量: {count}")

# #     except Exception as e:

# #         print("❌ 获取 Policy 数量失败")

# #         print(e)

# #         return

# #     # 没有保单
# #     if count == 0:

# #         print("⏳ 当前没有保单")

# #         return

# #     # 遍历 Policies
# #     for i in range(1, count + 1):

# #         print("\n-----------------------------------")
# #         print(f"📄 Policy #{i}")

# #         try:

# #             # 读取链上 Policy
# #             p = (
# #                 contract
# #                 .functions
# #                 .getPolicy(i)
# #                 .call()
# #             )

# #             user = p[0]

# #             city = p[1]

# #             threshold = p[2]

# #             payout_amount = p[3]

# #             premium_paid = p[4]

# #             active = p[5]

# #             paid = p[6]

# #             created_at = p[7]

# #             checked_at = p[8]

# #             print(f"👤 User: {user}")

# #             print(f"🏙️ City: {city}")

# #             print(f"🌧️ Threshold: {threshold} mm")

# #             print(f"💰 Payout: {payout_amount}")

# #             print(f"💵 Premium: {premium_paid}")

# #             print(f"✅ Active: {active}")

# #             print(f"🎯 Paid: {paid}")

# #             # 已结束
# #             if not active or paid:

# #                 print("⏭️ Policy 已结束，跳过")

# #                 continue

# #             # 获取天气
# #             rain = get_rain(city)

# #             # API 失败
# #             if rain < 0:

# #                 print("❌ 天气 API 获取失败")

# #                 continue

# #             print(f"🌦️ 当前雨量: {rain:.2f}mm")

# #             # 达到赔付条件
# #             if rain >= threshold:

# #                 print("🚨 达到赔付条件！")

# #                 tx_id = trigger_payout(
# #                     policy_id=i,
# #                     actual_rain=int(rain)
# #                 )

# #                 print(
# #                     f"🎉 已发送赔付交易"
# #                     f" | Tx ID: {tx_id}"
# #                 )

# #             else:

# #                 print(
# #                     f"⏳ 未达到赔付条件 "
# #                     f"({rain:.2f}mm < {threshold}mm)"
# #                 )

# #         except Exception as e:

# #             print(f"❌ Policy #{i} 检查失败")

# #             print(e)


# # # =========================
# # # 无限循环 Agent（可选）
# # # =========================
# # def start_loop(interval=3600):

# #     print("\n♾️ Agent Loop 已启动")

# #     print(f"⏱️ 检查间隔: {interval} 秒")

# #     while True:

# #         try:

# #             run_agent()

# #         except Exception as e:

# #             print("❌ Agent Loop 异常")

# #             print(e)

# #         print("\n😴 等待下一次检查...\n")

# #         time.sleep(interval)


# # # =========================
# # # 主程序
# # # =========================
# # if __name__ == "__main__":

# #     print("===================================")
# #     print("🌧️ Weather Insurance Agent 启动")
# #     print("===================================")

# #     # 单次运行
# #     run_agent()

# #     # 如果要开启循环：
# #     # start_loop(interval=3600)
# import logging
# from datetime import datetime, timezone
# import asyncio

# # ================== LOG ==================
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s"
# )
# logger = logging.getLogger(__name__)


# # ================== MOCK / 依赖接口（你替换成真实的） ==================
# class CircleClient:
#     async def payout(self, policy, rain_value):
#         await asyncio.sleep(1)  # 模拟链上延迟
#         return f"tx_{policy['id']}_{int(datetime.now().timestamp())}"


# circle_client = CircleClient()


# # ================== 状态机 ==================
# class PolicyStatus:
#     OPEN = "OPEN"
#     PROCESSING = "PROCESSING"
#     PAID = "PAID"
#     CLOSED = "CLOSED"


# # ================== 示例保单数据（你应替换 DB） ==================
# policies = [
#     {"id": 1, "city": "Tokyo", "threshold": 15.0, "status": PolicyStatus.OPEN},
#     {"id": 2, "city": "NewYork", "threshold": 20.0, "status": PolicyStatus.OPEN},
#     {"id": 3, "city": "Singapore", "threshold": 10.0, "status": PolicyStatus.OPEN},
# ]


# # ================== 气象 API（替换成你真实接口） ==================
# def get_rain(city: str) -> float:
#     mock_data = {
#         "Tokyo": 0.0,
#         "NewYork": 0.0,
#         "Singapore": 0.4
#     }
#     return mock_data.get(city, 0.0)


# # ================== 时间工具 ==================
# def get_today():
#     return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# # ================== 核心幂等判断 ==================
# def can_process(policy):
#     return policy["status"] == PolicyStatus.OPEN


# # ================== 原子状态更新 ==================
# def set_status(policy, status):
#     policy["status"] = status


# # ================== 赔付逻辑 ==================
# async def process_policy(policy):

#     # ❌ 幂等：已经处理过直接跳过
#     if not can_process(policy):
#         logger.info(f"⏭️ 跳过保单 #{policy['id']}（状态：{policy['status']}）")
#         return

#     city = policy["city"]
#     threshold = policy["threshold"]

#     # 🔒 锁定状态，防止重复执行
#     set_status(policy, PolicyStatus.PROCESSING)

#     logger.info(f"🔎 处理保单 #{policy['id']} [{city}] 阈值={threshold}")

#     try:
#         rain = get_rain(city)

#         logger.info(f"🌧️ {city} 今日雨量: {rain} mm")

#         # 🚨 赔付判断
#         if rain < threshold:
#             logger.info(f"⏳ 未达标，不赔付 #{policy['id']}")
#             set_status(policy, PolicyStatus.CLOSED)
#             return

#         logger.warning(f"🚨 触发赔付 #{policy['id']}")

#         # 💸 调用链上赔付
#         tx_id = await circle_client.payout(policy, rain)

#         # ✅ 成功
#         set_status(policy, PolicyStatus.PAID)

#         logger.info(f"✅ 赔付成功 #{policy['id']} TX={tx_id}")

#     except Exception as e:
#         # ❌ 回滚状态（防卡死）
#         set_status(policy, PolicyStatus.OPEN)
#         logger.error(f"❌ 赔付失败 #{policy['id']} err={e}")
#         raise


# # ================== 每日结算主流程 ==================
# async def payout_job():

#     logger.info("🌧️ 开始每日保险结算流程")
#     logger.info("=" * 60)

#     # 📌 冻结窗口（可选逻辑）
#     # 比如防止 23:59-00:01 数据波动
#     now_minute = datetime.now(timezone.utc).minute
#     if now_minute in [59, 0]:
#         logger.warning("⛔ 冻结窗口，跳过结算")
#         return

#     open_policies = [p for p in policies if p["status"] == PolicyStatus.OPEN]

#     logger.info(f"📋 待处理保单数量: {len(open_policies)}")

#     for policy in open_policies:
#         await process_policy(policy)

#     logger.info("=" * 60)
#     logger.info("🎉 每日结算完成")


# # ================== 入口 ==================
# if __name__ == "__main__":
#     asyncio.run(payout_job())
# import logging
# from datetime import datetime, timezone
# import asyncio

# # ================== LOG ==================
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s"
# )
# logger = logging.getLogger(__name__)


# # ================== 导入真实天气函数 ==================
# try:
#     from weather_agent import get_rain as fetch_real_rain
#     logger.info("✅ 成功导入真实天气函数")
# except:
#     logger.warning("⚠️ 未找到 weather_agent，使用模拟数据")
#     def fetch_real_rain(city_name: str = "Tokyo"):
#         return 0.0


# # ================== MOCK / 依赖接口 ==================
# class CircleClient:
#     async def payout(self, policy, rain_value):
#         await asyncio.sleep(2)  # 模拟链上延迟
#         return f"tx_{policy['id']}_{int(datetime.now().timestamp())}"


# circle_client = CircleClient()


# # ================== 状态机 ==================
# class PolicyStatus:
#     OPEN = "OPEN"
#     PROCESSING = "PROCESSING"
#     PAID = "PAID"
#     CLOSED = "CLOSED"


# # ================== 示例保单数据（后续改成数据库） ==================
# policies = [
#     {"id": 1, "city": "Tokyo", "threshold": 15.0, "status": PolicyStatus.OPEN},
#     {"id": 2, "city": "NewYork", "threshold": 20.0, "status": PolicyStatus.OPEN},
#     {"id": 3, "city": "Singapore", "threshold": 10.0, "status": PolicyStatus.OPEN},
# ]


# # ================== 赔付逻辑 ==================
# async def process_policy(policy):
#     if policy["status"] != PolicyStatus.OPEN:
#         logger.info(f"⏭️ 跳过保单 #{policy['id']}（状态：{policy['status']}）")
#         return

#     city = policy["city"]
#     threshold = policy["threshold"]

#     set_status(policy, PolicyStatus.PROCESSING)

#     logger.info(f"🔎 处理保单 #{policy['id']} [{city}] 阈值={threshold}mm")

#     try:
#         rain = fetch_real_rain(city)          # 使用真实天气

#         logger.info(f"🌧️ {city} 今日雨量: {rain:.2f} mm")

#         if rain < threshold:
#             logger.info(f"⏳ 未达标，不赔付 #{policy['id']}")
#             set_status(policy, PolicyStatus.CLOSED)
#             return

#         logger.warning(f"🚨 触发赔付 #{policy['id']} | 雨量 {rain:.2f}mm")

#         tx_id = await circle_client.payout(policy, rain)

#         set_status(policy, PolicyStatus.PAID)
#         logger.info(f"✅ 赔付成功 #{policy['id']} | TX={tx_id}")

#     except Exception as e:
#         set_status(policy, PolicyStatus.OPEN)
#         logger.error(f"❌ 赔付失败 #{policy['id']} | {e}")


# def set_status(policy, status):
#     policy["status"] = status


# # ================== 每日结算主流程 ==================
# async def payout_job():
#     logger.info("🌧️ 开始每日保险结算流程 (UTC)")
#     logger.info("=" * 60)

#     open_policies = [p for p in policies if p["status"] == PolicyStatus.OPEN]

#     logger.info(f"📋 待处理保单数量: {len(open_policies)}")

#     for policy in open_policies:
#         await process_policy(policy)

#     logger.info("=" * 60)
#     logger.info("🎉 每日结算完成\n")


# # ================== 定时运行（UTC 00:00 执行） ==================
# async def main():
#     logger.info("🕛 Agent 已启动 | 每日 UTC 00:00 执行结算")

#     while True:
#         now = datetime.now(timezone.utc)
#         if now.hour == 0 and now.minute < 5:        # UTC 凌晨 00:00~00:05 执行
#             await payout_job()
#             await asyncio.sleep(3600 * 23)          # 睡23小时
#         else:
#             await asyncio.sleep(60)                 # 每分钟检查一次


# if __name__ == "__main__":
#     asyncio.run(main())
import logging
from datetime import datetime, timezone, timedelta   # ← 这里加了 timedelta
import asyncio

# ================== LOG ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# ================== 真实天气调用 ==================
def get_rain(city: str) -> float:
    try:
        from weather_agent import get_rain as fetch_real_rain
        rain = fetch_real_rain(city)
        logger.info(f"🌧️ 从 weather_agent 获取 {city} 雨量: {rain:.2f} mm")
        return rain
    except Exception as e:
        logger.warning(f"⚠️ weather_agent 调用失败: {e}")
        return 0.0


# ================== Circle Client ==================
class CircleClient:
    async def payout(self, policy, rain_value):
        await asyncio.sleep(2)
        return f"tx_{policy['id']}_{int(datetime.now().timestamp())}"


circle_client = CircleClient()


# ================== 状态机 ==================
class PolicyStatus:
    OPEN = "OPEN"
    PROCESSING = "PROCESSING"
    PAID = "PAID"
    CLOSED = "CLOSED"


# ================== 示例保单数据 ==================
policies = [
    {"id": 1, "city": "Tokyo", "threshold": 15.0, "status": PolicyStatus.OPEN},
    {"id": 2, "city": "NewYork", "threshold": 20.0, "status": PolicyStatus.OPEN},
    {"id": 3, "city": "Singapore", "threshold": 10.0, "status": PolicyStatus.OPEN},
]


def set_status(policy, status):
    policy["status"] = status


# ================== 赔付逻辑 ==================
async def process_policy(policy):
    if policy["status"] != PolicyStatus.OPEN:
        return

    city = policy["city"]
    threshold = policy["threshold"]

    set_status(policy, PolicyStatus.PROCESSING)
    logger.info(f"🔎 处理保单 #{policy['id']} [{city}] 阈值={threshold}mm")

    try:
        rain = get_rain(city)

        if rain < threshold:
            logger.info(f"⏳ 未达标，不赔付 #{policy['id']} ({rain:.2f} < {threshold})")
            set_status(policy, PolicyStatus.CLOSED)
            return

        logger.warning(f"🚨 触发赔付 #{policy['id']} | 雨量 {rain:.2f}mm")

        tx_id = await circle_client.payout(policy, rain)
        set_status(policy, PolicyStatus.PAID)
        logger.info(f"✅ 赔付成功 #{policy['id']} | TX={tx_id}")

    except Exception as e:
        set_status(policy, PolicyStatus.OPEN)
        logger.error(f"❌ 赔付失败 #{policy['id']} | {e}")


# ================== 每日结算主流程 ==================
async def payout_job():
    logger.info("🌙 开始每日 UTC 00:00 保险结算")
    logger.info("=" * 70)

    open_policies = [p for p in policies if p["status"] == PolicyStatus.OPEN]
    logger.info(f"📋 今日待处理保单数量: {len(open_policies)}")

    for policy in open_policies:
        await process_policy(policy)

    logger.info("=" * 70)
    logger.info("🎉 今日结算完成\n")


# ================== 主循环 - 正式版 ==================
async def main():
    logger.info("🕛 Arc Weather Insurance Agent 已启动 | 正式模式（每日 UTC 00:00 执行）")

    while True:
        now = datetime.now(timezone.utc)

        if now.hour == 0 and now.minute < 5:           # UTC 00:00 ~ 00:05 执行
            await payout_job()
            logger.info("💤 今日结算完成，休眠至明天...")
            await asyncio.sleep(3600 * 23)
        else:
            next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            seconds_left = (next_day - now).total_seconds()
            logger.info(f"⏳ 距离下次结算还有 {int(seconds_left//3600)}小时 {int((seconds_left%3600)//60)}分钟")
            await asyncio.sleep(60)   # 每分钟检查一次


if __name__ == "__main__":
    asyncio.run(main())