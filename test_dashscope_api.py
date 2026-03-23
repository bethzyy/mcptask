#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 DashScope API Key 是否有效
"""

import os
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv

# 加载环境变量（强制覆盖系统环境变量）
load_dotenv(dotenv_path=".mcp_env", override=True)

# 获取配置
api_key = os.getenv("DASHSCOPE_API_KEY")
base_url = os.getenv("DASHSCOPE_BASE_URL")

print("=" * 50)
print("DashScope API Key Test")
print("=" * 50)
print(f"API Key: {api_key[:10]}...{api_key[-10:] if api_key else 'None'}")
print(f"Base URL: {base_url}")
print("=" * 50)

# 方法1: 使用 OpenAI 兼容接口
print("\n[Method 1] Using OpenAI compatible API...")
try:
    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=50,
    )

    print("[SUCCESS]")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"[FAILED] {e}")

# 方法2: 直接 HTTP 请求
print("\n[Method 2] Direct HTTP request...")
try:
    import requests
    import json

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "qwen3.5-plus",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 50,
    }

    response = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json=data,
        timeout=30,
    )

    print(f"HTTP Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("[SUCCESS]")
        print(f"Response: {result['choices'][0]['message']['content']}")
    else:
        print("[FAILED]")
        print(f"Error: {response.text}")
except Exception as e:
    print(f"[FAILED] {e}")

# 方法3: 测试原生 DashScope API
print("\n[Method 3] Native DashScope API...")
try:
    import requests

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 原生 DashScope API 端点
    native_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    data = {
        "model": "qwen-plus",
        "input": {
            "messages": [{"role": "user", "content": "Hello"}]
        },
        "parameters": {
            "max_tokens": 50
        }
    }

    response = requests.post(
        native_url,
        headers=headers,
        json=data,
        timeout=30,
    )

    print(f"HTTP Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("[SUCCESS]")
        print(f"Response: {result}")
    else:
        print("[FAILED]")
        print(f"Error: {response.text}")
except Exception as e:
    print(f"[FAILED] {e}")

print("\n" + "=" * 50)
print("Test completed")
print("=" * 50)
