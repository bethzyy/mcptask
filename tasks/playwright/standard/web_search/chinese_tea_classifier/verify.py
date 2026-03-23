#!/usr/bin/env python3
"""
Verification for Chinese Tea Classification Task v6.
Correct answer: Da Hong Pao (大红袍) - Wuyi Rock Oolong

v6 Design:
- Wikipedia Link-Chain Navigation starting from Chinese_tea
- Step-by-step output requirement (20+ turns)
- Name trap: "Big Red Robe" sounds like Black Tea but is Oolong
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
    "semi-oxidized", "半发酵", "rock tea", "岩茶"
}

# Trap answers - Black Teas
TRAP_BLACK_TEAS = set([
    "lapsang souchong", "正山小种", "jin jun mei", "金骏眉",
    "tanyang gongfu", "坦洋工夫", "dian hong", "滇红",
])

# Phrases indicating model chose Black Tea as final answer (only in answer section)
TRAP_ANSWER_PHRASES = [
    "category: black tea", "category: black",
    "type: black tea", "type: black"
]

MIN_TURNS = 20


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
            return {"ok": False, "text": "", "turns": 0}

        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)

        text_parts = []
        urls = []

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

            if m.get("role") == "tool" or m.get("type") == "function_call_output":
                content = m.get("content", "") or m.get("output", "")
                if isinstance(content, str):
                    found_urls = re.findall(r'https?://[^\s<>"\']+', content)
                    urls.extend(found_urls)

        full_text = " ".join(text_parts)
        turn_markers = re.findall(r'===\s*TURN\s*\d+', full_text, re.IGNORECASE)
        turn_count = len(turn_markers)

        if turn_count < 5:
            alt_turns = re.findall(r'TURN\s*\d+', full_text, re.IGNORECASE)
            turn_count = max(turn_count, len(alt_turns))

        wikipedia_urls = [u for u in urls if 'wikipedia.org' in u.lower()]
        if turn_count < 5 and len(wikipedia_urls) > 0:
            turn_count = len(set(wikipedia_urls))

        return {"ok": True, "text": full_text, "turns": turn_count}
    except Exception as e:
        print(f"| [ERROR] Failed to parse messages: {e}")
        return {"ok": False, "text": "", "turns": 0}


def parse_ans(txt):
    r = {"f": [], "e": "", "answer_text": ""}
    try:
        m = re.search(r"<answer>(.+?)</answer>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["answer_text"] = m.group(1).strip()
            r["f"] = [x.strip() for x in r["answer_text"].split("\n") if x.strip()]

        m = re.search(r"<reasoning>(.+?)</reasoning>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["e"] = m.group(1).strip()

        if not r["f"]:
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
    found = []
    for f in fests:
        f_lower = f.lower()
        for w in wrong_set:
            if w in f_lower:
                found.append(f)
                break
    return found


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chinese Tea Classification (v6)")
    print("| Correct Answer: Da Hong Pao (大红袍) - Wuyi Rock Oolong")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    turn_count = msgs["turns"]
    print(f"| Detected turns: {turn_count}")
    print(f"| Minimum required: {MIN_TURNS}")

    ans = parse_ans(msgs["text"])
    print(f"| Answer: {ans['f']}")
    print(f"| Reasoning: {len(ans['e'])} chars")
    print("| " + "-" * 68)

    reasoning_lower = ans["e"].lower()
    answer_lower = ans["answer_text"].lower()

    # CHECK 1: Did model choose Black Tea in final answer?
    chose_black = any(phrase in answer_lower for phrase in TRAP_ANSWER_PHRASES)
    if chose_black:
        print("| [FAILED] Model chose Black Tea as final category!")
        print("|          Da Hong Pao is Oolong, NOT Black Tea")
        return False

    # CHECK 2: Correct tea name
    if not check_in(ans["f"], CORRECT_NAMES):
        print("| [FAILED] Correct tea NOT found")
        print("|          Expected: Da Hong Pao (大红袍)")
        print(f"|          Got: {ans['f']}")
        return False
    print("| [PASSED] Correct tea: Da Hong Pao")

    # CHECK 3: Correct category
    has_oolong = check_in(ans["f"], CORRECT_CATEGORY) or any(kw in reasoning_lower for kw in CORRECT_CATEGORY)
    if not has_oolong:
        print("| [FAILED] Correct category NOT identified")
        print("|          Expected: Oolong (乌龙茶)")
        return False
    print("| [PASSED] Correct category: Oolong")

    # CHECK 4: No trap answers
    wrong_found = check_wrong(ans["f"], TRAP_BLACK_TEAS)
    if wrong_found:
        print(f"| [FAILED] Trap answer selected: {wrong_found}")
        return False
    print("| [PASSED] No trap answers selected")

    # CHECK 5: Turn count (information only, not verified)
    print("| " + "-" * 68)
    print(f"| [INFO] Turn count: {turn_count} (recommended: {MIN_TURNS}+)")

    # CHECK 6: Trap explanation
    print("| " + "-" * 68)
    trap_explained = ("red" in reasoning_lower or "红" in ans["e"]) and \
                     ("oolong" in reasoning_lower or "乌龙" in ans["e"])
    if trap_explained:
        print("| [PASSED] Trap explained")
    else:
        print("| [INFO] Could strengthen trap explanation")

    print("=" * 70)
    print("| RESULT: SUCCESS")
    print(f"| Model identified Da Hong Pao as Oolong in {turn_count} turns")
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
