#!/usr/bin/env python3
import json

messages_path = r"results/hard_v4/qwen3-5-plus__playwright/run-1/web_search__jasminum_nudiflorum_info/messages.json"

print(f"Total messages: {len(messages)}")

# Find last assistant message with completed status
last_assistant_msg = None
for i in range(len(messages) - 1, -1, -1):
    msg = messages[i]
    if msg.get("role") == "assistant" and msg.get("status") == "completed":
        last_assistant_message = msg

if last_assistant_message is None:
    print("No completed assistant message found!")
else:
    content = last_assistant_message.get("content")
    print("\n=== Last Assistant Message ===")
    print(f"Status: {last_assistant_message.get('status')}")
    print(f"Content type: {type(content)}")

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                print(f"Text length: {len(text)}")
                print(f"Text preview: {text[:500]}")
                if "<answer>" in text:
                    print("\n*** FOUND ANSWER TAG! ***")
                    print(text)
    else:
        print("\nFull text:")
        print(text)
