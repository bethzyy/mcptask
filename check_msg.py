#!/usr/bin/env python3
import json

messages_path = "results/hard_v4/qwen3-5-plus__playwright/run-1/web_search__jasminum_nudiflorum_info/messages.json"

with open(messages_path, "r", encoding="utf-8") as f:
    messages = json.load(f)

print(f"Total messages: {len(messages)}")

# Find last 5 assistant messages
assistant_msgs = [(i, msg) for i, msg in enumerate(messages) if msg.get("role") == "assistant"]
print(f"Found {len(assistant_msgs)} assistant messages")

for idx, msg in assistant_msgs[-5:]:
    status = msg.get("status")
    content = msg.get("content")
    print(f"\n=== Message {idx} (status={status}) ===")
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                print(f"Content: {text[:500]}")
