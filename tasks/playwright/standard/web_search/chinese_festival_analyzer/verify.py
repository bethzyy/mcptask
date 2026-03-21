#!/usr/bin/env python3
"""
Verification script for Chain Dependency Task v88.
Simplified structure: 4 stages with geographic & historical constraints.

Chain: Festival → Poem (same festival) → Event (same poet)
Stages: 1, 2, 3, 4 (simplified from 13 sub-stages)
"""
import sys
import json
import os
import re
from pathlib import Path

# Stage 1: Festival with 5 conditions
STAGE1_CORRECT = {
    # Taste (NOT sweet) - correct answers
    "renri", "human day", "qicaigeng", "seven vegetable", "七菜羹",
    "shangsi", "double third", "bitter", "savory", "上巳节", "上巳",
    "medicinal", "health", "purification", "人日", "荠菜", "蒿子",
    # Symbolism
    "健康", "health", "净化", "purification", "驱邪",
    # Geographic (Jiangnan or North China Plain)
    "江南", "jiangnan", "华北", "north china", "中原", "central plain",
    "henan", "河南", "shandong", "山东", "hebei", "河北",
    # Historical (Pre-Tang)
    "唐代", "tang dynasty", "唐以前", "before tang",
    "han", "汉", "jin", "晋", "wei", "魏", "six dynasties", "六朝",
    "zhou", "周", "pre-tang", "tang之前",
}
STAGE1_WRONG = {
    "qingtuan", "yuanxiao", "mooncake",  # Sweet foods
    "zongzi", "duanwu", "dragon boat",  # Ambiguous
    "sweet", "甜", "红豆", "red bean", "芝麻", "sesame",  # Sweet indicators
}

# Stage 2: Poem about the festival with political frustration
STAGE2_CORRECT = {
    # For Shangsi festival poems
    "du fu", "dufu", "杜甫", "liren", "丽人行",
    # For Renri festival poems
    "renri", "人日", "人日两首",
    # Political frustration keywords
    "political", "frustration", "satire", "criticism", "讽刺", "政治",
    "demotion", "贬", "exile", "流放", "dismissed", "罢免",
}
STAGE2_WRONG = {
    "lost love", "romance", "beauty", "peach blossom",
    "homesick", "missing home", "nostalgia", "思乡",
}

# Stage 3: Political demotion of the poet from Stage 2
STAGE3_CORRECT = {
    # For Du Fu
    "755", "756", "757", "758", "an lushan", "rebellion",
    "huazhou", "华州", "司功参军",
    # For Bai Juyi
    "815", "bai juyi", "白居易", "jiangzhou", "江州",
    # For Xin Qiji
    "1181", "forced resign",
    # General demotion keywords
    "demoted", "exile", "banished", "贬谪", "贬官", "demotion",
}
STAGE3_WRONG = {
    "rebellion was the", "war was the", "battle of",
    "death of", "died of", "illness caused",
}

# Stage tags that must be present (v88 has 4 stages)
STAGE_TAGS = ["stage1", "stage2", "stage3", "stage4"]

# Keyword groups for reasoning feature check (need 4/5)
KEYWORD_GROUPS = [
    # Group 1: Taste features
    ["咸", "savory", "苦", "bitter", "非甜", "not sweet", "药", "vegetable"],
    # Group 2: Appearance features
    ["绿色", "green", "青", "翠绿", "herb"],
    # Group 3: Symbolism features
    ["健康", "health", "净化", "purification", "驱邪", "spring"],
    # Group 4: Geographic features
    ["江南", "jiangnan", "华北", "north china", "中原", "central plain",
     "henan", "河南", "shandong", "山东"],
    # Group 5: Historical features
    ["唐代", "tang", "唐以前", "before tang", "han", "汉", "jin", "晋",
     "wei", "魏", "six dynasties", "六朝", "pre-tang", "zhou", "周"],
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
                            if i.get("type") == "text":
                                text_parts.append(i.get("text", ""))
                            elif i.get("type") == "output_text":
                                text_parts.append(i.get("text", ""))

        return {"ok": True, "text": " ".join(text_parts)}
    except Exception as e:
        print(f"| [ERROR] {e}")
        return {"ok": False, "text": ""}


def parse_answer(txt):
    result = {
        "stages": {},
        "substages": {},
        "full_answer": "",
        "chain": [],
        "citations": []
    }

    # Extract chain
    m = re.search(r"Chain:\s*(.+?)(?:\n|Stage 1:|$)", txt, re.IGNORECASE)
    if m:
        result["chain"] = m.group(1).strip()

    # Extract 4 main stages
    for i in range(1, 5):
        m = re.search(rf"<stage{i}>(.+?)</stage{i}>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            result["stages"][i] = m.group(1).strip()

    # Extract sub-stages (stage1a, stage1b, etc.)
    sub_counts = {1: 5, 2: 2, 3: 2, 4: 1}  # v89: sub-stage counts
    for stage in range(1, 5):
        for sub_idx in range(1, sub_counts.get(stage, 1) + 1):
            sub_letter = chr(ord('a') + sub_idx - 1)
            tag = f"stage{stage}{sub_letter}"
            m = re.search(rf"<{tag}>(.+?)</{tag}>", txt, re.DOTALL | re.IGNORECASE)
            if m:
                result["substages"][tag] = m.group(1).strip()
                # Also map to main stage if not already set
                if stage not in result["stages"]:
                    result["stages"][stage] = m.group(1).strip()

    # Extract final answer
    m = re.search(r"<answer>(.+?)</answer>", txt, re.DOTALL | re.IGNORECASE)
    if m:
        result["full_answer"] = m.group(1).strip()

    # Extract citations (URLs)
    url_pattern = r'https?://[^\s<>"\)\]]+'
    result["citations"].extend(re.findall(url_pattern, txt))

    return result


def check_stages(stages):
    """Check if all required stages are present."""
    found = []
    missing = []

    for tag_num in range(1, 5):
        if tag_num in stages and stages[tag_num].strip():
            found.append(f"stage{tag_num}")
        else:
            missing.append(f"stage{tag_num}")

    return found, missing


def check_citations(content, min_count=5):
    """Check if content has enough citations."""
    url_pattern = r'https?://[^\s<>"\)\]]+'
    citations = re.findall(url_pattern, content)
    return len(citations) >= min_count, citations


def check_content(content, correct_set, wrong_set):
    """Check if content has correct elements."""
    if not content:
        return False, "No content", [], []

    content_lower = content.lower()

    # Extract the "Festival:" line to check the actual answer
    # This avoids false positives from "Why other candidates failed" section
    festival_match = re.search(r'Festival:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if festival_match:
        festival_line = festival_match.group(1).lower()
        # Check wrong elements ONLY in the festival selection line
        wrong_found = [w for w in wrong_set if w in festival_line]
        if wrong_found:
            return False, "WRONG answer detected", [], wrong_found

    # Check correct elements in full content
    correct_found = [c for c in correct_set if c in content_lower or c in content]

    if len(correct_found) >= 2:
        return True, "Correct", correct_found, []

    return False, "Missing key elements", correct_found, []


def check_reasoning_features(reasoning):
    """Check if reasoning contains features from at least 4/5 keyword groups."""
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
    min_required = 4

    if score >= min_required:
        return score, found_keywords, f"PASSED ({score}/5 groups)"
    else:
        return score, found_keywords, f"FAILED ({score}/5 groups, need {min_required})"


def verify_chain_dependency(stages):
    """Verify that stages form a valid chain."""
    issues = []

    if 1 in stages and 2 in stages:
        s1 = stages[1].lower()
        s2 = stages[2].lower()

        # Extract the actual festival from the "Festival:" line only
        festival_match = re.search(r'festival:\s*(.+?)(?:\n|$)', s1, re.IGNORECASE)
        if festival_match:
            festival_line = festival_match.group(1)

            # Check if festival is Shangsi
            if "shangsi" in festival_line or "double third" in festival_line or "上巳" in festival_line:
                if "shangsi" not in s2 and "liren" not in s2 and "丽人行" not in s2 and "上巳" not in s2:
                    issues.append("Stage 2 poem doesn't match Stage 1 festival (Shangsi)")

            # Check if festival is Renri
            elif "renri" in festival_line or "human day" in festival_line or "人日" in festival_line:
                if "renri" not in s2 and "人日" not in s2:
                    issues.append("Stage 2 poem doesn't match Stage 1 festival (Renri)")

    if 2 in stages and 3 in stages:
        s2 = stages[2].lower()
        s3 = stages[3].lower()

        poet = None
        if "du fu" in s2 or "dufu" in s2 or "杜甫" in s2:
            poet = "du fu"
        elif "xin qiji" in s2 or "辛弃疾" in s2:
            poet = "xin qiji"
        elif "su shi" in s2 or "苏轼" in s2:
            poet = "su shi"

        if poet and poet not in s3:
            issues.append(f"Stage 3 event doesn't match Stage 2 poet ({poet})")

    return issues


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chain Dependency Task (v88)")
    print("| Simplified 4-Stage Structure with Geographic & Historical Constraints")
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

    # === STAGE CHECK ===
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
    print("| Required: At least 4/5 keyword groups in reasoning")

    feature_score, found_keywords, feature_msg = check_reasoning_features(msgs["text"])

    print(f"| {feature_msg}")
    print(f"| Found keywords: {found_keywords[:10]}")

    if feature_score < 4:
        print(f"| [FAILED] Need features from 4/5 groups, got {feature_score}/5")
        ok = False
    else:
        print(f"| [PASSED] Features from {feature_score}/5 groups found")

    # === STAGE 1 ===
    print("| " + "-" * 68)
    print("| === STAGE 1: Festival Puzzle (5 Conditions) ===")
    print("|    1. Appearance: Green")
    print("|    2. Taste: NOT sweet (savory or bitter)")
    print("|    3. Symbolism: Health or purification")
    print("|    4. Geographic: Jiangnan OR North China Plain")
    print("|    5. Historical: Before Tang Dynasty (618 CE)")
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
    print("| === STAGE 2: Poem Puzzle ===")
    print("|    Correct: Poem about Stage 1 festival with political frustration")

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
    print("|    Correct: Demotion of Stage 2 poet")

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
        print("| Valid chain: Festival → Poem → Event")
        print("| All 4 stages completed")
        print("| All 5 conditions verified")
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
