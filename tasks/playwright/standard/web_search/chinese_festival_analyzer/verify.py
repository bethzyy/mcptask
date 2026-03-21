#!/usr/bin/env python3
"""
Verification script for v109 - Step-by-Step Output Required.
Requires 20+ documented turns, correct festival selection.
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct answers
CORRECT_KEYWORDS = {
    "shangsi", "double third", "shangsi festival", "上巳",
    "renri", "human day", "人日",
    "savory", "bitter", "咸", "苦", "herb", "not sweet",
    "健康", "health", "净化", "purification", "驱邪",
    "江南", "jiangnan", "华北", "north china",
    "han", "汉", "jin", "晋", "zhou", "周", "pre-tang",
    "du fu", "dufu", "杜甫", "bai juyi", "白居易",
    "gao shi", "高适",
}

# Trap keywords
WRONG_KEYWORDS = {
    "qingtuan", "yuanxiao", "mooncake", "red bean paste",
    "dragon boat", "duanwu", "zongzi", "qu yuan", "屈原",
    "suicide", "drowned", "投江", "278 bc", "miluo",
    "qingming festival", "清明节",
}

MIN_TURNS = 20


def get_work_dir():
    try:
        p = os.getenv("MCP_MESSAGES")
        if p and Path(p).exists():
            return Path(p).parent
        return Path(".")
    except Exception as e:
        print(f"| [ERROR] {e}")
        return Path(".")


def parse_messages(wd):
    try:
        f = wd / "messages.json"
        if not f.exists():
            return {"ok": False, "text": "", "raw": []}

        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)

        text_parts = []
        for m in data:
            if m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") == "text":
                                text_parts.append(i.get("text", ""))
                            elif i.get("type") == "output_text":
                                text_parts.append(i.get("text", ""))

        return {"ok": True, "text": " ".join(text_parts), "raw": data}
    except Exception as e:
        print(f"| [ERROR] {e}")
        return {"ok": False, "text": "", "raw": []}


def count_documented_turns(text):
    """Count documented turns in the output."""
    # Look for "=== TURN N ===" pattern
    turn_pattern = r'===\s*TURN\s+(\d+)\s*==='
    turns = re.findall(turn_pattern, text, re.IGNORECASE)
    if turns:
        return len(set(int(t) for t in turns))

    # Alternative: "Turn N:" pattern
    turn_pattern2 = r'Turn\s+(\d+):'
    turns2 = re.findall(turn_pattern2, text, re.IGNORECASE)
    if turns2:
        return len(set(int(t) for t in turns2))

    return 0


def count_actual_turns(raw_msgs):
    """Count actual assistant turns in messages."""
    count = 0
    for m in raw_msgs:
        if m.get("role") == "assistant":
            count += 1
    return count


def count_browser_actions(raw_msgs):
    """Count browser actions."""
    count = 0
    for m in raw_msgs:
        if m.get("role") == "assistant":
            content = m.get("content", "")
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        name = c.get("name", "")
                        if name.startswith("browser_"):
                            count += 1
    return count


def check_festival_selection(text):
    """Check if correct festival selected."""
    text_lower = text.lower()

    festival_patterns = [
        r'Festival:\s*(.+?)(?:\n|$)',
        r'Selected Festival:\s*(.+?)(?:\n|$)',
    ]

    for pattern in festival_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            festival_line = m.group(1).lower()

            for w in WRONG_KEYWORDS:
                if w in festival_line:
                    return False, f"Trap detected: {w}"

            for c in ["shangsi", "double third", "上巳", "renri", "human day", "人日"]:
                if c in festival_line:
                    return True, "Correct festival selected"

    return False, "No valid festival found"


def check_demotion_event(text):
    """Check for demotion (not suicide)."""
    text_lower = text.lower()

    suicide_indicators = ["suicide", "drowned", "投江", "278 bc", "miluo river"]
    for s in suicide_indicators:
        if s in text_lower:
            return False, f"Suicide detected: {s}"

    demotion_indicators = ["demoted", "exile", "banished", "贬谪", "demotion", "governor"]
    found = [d for d in demotion_indicators if d in text_lower]

    if found:
        return True, f"Demotion found: {found[:3]}"

    return False, "No demotion found"


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: v109 - Step-by-Step Output Required")
    print(f"| Requires: {MIN_TURNS}+ documented turns")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    raw = msgs["raw"]

    ok = True

    # === TURN COUNT CHECK ===
    print("| === TURN COUNT CHECK ===")
    print(f"| REQUIRED: {MIN_TURNS}+ turns")

    documented_turns = count_documented_turns(text)
    actual_turns = count_actual_turns(raw)
    browser_actions = count_browser_actions(raw)

    print(f"| Documented turns in output: {documented_turns}")
    print(f"| Actual assistant turns: {actual_turns}")
    print(f"| Browser actions: {browser_actions}")

    if documented_turns < MIN_TURNS and actual_turns < MIN_TURNS:
        print(f"| [FAILED] Only {max(documented_turns, actual_turns)} turns (need {MIN_TURNS}+)")
        ok = False
    else:
        print(f"| [PASSED] {max(documented_turns, actual_turns)} turns found")

    # === FESTIVAL CHECK ===
    print("| " + "-" * 68)
    print("| === FESTIVAL SELECTION CHECK ===")

    festival_ok, festival_msg = check_festival_selection(text)
    if festival_ok:
        print(f"| [PASSED] {festival_msg}")
    else:
        print(f"| [FAILED] {festival_msg}")
        ok = False

    # === DEMOTION CHECK ===
    print("| " + "-" * 68)
    print("| === DEMOTION EVENT CHECK ===")

    demotion_ok, demotion_msg = check_demotion_event(text)
    if demotion_ok:
        print(f"| [PASSED] {demotion_msg}")
    else:
        print(f"| [FAILED] {demotion_msg}")
        ok = False

    # === KEYWORD CHECK ===
    print("| " + "-" * 68)
    print("| === KEYWORD CHECK ===")

    correct_found = [k for k in CORRECT_KEYWORDS if k in text.lower()]
    wrong_found = [k for k in WRONG_KEYWORDS if k in text.lower()]

    print(f"| Correct: {len(correct_found)} - {correct_found[:5]}...")
    print(f"| Wrong: {len(wrong_found)} - {wrong_found[:5]}...")

    # === FINAL RESULT ===
    print("=" * 70)
    if ok:
        print("| RESULT: SUCCESS")
        print(f"| Turns: {max(documented_turns, actual_turns)}")
        print("=" * 70)
        return True
    else:
        print("| RESULT: FAILED")
        print("=" * 70)
        return False


def main():
    try:
        wd = get_work_dir()
        print(f"| Working dir: {wd}")
        result = verify(wd)
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"| [ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
