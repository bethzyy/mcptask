#!/usr/bin/env python3
"""
Test script for Zhipu AI Anthropic-compatible API.
"""

import os
import asyncio
from dotenv import load_dotenv
import litellm

# Load environment variables from .mcp_env
load_dotenv(dotenv_path=".mcp_env", override=True)

def test_zhipu_anthropic():
    """Test Zhipu AI Anthropic-compatible API call."""
    api_key = os.getenv("ZHIPU_API_KEY")
    base_url = os.getenv("ZHIPU_BASE_URL")

    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: NOT SET")
    print(f"Base URL: {base_url}")

    if not api_key:
        print("ERROR: ZHIPU_API_KEY not set")
        return False

    try:
        print("\nSending test request to Zhipu AI (Anthropic-compatible)...")

        response = litellm.completion(
            model="anthropic/glm-5",
            api_key=api_key,
            base_url=base_url,
            messages=[
                {"role": "user", "content": "Say 'Hello, Zhipu!' in Chinese."}
            ],
            max_tokens=50,
        )

        content = response.choices[0].message.content
        print(f"\nResponse: {content}")
        print("\nSUCCESS: Zhipu AI Anthropic-compatible API works!")
        return True

    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = test_zhipu_anthropic()
    exit(0 if success else 1)
