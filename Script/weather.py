#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高德天气查询脚本（深圳龙岗区）
获取实时温度 + 未来 3 天预报
"""

import requests
import sys

# ================= 配置区域 =================
API_KEY = "your_api_key"          # 请替换为你的高德 Web 服务 Key
ADCODE = "440307"        # 深圳龙岗区
# ===========================================

# API 基础地址
BASE_URL = "https://restapi.amap.com/v3/weather/weatherInfo"


def get_current_temperature(session, api_key, adcode):
    """获取实时温度（extensions=base）"""
    params = {
        "city": adcode,
        "key": api_key,
        "extensions": "base"
    }
    try:
        resp = session.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # 实时天气数据在 lives[0] 中
        if data.get("status") == "1" and data.get("lives"):
            temp = data["lives"][0].get("temperature", "--")
            return temp
        else:
            return "--"
    except Exception as e:
        print(f"获取实时温度失败: {e}", file=sys.stderr)
        return "--"


def get_forecast(session, api_key, adcode):
    """获取未来多天预报（extensions=all）"""
    params = {
        "city": adcode,
        "key": api_key,
        "extensions": "all"
    }
    try:
        resp = session.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "1" and data.get("forecasts"):
            # 返回第一个 forecast 的 casts 列表（即预报数据）
            return data["forecasts"][0].get("casts", [])
        else:
            return []
    except Exception as e:
        print(f"获取预报数据失败: {e}", file=sys.stderr)
        return []


def format_date(date_str):
    """
    将 '2024-02-14' 转为 '2月14日'（去除前导零）
    """
    try:
        year, month, day = date_str.split("-")
        # 将字符串转为整数去除前导零，再转回字符串
        month = str(int(month))
        day = str(int(day))
        return f"{month}月{day}日"
    except Exception:
        return date_str


def format_weather(day_weather, night_weather):
    """生成天气描述：相同则只显示一个，否则“白天转晚上”"""
    if day_weather == night_weather:
        return day_weather
    else:
        return f"{day_weather}转{night_weather}"


def main():
    # 检查 API Key 是否已填写
    if not API_KEY or API_KEY in ("xxx", "你的高德Key"):
        print("错误: 请先在脚本中填入有效的高德 API Key。")
        sys.exit(1)

    session = requests.Session()

    # 步骤1：获取实时温度
    current_temp = get_current_temperature(session, API_KEY, ADCODE)
    print(f"龙岗区当前温度：{current_temp}℃")

    # 步骤2：获取预报数据
    forecasts = get_forecast(session, API_KEY, ADCODE)
    if not forecasts:
        print("未能获取到预报数据")
        sys.exit(1)

    # 步骤3：输出未来 3 天预报（取前 3 条）
    for i, cast in enumerate(forecasts[:3], start=1):
        date = cast.get("date", "")
        day_weather = cast.get("dayweather", "")
        night_weather = cast.get("nightweather", "")
        day_temp = cast.get("daytemp", "")    # 高温
        night_temp = cast.get("nighttemp", "") # 低温

        if not date or not day_temp or not night_temp:
            continue

        formatted_date = format_date(date)
        weather_str = format_weather(day_weather, night_weather)
        # 输出格式：📅日期：天气，低温~高温
        print(f"📅{formatted_date}：{weather_str}，{night_temp}℃~{day_temp}℃")


if __name__ == "__main__":
    main()
