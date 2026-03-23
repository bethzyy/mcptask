#!/usr/bin/env python3
import json
import os

# Read messages.json
messages_path = "results/hard_v4/qwen3-5-plus__playwright/run-1/web_search__jasminum_nudiflorum_info/messages.json"

with open(messages_path, "r", encoding="utf-8") as f:
    messages = json.load(f)

print(f"Total messages: {len(messages)}")

# Check each message
for i, range(len(messages)):
    msg = messages[i]
    if msg.get("role") == "assistant":
        content = msg.get("content")
        status = msg.get("status")
        print(f"Msg {i}: role=assistant, status={status}")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text", "")
                    if "<answer>" in text:
                        print(f"  Found answer: {text[:200]}")
