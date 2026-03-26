#!/usr/bin/env python3
"""
Verification for Daoist Concept Task v15.
Correct answer: Ziran (自然) - Naturalness

v15 Changes:
- Quote Chapter 25 directly ("道法__X__")
- Require finding the Tao Te Ching page
- Require finding Chapter 25
- 4 conditions with textual evidence requirement
- Goal: Force navigation to Tao Te Ching chapter list

Key insight: "道法自然" (Dao follows ziran/nature) - Chapter 25
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct: Ziran (naturalness)
CORRECT = {
    "ziran", "tzu-jan", "zìrán", "nature", "naturalness",
    "spontaneity", "self-so", "of itself",
    # Chinese characters
    "自然", "zì rán", "zi ran"
}

# TRAP: Wu Wei (about action, not Dao's operation)
TRAP_WU_WEI = {
    "wu wei", "wuwei", "wú wéi", "non-action", "inaction"
}


def get_work_dir():
    p = os.getenv("MCP_MESSAGES")
    if p and Path(p).exists():
        return Path(p).parent
    return Path(".")


def parse_messages(wd):
    """Parse messages and extract text."""
    f = wd / "messages.json"
    if not f.exists():
        return {"ok": False, "text": ""}

    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"| [ERROR] Failed to parse messages.json: {e}")
        return {"ok": False, "text": ""}

    text_parts = []

    for m in data:
        try:
            if m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))
        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts)}


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Daoist Concept Task (v15)")
    print("|")
    print("| Chapter 25 Quote: 道法__X__")
    print("| The answer is what X represents")
    print("|")
    print("| Conditions:")
    print("|   1. Mentioned in Tao Te Ching Chapter 25")
    print("|   2. Describes how Dao operates (not human action)")
    print("|   3. NOT Wu Wei")
    print("|   4. Appears in chapters 1-10 AND 20-30")
    print("|")
    print("| Correct: Ziran (道法自然 - Dao follows nature)")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    answer = extract_tag(text, "answer")

    if not answer:
        print("| [FAILED] No <answer> tag found")
        print("|          Format: <answer>[concept]</answer>")
        print("=" * 70)
        return False

    answer_lower = answer.lower()
    print(f"| [INFO] Answer: {answer[:100]}")

    # Check for Wu Wei trap first
    for trap in TRAP_WU_WEI:
        if trap in answer_lower:
            print(f"| [FAILED] TRAP: Wu Wei selected")
            print(f"|          Wu Wei is about human action, not how Dao operates")
            print(f"|          Correct: Ziran (道法自然)")
            print("=" * 70)
            return False

    # Check correct answer
    found_correct = False
    for correct in CORRECT:
        if correct in answer_lower:
            found_correct = True
            break

    if found_correct:
        print("| [PASSED] Correct answer: Ziran")
        print("|          道法自然 (Dao follows nature)")
        print("=" * 70)
        print("| RESULT: SUCCESS")
        print("=" * 70)
        return True

    print("| [FAILED] Correct answer not found")
    print("|          Expected: Ziran")
    print("|          Hint: 道法__X__")
    print("=" * 70)
    return False


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
