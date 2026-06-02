# # from fastapi import APIRouter

# # from core.weather_agent import get_rain
# # from config import settings

# # # 创建 router
# # router = APIRouter()


# # # =========================
# # # 健康检查
# # # =========================
# # @router.get("/")
# # def health():

# #     return {
# #         "status": "ok",
# #         "service": "Weather Insurance API"
# #     }


# # # =========================
# # # 获取天气
# # # =========================
# # @router.get("/weather/{city}")
# # def weather(city: str):

# #     rain = get_rain(city)

# #     config = settings.get_city_config(city)

# #     threshold = config.get("threshold", 15)

# #     return {
# #         "city": city,
# #         "rain": rain,
# #         "threshold": threshold,
# #         "triggered": rain >= threshold
# #     }


# # # =========================
# # # 获取全部城市
# # # =========================
# # @router.get("/cities")
# # def get_cities():

# #     return {
# #         "cities": settings.get_all_cities()
# #     }
# from fastapi import APIRouter

# from core.weather_agent import get_rain
# from core.payout_agent import run_agent

# from config import settings
# from utils.contract import contract


# # =========================
# # Router
# # =========================
# router = APIRouter()


# # =========================
# # 健康检查
# # =========================
# @router.get("/")
# def health():

#     return {
#         "status": "ok",
#         "service": "Weather Insurance API"
#     }


# # =========================
# # 获取天气
# # =========================
# @router.get("/weather/{city}")
# def weather(city: str):

#     rain = get_rain(city)

#     config = settings.get_city_config(city)

#     threshold = config.get("threshold", 15)

#     return {
#         "city": city,
#         "rain": rain,
#         "threshold": threshold,
#         "triggered": rain >= threshold
#     }


# # =========================
# # 获取全部城市
# # =========================
# @router.get("/cities")
# def get_cities():

#     return {
#         "cities": settings.get_all_cities()
#     }


# # =========================
# # 获取全部 Policies
# # =========================
# @router.get("/policies")
# def get_policies():

#     policies = []

#     try:

#         count = (
#             contract
#             .functions
#             .policyCount()
#             .call()
#         )

#         for i in range(1, count + 1):

#             p = (
#                 contract
#                 .functions
#                 .getPolicy(i)
#                 .call()
#             )

#             policies.append({

#                 "policy_id": i,

#                 "user": p[0],

#                 "city": p[1],

#                 "threshold": p[2],

#                 "payout": p[3],

#                 "premium": p[4],

#                 "active": p[5],

#                 "paid": p[6],

#                 "created_at": p[7],

#                 "checked_at": p[8]
#             })

#         return {
#             "success": True,
#             "count": count,
#             "policies": policies
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "error": str(e)
#         }


# # =========================
# # 获取单个 Policy
# # =========================
# @router.get("/policy/{policy_id}")
# def get_policy(policy_id: int):

#     try:

#         p = (
#             contract
#             .functions
#             .getPolicy(policy_id)
#             .call()
#         )

#         return {

#             "success": True,

#             "policy_id": policy_id,

#             "user": p[0],

#             "city": p[1],

#             "threshold": p[2],

#             "payout": p[3],

#             "premium": p[4],

#             "active": p[5],

#             "paid": p[6],

#             "created_at": p[7],

#             "checked_at": p[8]
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "error": str(e)
#         }


# # =========================
# # 获取 Pool Balance
# # =========================
# @router.get("/pool-balance")
# def get_pool_balance():

#     try:

#         balance = (
#             contract
#             .functions
#             .getPoolBalance()
#             .call()
#         )

#         return {
#             "success": True,
#             "pool_balance": balance
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "error": str(e)
#         }


# # =========================
# # 手动运行 Agent
# # =========================
# @router.post("/run-agent")
# def run_weather_agent():

#     try:

#         run_agent()

#         return {
#             "success": True,
#             "message": "Agent executed successfully"
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "error": str(e)
#         }
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from core.weather_agent import get_rain

# =====================================================================
# 💡 终极修复：三重兼容导入
# 依次尝试导入可能存在的三种函数名，彻底解决由于命名不一致导致的 ImportError
# =====================================================================
try:
    from core.payout_agent import run_daily_settlement
except ImportError:
    try:
        from core.payout_agent import run_agent as run_daily_settlement
    except ImportError:
        # 如果前两个名字都没有，则强行绑定初始版本的同步/异步 payout_job 函数
        from core.payout_agent import payout_job as run_daily_settlement

from config import settings
from utils.contract import contract

logger = logging.getLogger("WeatherRoutes")
router = APIRouter()


# =========================
# 健康检查
# =========================
@router.get("/")
def health():
    return {
        "status": "ok",
        "service": "Weather Insurance API"
    }


# =========================
# 获取天气
# =========================
@router.get("/weather/{city}")
def weather(city: str):
    rain = get_rain(city)

    # 防御性拦截：如果天气 API 故障返回负数，直接报错，不给前端错误数据
    if rain < 0:
        raise HTTPException(status_code=502, detail=f"无法从气象服务获取城市 [{city}] 的真实雨量")

    config = settings.get_city_config(city)
    threshold = config.get("threshold", 15.0) if config else 15.0

    return {
        "city": city,
        "rain": rain,
        "threshold": threshold,
        "triggered": rain >= threshold
    }


# =========================
# 获取全部城市
# =========================
@router.get("/cities")
def get_cities():
    return {
        "cities": settings.get_all_cities()
    }


# =========================
# 获取全部 Policies
# =========================
@router.get("/policies")
def get_policies():
    policies = []

    try:
        count = contract.functions.policyCount().call()

        for i in range(1, count + 1):
            try:
                # 为单次链上读取加保护，防止单笔坏保单崩溃拖垮整个列表接口
                p = contract.functions.getPolicy(i).call()
                policies.append({
                    "policy_id": i,
                    "user": p[0],
                    "city": p[1],
                    "threshold": p[2],
                    "payout": p[3],
                    "premium": p[4],
                    "active": p[5],
                    "paid": p[6],
                    "created_at": p[7],
                    "checked_at": p[8]
                })
            except Exception as single_err:
                logger.error(f"❌ 链上保单 #{i} 解析失败，已跳过: {single_err}")
                continue

        return {
            "success": True,
            "count": count,
            "displayed_count": len(policies),
            "policies": policies
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"读取链上保单总数失败: {str(e)}"
        }


# =========================
# 获取单个 Policy
# =========================
@router.get("/policy/{policy_id}")
def get_policy(policy_id: int):
    try:
        p = contract.functions.getPolicy(policy_id).call()

        return {
            "success": True,
            "policy_id": policy_id,
            "user": p[0],
            "city": p[1],
            "threshold": p[2],
            "payout": p[3],
            "premium": p[4],
            "active": p[5],
            "paid": p[6],
            "created_at": p[7],
            "checked_at": p[8]
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"未找到保单 #{policy_id} 或链上查询失败: {str(e)}")


# =========================
# 获取 Pool Balance
# =========================
@router.get("/pool-balance")
def get_pool_balance():
    try:
        balance = contract.functions.getPoolBalance().call()
        return {
            "success": True,
            "pool_balance": balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取资金池余额失败: {str(e)}")


# =========================
# 手动运行 Agent (后台异步非阻塞版)
# =========================
@router.post("/run-agent")
def run_weather_agent(background_tasks: BackgroundTasks):
    """
    使用 BackgroundTasks：
    前端请求后立刻拿到响应，结算 Agent 会在后台安全、独立地运行，绝不阻塞服务。
    """
    try:
        # 将耗时较长的链上理赔轮询丢进 FastAPI 后台任务队列
        background_tasks.add_task(run_daily_settlement)

        return {
            "success": True,
            "status": "processing",
            "message": "保险结算流水已在后台异步启动，请观察服务器日志或稍后刷新保单列表查看结果。"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"无法启动后台结算任务: {str(e)}"
        }