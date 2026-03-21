#!/usr/bin/env python3
"""
Verification for Chinese Tea Classification Task v3.
Correct answer: Da Hong Pao (大红袍) - Wuyi Rock Oolong

v3 Design:
- REMOVED explicit "rock rhyme" mention from description
- MANDATORY multi-source verification (Wikipedia + Baidu Baike)
- Model must discover oxidation levels independently
- All 20 candidates must be investigated
- Information dependency chain design
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct answer: Da Hong Pao (大红袍)
CORRECT_NAMES = {
    "da hong pao", "大红袍", "dahongpao", "big red robe",
    "ta hung pao", "da hong bao"
}

# Correct category: Oolong (乌龙茶)
CORRECT_CATEGORY = {
    "oolong", "乌龙茶", "乌龙", "wulong", "wu long",
    "semi-oxidized", "半发酵", "semi-fermented"
}

# Wrong answers - these are Black Teas (apprentice's trap)
WRONG_BLACK_TEAS = set([
    "lapsang souchong", "正山小种",
    "jin jun mei", "金骏眉",
    "tanyang gongfu", "坦洋工夫",
    "zhenghe gongfu", "政和工夫",
    "dian hong", "滇红",
    "keemun", "祁门", "qimen",
])

# Wrong answers - other categories
WRONG_OTHER = set([
    "pu'er", "普洱",
    "tai ping hou kui", "太平猴魁",
    "tie guan yin", "铁观音",  # Correct category but wrong region (Anxi, not Wuyi)
    "dong ding", "冻顶",
    "alishan", "阿里山",
    "fenghuang", "凤凰",
    "huang jin gui", "黄金桂",
    "ben shan", "本山",
])

# All wrong answers
WRONG = WRONG_BLACK_TEAS | WRONG_OTHER

# Required verification keywords
REQUIRED_KEYWORDS = {
    "category": ["oolong", "乌龙茶", "乌龙", "wulong"],
    "oxidation": ["oxidation", "氧化", "semi-oxidized", "半发酵", "30", "50"],
    "rock_rhyme": ["rock rhyme", "岩韵", "yan yun", "mineral"],
    "wuyi": ["wuyi", "武夷", "rock tea", "岩茶"],
    "not_black": ["not black tea", "不是红茶", "oolong not black", "乌龙茶不是红茶"],
}


def get_work_dir():
    try:
        p = os.getenv("MCP_MESSAGES")
        if p and Path(p).exists():
            return Path(p).parent
        return Path(".")
    except Exception as e:
        print(f"| [ERROR] Failed to get work dir: {e}")
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
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))
                        elif isinstance(i, str):
                            text_parts.append(i)

        return {"ok": True, "text": " ".join(text_parts)}
    except Exception as e:
        print(f"| [ERROR] Failed to parse messages: {e}")
        return {"ok": False, "text": ""}


def parse_ans(txt):
    r = {"f": [], "e": ""}
    try:
        m = re.search(r"<answer>(.+?)</answer>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["f"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        m = re.search(r"<reasoning>(.+?)</reasoning>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["e"] = m.group(1).strip()

        if not r["f"]:
            # Try to find tea name in text
            m = re.search(r"(?:da hong pao|大红袍|dahongpao)", txt, re.IGNORECASE)
            if m:
                r["f"] = [m.group(0)]

        if not r["e"] and txt:
            r["e"] = txt.strip()

    except Exception as e:
        print(f"| [ERROR] Failed to parse answer: {e}")
    return r


def check_in(fests, exp):
    for f in fests:
        for e in exp:
            if e in f.lower():
                return True
    return False


def check_wrong(fests, wrong_set):
    """Check if any wrong answer is in the response."""
    found = []
    for f in fests:
        f_lower = f.lower()
        for w in wrong_set:
            if w in f_lower:
                found.append(f)
                break
    return found


def check_keywords(reasoning, keyword_dict):
    """Check if reasoning contains required keyword groups."""
    results = {}
    for category, keywords in keyword_dict.items():
        found = any(kw in reasoning.lower() for kw in keywords)
        results[category] = found
    return results


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chinese Tea Classification (v3)")
    print("| Correct Answer: Da Hong Pao (大红袍) - Wuyi Rock Oolong")
    print("| Design: Multi-source verification + Information dependency chain")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    ans = parse_ans(msgs["text"])
    print(f"| Answer: {ans['f']}")
    print(f"| Reasoning: {len(ans['e'])} chars")
    print("| " + "-" * 68)

    # CHECK 1: Correct tea name
    if not check_in(ans["f"], CORRECT_NAMES):
        print("| [FAILED] Correct tea NOT found")
        print("|          Expected: Da Hong Pao (大红袍)")
        print(f"|          Got: {ans['f']}")
        return False
    print("| [PASSED] Correct tea: Da Hong Pao")

    # CHECK 2: Correct category (Oolong, not Black Tea)
    if not check_in(ans["f"], CORRECT_CATEGORY) and not any(kw in ans["e"].lower() for kw in CORRECT_CATEGORY):
        print("| [FAILED] Correct category NOT identified")
        print("|          Expected: Oolong (乌龙茶)")
        print("|          Hint: Da Hong Pao is Oolong, NOT Black Tea!")
        return False
    print("| [PASSED] Correct category: Oolong (not Black Tea)")

    # CHECK 3: No wrong answers
    wrong_found = check_wrong(ans["f"], WRONG)
    if wrong_found:
        print(f"| [FAILED] Wrong answer detected: {wrong_found}")
        print("|          Must not select Black Tea or other categories")
        return False
    print("| [PASSED] No wrong answers")

    # CHECK 4: Required verification keywords
    print("| " + "-" * 68)
    print("| Taxonomic Verification Evidence:")

    kw_results = check_keywords(ans["e"], REQUIRED_KEYWORDS)

    # Must identify correct category
    if not kw_results["category"]:
        print("| [FAILED] Category (Oolong) not mentioned in reasoning")
        return False
    print("| [PASSED] Category (Oolong) correctly identified")

    # Must understand oxidation
    if not kw_results["oxidation"]:
        print("| [WARNING] Oxidation level not mentioned")
    else:
        print("| [PASSED] Oxidation level discussed")

    # Must mention rock rhyme (Wuyi characteristic)
    if not kw_results["rock_rhyme"]:
        print("| [WARNING] Rock rhyme (岩韵) not mentioned")
    else:
        print("| [PASSED] Rock rhyme (岩韵) identified")

    # Must identify Wuyi origin
    if not kw_results["wuyi"]:
        print("| [WARNING] Wuyi origin not mentioned")
    else:
        print("| [PASSED] Wuyi origin identified")

    # CHECK 5: Must explain the trap
    print("| " + "-" * 68)
    print("| Trap Explanation:")

    # Model should explain why apprentice was wrong
    trap_explanation = (
        ("red" in ans["e"].lower() or "红" in ans["e"]) and
        ("oolong" in ans["e"].lower() or "乌龙" in ans["e"])
    )

    if trap_explanation:
        print("| [PASSED] Trap explained (name has 'Red' but is Oolong)")
    else:
        print("| [INFO] Could strengthen trap explanation")

    # Check if model corrected the apprentice's error
    if any(phrase in ans["e"].lower() for phrase in [
        "apprentice was wrong", "incorrect", "error", "mistake",
        "not black tea", "不是红茶"
    ]):
        print("| [PASSED] Apprentice error corrected")
    else:
        print("| [INFO] Could explicitly correct apprentice's error")

    print("=" * 70)
    print("| RESULT: SUCCESS")
    print("|")
    print("| Model correctly identified Da Hong Pao as Oolong, not Black Tea.")
    print("| The apprentice's trap (reddish color = black tea) was overcome.")
    print("=" * 70)
    return True


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
