#!/usr/bin/env python3
"""
Verification script for Chain Dependency Task v80.
Verifies TRUE CHAIN DEPENDENCY between stages.

Chain: Festival → Poem (same festival) → Event (same poet)
"""
import sys
import json
import os
import re
from pathlib import Path

# Stage 1: Festival with green, savory/bitter food
STAGE1_CORRECT = {
    "renri", "human day", "qicaigeng", "seven vegetable", "七菜羹",
    "shangsi", "double third", "bitter", "savory", "上巳节", "上巳",
    "medicinal", "health", "purification", "人日", "荠菜", "蒿子",
}
STAGE1_WRONG = {
    "qingtuan", "yuanxiao", "mooncake",  # Sweet foods
    "zongzi", "duanwu", "dragon boat",  # Ambiguous (can be sweet OR savory)
}

# Stage 2: Poem about the festival with political frustration
# Must match the festival from Stage 1
STAGE2_CORRECT = {
    # For Shangsi festival poems
    "du fu", "dufu", "杜甫", "liren", "丽人行",
    # For Renri festival poems
    "renri", "人日", "人日两首", "renri poetry",
    # For Qingming festival poems (trap - easy to find)
    "du mu", "清明", "杜牧",
    # Political frustration keywords
    "political", "frustration", "satire", "criticism", "讽刺", "政治",
}
STAGE2_WRONG = {
    "lost love", "romance", "beauty", "peach blossom",  # Personal emotions
    "homesick", "missing home", "nostalgia",  # Not political
}

# Stage 3: Political demotion of the poet from Stage 2
# Must match the poet from Stage 2
STAGE3_CORRECT = {
    # For Du Fu (Shangsi/Renri chain)
    "755", "756", "757", "758", "an lushan", "rebellion", "suffering",
    "huazhou", "华州", "demotion", "司功参军",
    # For Xin Qiji (Renri chain - if exists)
    "1181", "forced resign", "resignation",
    # For Lu You (Dragon Boat chain)
    "1164", "longxing", "隆兴",
    # General demotion keywords
    "demoted", "exile", "banished", "贬谪",
}
STAGE3_WRONG = {
    # Only flag if war/rebellion is the MAIN event
    "rebellion was the", "war was the", "battle of",
    # Personal tragedy
    "death of", "died of", "illness caused",
}


def get_work_dir():
    try:
        p = os.getenv("MCP_MESSAGES")
        if p and Path(p).exists():
            return Path(p).parent
        return Path(".")
    except Exception as e:
        print(f"| [ERROR] {e}")
        return Path(".")


def parse_msgs(wd):
    try:
        f = wd / "messages.json"
        if not f.exists():
            return {"ok": False, "text": ""}

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
                            # Handle both "text" and "output_text" types
                            if i.get("type") == "text":
                                text_parts.append(i.get("text", ""))
                            elif i.get("type") == "output_text":
                                # output_text might have content in different fields
                                text_parts.append(i.get("text", ""))

        return {"ok": True, "text": " ".join(text_parts)}
    except Exception as e:
        print(f"| [ERROR] {e}")
        return {"ok": False, "text": ""}


def parse_answer(txt):
    result = {"stages": {}, "full_answer": "", "chain": []}

    # Extract chain
    m = re.search(r"Chain:\s*(.+?)(?:\n|Stage 1:)", txt, re.IGNORECASE)
    if m:
        result["chain"] = m.group(1).strip()

    # Extract stages
    for i in range(1, 4):
        m = re.search(rf"<stage{i}>(.+?)</stage{i}>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            result["stages"][i] = m.group(1).strip()

    # Extract final answer
    m = re.search(r"<answer>(.+?)</answer>", txt, re.DOTALL | re.IGNORECASE)
    if m:
        result["full_answer"] = m.group(1).strip()

    return result


def check_content(content, correct_set, wrong_set):
    """Check if content has correct elements, returns (ok, msg, found)"""
    if not content:
        return False, "No content", [], []

    content_lower = content.lower()

    # Find wrong elements FIRST - these are hard failures
    wrong_found = [w for w in wrong_set if w in content_lower or w in content]

    # If wrong elements found, FAIL immediately
    if wrong_found:
        return False, "WRONG answer detected", [], wrong_found

    # Only check correct elements if no wrong elements
    # Check both lowercase and original content for Chinese keywords
    correct_found = [c for c in correct_set if c in content_lower or c in content]

    if len(correct_found) >= 2:
        return True, "Correct", correct_found, []

    return False, "Missing key elements", correct_found, []


def verify_chain_dependency(stages):
    """Verify that stages form a valid chain."""
    issues = []

    # Check Stage 1 → Stage 2 dependency
    if 1 in stages and 2 in stages:
        s1 = stages[1].lower()
        s2 = stages[2].lower()

        # If Stage 1 says Shangsi, Stage 2 should mention it
        if "shangsi" in s1 and "shangsi" not in s2 and "liren" not in s2:
            issues.append("Stage 2 poem doesn't match Stage 1 festival (Shangsi)")

        # If Stage 1 says Renri, Stage 2 should mention it
        if "renri" in s1 and "renri" not in s2 and "人日" not in s2:
            issues.append("Stage 2 poem doesn't match Stage 1 festival (Renri)")

    # Check Stage 2 → Stage 3 dependency
    if 2 in stages and 3 in stages:
        s2 = stages[2].lower()
        s3 = stages[3].lower()

        # Extract poet from Stage 2
        poet = None
        if "du fu" in s2 or "dufu" in s2:
            poet = "du fu"
        elif "xin qiji" in s2:
            poet = "xin qiji"
        elif "su shi" in s2:
            poet = "su shi"

        if poet and poet not in s3:
            issues.append(f"Stage 3 event doesn't match Stage 2 poet ({poet})")

    return issues


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chain Dependency Task (v80)")
    print("| Festival → Poem (same festival) → Event (same poet)")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    ans = parse_answer(msgs["text"])
    print(f"| Chain: {ans['chain'][:80] if ans['chain'] else 'Not found'}...")
    print("| " + "-" * 68)

    ok = True

    # === STAGE 1 ===
    print("| === STAGE 1: Festival Puzzle ===")
    print("|    Correct: Renri (savory) OR Shangsi (bitter)")
    print("|    Trap: Qingtuan/Yuanxiao are SWEET")

    stage1_content = ans["stages"].get(1, ans["full_answer"])
    s1_ok, s1_msg, s1_correct, s1_wrong = check_content(
        stage1_content, STAGE1_CORRECT, STAGE1_WRONG
    )

    if s1_ok:
        print(f"| [PASSED] {s1_msg}")
        print(f"|          Found: {s1_correct[:5]}")
    else:
        print(f"| [FAILED] {s1_msg}")
        if s1_wrong:
            print(f"|          Wrong elements: {s1_wrong[:5]}")
        ok = False

    # === STAGE 2 ===
    print("| === STAGE 2: Poem Puzzle (must match Stage 1 festival) ===")
    print("|    Correct: Poem about Stage 1 festival with political frustration")

    stage2_content = ans["stages"].get(2, ans["full_answer"])
    s2_ok, s2_msg, s2_correct, s2_wrong = check_content(
        stage2_content, STAGE2_CORRECT, STAGE2_WRONG
    )

    if s2_ok:
        print(f"| [PASSED] {s2_msg}")
        print(f"|          Found: {s2_correct[:5]}")
    else:
        print(f"| [FAILED] {s2_msg}")
        if s2_wrong:
            print(f"|          Wrong elements: {s2_wrong[:5]}")
        ok = False

    # === STAGE 3 ===
    print("| === STAGE 3: Historical Event (must match Stage 2 poet) ===")
    print("|    Correct: Demotion of Stage 2 poet")

    stage3_content = ans["stages"].get(3, ans["full_answer"])
    s3_ok, s3_msg, s3_correct, s3_wrong = check_content(
        stage3_content, STAGE3_CORRECT, STAGE3_WRONG
    )

    if s3_ok:
        print(f"| [PASSED] {s3_msg}")
        print(f"|          Found: {s3_correct[:5]}")
    else:
        print(f"| [FAILED] {s3_msg}")
        if s3_wrong:
            print(f"|          Wrong elements: {s3_wrong[:5]}")
        ok = False

    # === CHAIN DEPENDENCY CHECK ===
    print("| " + "-" * 68)
    print("| === CHAIN DEPENDENCY CHECK ===")

    chain_issues = verify_chain_dependency(ans["stages"])
    if chain_issues:
        print("| [FAILED] Chain dependency broken!")
        for issue in chain_issues:
            print(f"|          - {issue}")
        ok = False
    else:
        print("| [PASSED] Chain dependency intact")

    print("=" * 70)
    if ok:
        print("| RESULT: SUCCESS")
        print("|")
        print("| Valid chain: Festival → Poem → Event")
        print("=" * 70)
        return True
    else:
        print("| RESULT: FAILED")
        print("|")
        print("| Chain broken or wrong answers")
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
        sys.exit(1)


if __name__ == "__main__":
    main()
