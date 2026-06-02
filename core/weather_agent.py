import requests
import os
from typing import Dict

# 🌐 线上部署绑定的商业级气象密钥
WEATHER_API_KEY = "278bce63de514759944125901262605"
def get_rain(city_name: str = "Tokyo") -> float:
    
    # 线上生产环境城市及阀值配置（经纬度用于高精度气象定位）
    cities = {
        "tokyo": {"lat": 35.6895, "lon": 139.6917, "name_cn": "东京", "threshold": 15.0},
        "newyork": {"lat": 40.7128, "lon": -74.0060, "name_cn": "纽约", "threshold": 20.0},
        "singapore": {"lat": 1.3521, "lon": 103.8198, "name_cn": "新加坡", "threshold": 10.0},
    }

    
    cleaned_name = city_name.replace(" ", "").lower()
    config = cities.get(cleaned_name)
    
    if not config:
        print(f"❌ [生产警告] 未找到支持的城市配置: {city_name}")
        return -1.0

    url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={config['lat']},{config['lon']}&days=1&aqi=no&alerts=no"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        # 提取目标城市当天 00:00 至 23:59 的累计总降雨量 (mm)
        rain = float(data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"])
        print(f"📡 [气象源成功] {config['name_cn']} ({city_name}) 当日累计雨量: {rain:.2f} mm")
        return rain

    except Exception as e:
        print(f"💥 [生产错误] 气象服务请求失败或解析异常: {e}")
        return -1.0


def check_rain_and_decide(city_name: str = "Tokyo") -> Dict:
    """
    线上理赔核验核心：判定实际雨量是否达到或超过智能合约规定的起赔阀值
    """
    cleaned_name = city_name.replace(" ", "").lower()
    cities = {
        "tokyo": {"threshold": 15.0, "name_cn": "东京"},
        "newyork": {"threshold": 20.0, "name_cn": "纽约"},
        "singapore": {"threshold": 10.0, "name_cn": "新加坡"},
    }
    
    config = cities.get(cleaned_name)
    if not config:
        return {"city": city_name, "rain": -1.0, "should_payout": False}

    # 执行核心天气获取
    rain = get_rain(city_name)
    
    # 拦截任何不正常的负数雨量，保护资金池免受接口故障影响
    if rain < 0:
        print(f"🛑 [理赔拦截] 由于 {city_name} 气象数据获取失败，本次理赔流水强制安全中止。")
        return {"city": city_name, "rain": rain, "should_payout": False}

    threshold = config["threshold"]
    should_payout = rain >= threshold

    print(f"⚖️  [理赔判定] 城市: {config['name_cn']} | 当前雨量: {rain:.2f}mm | 起赔阀值: {threshold:.1f}mm | 触发理赔: {'【是】' if should_payout else '【否】'}")
    
    return {
        "city": city_name,
        "rain": rain,
        "threshold": threshold,
        "should_payout": should_payout
    }