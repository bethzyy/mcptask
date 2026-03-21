#!/usr/bin/env python3
"""
Verification script for Treasure Hunt Task v105.
Wikipedia Link Chain Design - Must follow links, not search directly.

Chain: List of Festivals -> Festival -> Poet -> Event
"""
import sys
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

# Correct answers for Stage 1 (festival meeting all 6 conditions)
STAGE1_CORRECT = {
    # Shangsi Festival (Double Third Festival)
    "shangsi", "double third", "上巳", "三月三",
    # Renri (Human Day)
    "renri", "human day", "人日",
    # Taste (NOT sweet)
    "savory", "bitter", "咸", "苦", "herb", "vegetable",
    # Symbolism
    "健康", "health", "净化", "purification", "驱邪",
    # Geographic
    "江南", "jiangnan", "华北", "north china", "中原",
    # Historical (Pre-Tang)
    "han", "汉", "jin", "晋", "zhou", "周",
    # Poets
    "du fu", "dufu", "杜甫", "bai juyi", "白居易", "wang xizhi", "王羲之",
}

# Traps - Dragon Boat Festival (Qu Yuan suicide, not demotion)
STAGE1_WRONG = {
    # Sweet foods (traps)
    "qingtuan", "yuanxiao", "mooncake",
    "sweet", "甜", "red bean", "红豆",
    # Ambiguous foods
    "zongzi", "dragon boat", "duanwu",
    "qingming",
}

# Stage 2: Political frustration poems
STAGE2_CORRECT = {
    "political", "frustration", "satire", "criticism",
    "demotion", "贬", "exile", "流放", "dissatisfaction", "dissatisfied",
    "du fu", "杜甫", "bai juyi", "白居易", "du mu", "杜牧",
    "career", "failure", "poem", "poet", "governor",
}

STAGE2_WRONG = {
    "lost love", "romance", "beauty",
    "homesick", "missing home", "思乡",
}

# Stage 3: Demotion events
STAGE3_CORRECT = {
    "755", "756", "757", "815", "842",
    "demoted", "exile", "banished", "贬谪", "demotion",
    "governor", "prefecture", "prefectures", "appointment",
    "dissatisfied", "failure", "career",
}

STAGE3_WRONG = {
    # Qu Yuan's exile led to SUICIDE, not demotion
    "suicide", "drowned", "投江", "278 bc", "miluo river", "汨罗江",
    "committed suicide", "自沉", "drown",
}

# Keyword groups for reasoning feature check
KEYWORD_GROUPS = [
    ["咸", "savory", "苦", "bitter", "非甜"],
    ["绿色", "green", "青", "herb"],
    ["健康", "health", "净化", "purification"],
    ["江南", "jiangnan", "华北", "north china"],
    ["唐", "tang", "汉", "han", "晋", "jin", "周", "zhou"],
]

# Required starting URL
REQUIRED_START_URL = "en.wikipedia.org/wiki/List_of_festivals_in_China"

# Extraction patterns
EXTRACTION_PATTERNS = [
    (r'<stage(\d)>(.+?)</stage\d>', re.DOTALL | re.IGNORECASE),
    (r'### Stage (\d+): (.+?)(?:\n### |$)', re.DOTALL | re.IGNORECASE),
    (r'Stage (\d+):\s*(.+?)(?:\nStage \d+:|$)', re.DOTALL | re.IGNORECASE),
]


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


def parse_answer(txt):
    result = {
        "stages": {},
        "full_answer": "",
        "chain": [],
        "citations": [],
        "navigation_path": []
    }

    # Extract chain
    m = re.search(r"Chain:\s*(.+?)(?:\n|Stage 1:|$)", txt, re.IGNORECASE)
    if m:
        result["chain"] = m.group(1).strip()

    # Extract 4 main stages using multiple patterns
    # Pattern 1: XML tags
    for i in range(1, 5):
        m = re.search(rf"<stage{i}>(.+?)</stage{i}>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            result["stages"][i] = m.group(1).strip()

    # Pattern 2: Markdown headers
    if not result["stages"]:
        for i in range(1, 5):
            m = re.search(rf"### Stage {i}:\s*(.+?)(?:\n### |$)", txt, re.DOTALL | re.IGNORECASE)
            if m:
                result["stages"][i] = m.group(1).strip()

    # Pattern 3: Plain text headers
    if not result["stages"]:
        for i in range(1, 5):
            m = re.search(rf"Stage {i}:\s*(.+?)(?:\nStage \d+:|$)", txt, re.DOTALL | re.IGNORECASE)
            if m:
                result["stages"][i] = m.group(1).strip()

    # Extract final answer
    m = re.search(r"<answer>(.+?)</answer>", txt, re.DOTALL | re.IGNORECASE)
    if m:
        result["full_answer"] = m.group(1).strip()

    # Extract citations (URLs)
    url_pattern = r'https?://[^\s<>"\)\]]+'
    result["citations"].extend(re.findall(url_pattern, txt))

    # Extract navigation path from Stage 1
    if 1 in result["stages"]:
        s1 = result["stages"][1]
        path_urls = re.findall(r'https?://[^\s<>"\)\]]+', s1)
        result["navigation_path"] = path_urls

    return result


def check_link_chain_integrity(msgs_raw, ans):
    issues = []
    navigate_urls = []

    for m in msgs_raw:
        if m.get("role") == "assistant":
            content = m.get("content", "")
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        if c.get("name") == "browser_navigate":
                            args = c.get("input", {})
                            url = args.get("url", "")
                            if url:
                                navigate_urls.append(url)

    if navigate_urls:
        first_url = navigate_urls[0]
        if REQUIRED_START_URL not in first_url:
            issues.append(f"Did not start from required URL: {REQUIRED_START_URL}")

    if 1 in ans["stages"]:
        s1 = ans["stages"][1]
        if "Navigation Path" not in s1 and "navigation path" not in s1.lower():
            issues.append("Stage 1 missing navigation path documentation")

    return issues, navigate_urls


def check_stages(stages):
    found = []
    missing = []

    for tag_num in range(1, 5):
        if tag_num in stages and stages[tag_num].strip():
            found.append(f"stage{tag_num}")
        else:
            missing.append(f"stage{tag_num}")

    return found, missing


def check_citations(content, min_count=5):
    url_pattern = r'https?://[^\s<>"\)\]]+'
    citations = re.findall(url_pattern, content)
    return len(citations) >= min_count, citations


def check_content(content, correct_set, wrong_set):
    if not content:
        return False, "No content", [], []

    content_lower = content.lower()

    # Extract the "Festival:" line
    festival_match = re.search(r'Festival(?:\s+Found)?:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if festival_match:
        festival_line = festival_match.group(1).lower()
        wrong_found = [w for w in wrong_set if w in festival_line]
        if wrong_found:
            return False, "WRONG answer detected", [], wrong_found

    correct_found = [c for c in correct_set if c in content_lower or c in content]

    if len(correct_found) >= 3:
        return True, "Correct", correct_found, []

    return False, "Missing key elements", correct_found, []


def check_reasoning_features(reasoning):
    if not reasoning:
        return 0, [], "No reasoning content"

    reasoning_lower = reasoning.lower()
    found_groups = []
    found_keywords = []

    for i, group in enumerate(KEYWORD_GROUPS):
        for kw in group:
            if kw.lower() in reasoning_lower:
                found_groups.append(i)
                found_keywords.append(kw)
                break

    score = len(found_groups)
    min_required = 3

    if score >= min_required:
        return score, found_keywords, f"PASSED ({score}/5 groups)"
    else:
        return score, found_keywords, f"FAILED ({score}/5 groups, need {min_required})"


def verify_chain_dependency(stages):
    issues = []

    if 1 in stages and 2 in stages:
        s1 = stages[1].lower()
        s2 = stages[2].lower()

        # Check festival-poet connection
        if "shangsi" in s1 or "double third" in s1:
            if "du fu" not in s2 and "bai juyi" not in s2:
                issues.append("Stage 2 poet doesn't match Stage 1 festival (Shangsi)")

        elif "renri" in s1 or "human day" in s1:
            if "du fu" not in s2 and "gao shi" not in s2:
                issues.append("Stage 2 poet doesn't match Stage 1 festival (Renri)")

        # Dragon Boat is a trap - Qu Yuan's SUICIDE, not demotion
        elif "duanwu" in s1 or "dragon boat" in s1 or "zongzi" in s1:
            issues.append("Stage 1 chose trap festival (Dragon Boat - Qu Yuan's suicide, not demotion)")

        # Qingming is a trap - Qingtuan is SWEET
        elif "qingming" in s1 or "qingtuan" in s1:
            issues.append("Stage 1 chose trap festival (Qingming - Qingtuan is sweet)")

    if 2 in stages and 3 in stages:
        s2 = stages[2].lower()
        s3 = stages[3].lower()

        poet = None
        if "du fu" in s2 or "dufu" in s2:
            poet = "du fu"
        elif "bai juyi" in s2:
            poet = "bai juyi"
        elif "gao shi" in s2:
            poet = "gao shi"
        elif "qu yuan" in s2:
            poet = "qu yuan"

        if poet and poet not in s3:
            issues.append(f"Stage 3 event doesn't match Stage 2 poet ({poet})")

    return issues


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Treasure Hunt Task (v105)")
    print("| Wikipedia Link Chain - Must follow links, not search directly")
    print("| List of Festivals -> Festival -> Poet -> Event")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    ans = parse_answer(msgs["text"])
    print(f"| Chain: {ans['chain'][:80] if ans['chain'] else 'Not found'}...")
    print("| " + "-" * 68)

    ok = True

    # === LINK CHAIN INTEGRITY CHECK ===
    print("| === LINK CHAIN INTEGRITY CHECK ===")
    print(f"| Required starting URL: {REQUIRED_START_URL}")

    chain_issues, navigate_urls = check_link_chain_integrity(msgs["raw"], ans)
    if chain_issues:
        print("| [FAILED] Link chain issues:")
        for issue in chain_issues:
            print(f"|          - {issue}")
        ok = False
    else:
        print("| [PASSED] Link chain integrity intact")

    print(f"| Navigation URLs found: {len(navigate_urls)}")

    # === STAGE CHECK ===
    print("| " + "-" * 68)
    print("| === STAGE CHECK ===")
    print("| Required: 4 stages (1, 2, 3, 4)")

    found_stages, missing_stages = check_stages(ans["stages"])

    if missing_stages:
        print(f"| [FAILED] Missing stages: {missing_stages}")
        ok = False
    else:
        print(f"| [PASSED] All 4 stages found")

    print(f"| Found: {found_stages}")

    # === CITATION CHECK ===
    print("| " + "-" * 68)
    print("| === CITATION CHECK ===")
    print("| Required: At least 5 URLs cited")

    citation_ok, citations = check_citations(msgs["text"], min_count=5)

    if not citation_ok:
        print(f"| [FAILED] Only {len(citations)} citations found (need 5+)")
        ok = False
    else:
        print(f"| [PASSED] {len(citations)} citations found")

    # === REASONING FEATURE CHECK ===
    print("| " + "-" * 68)
    print("| === REASONING FEATURE CHECK ===")
    print("| Required: At least 3/5 keyword groups in reasoning")

    feature_score, found_keywords, feature_msg = check_reasoning_features(msgs["text"])

    print(f"| {feature_msg}")
    print(f"| Found keywords: {found_keywords[:10]}")

    if feature_score < 3:
        print(f"| [FAILED] Need features from 3/5 groups, got {feature_score}/5")
        ok = False
    else:
        print(f"| [PASSED] Features from {feature_score}/5 groups found")

    # === STAGE 1 ===
    print("| " + "-" * 68)
    print("| === STAGE 1: Festival Puzzle (6 Conditions) ===")
    print("|    Trap: Qingtuan/Yuanxiao are SWEET")

    stage1_content = ans["stages"].get(1, "")
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
    print("| === STAGE 2: Poem Puzzle ===")

    stage2_content = ans["stages"].get(2, "")
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
    print("| === STAGE 3: Historical Event ===")

    stage3_content = ans["stages"].get(3, "")
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
        print("| Valid chain: List of Festivals -> Festival -> Poet -> Event")
        print("| Link chain followed correctly")
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
        sys.exit(1)


if __name__ == "__main__":
    main()
