#!/usr/bin/env python3
"""
Verification script for Chinese Traditional Festival Cross-Analyzer.
Validates that the model correctly identifies festivals meeting all criteria.
"""
import sys
import json
import os
import re
from pathlib import Path

# Required festivals (must be included in answer)
EXPECTED = {"chinese new year", "spring festival", "lantern festival"}

# Excluded festivals (must NOT be included)
EXCLUDED = {
    "dragon boat", "duanwu", "端午",
    "mid-autumn", "moon festival", "中秋",
    "double ninth", "chongyang", "重阳",
    "qingming", "tomb sweeping", "清明",
    "winter solstice", "dongzhi", "冬至",
    "laba", "腊八",
    "hungry ghost", "zhongyuan", "中元", "ghost festival",
    "kitchen god", "xiaonian", "小年"
}

# Valid desserts with dedicated Wikipedia articles (Condition E)
VALID_DESSERTS = {
    "nian gao", "年糕", "rice cake", "sweet rice cake",
    "tangyuan", "汤圆", "yuanxiao", "元宵",
    "glutinous rice ball", "sweet glutinous rice"
}


def get_work_dir():
    """Get working directory from MCP_MESSAGES environment variable."""
    try:
        p = os.getenv("MCP_MESSAGES")
        if p and Path(p).exists():
            return Path(p).parent
        return Path(".")
    except Exception as e:
        print(f"| [ERROR] Failed to get work dir: {e}")
        return Path(".")


def parse_msgs(wd):
    """Parse messages.json and extract the last assistant message."""
    try:
        f = wd / "messages.json"
        if not f.exists():
            print(f"| [ERROR] messages.json not found at {f}")
            return {"ok": False}

        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)

        text = ""
        for m in data:
            if m.get("role") == "assistant":
                c = str(m.get("content", ""))
                if isinstance(m.get("content"), list):
                    parts = []
                    for i in m.get("content", []):
                        if isinstance(i, dict):
                            parts.append(i.get("text", ""))
                        else:
                            parts.append(str(i))
                    c = " ".join(parts)
                text = c
        return {"ok": True, "text": text}
    except Exception as e:
        print(f"| [ERROR] Failed to parse messages: {e}")
        return {"ok": False}


def parse_ans(txt):
    """Parse the answer from the model response."""
    r = {"f": [], "d": [], "s": []}
    try:
        # Parse FESTIVALS
        m = re.search(r"<FESTIVALS>(.+?)</FESTIVALS>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["f"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        # Parse DATES
        m = re.search(r"<DATES>(.+?)</DATES>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["d"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        # Parse DESSERTS
        m = re.search(r"<DESSERTS>(.+?)</DESSERTS>", txt, re.DOTALL | re.IGNORECASE)
        if not m:
            m = re.search(r"<SWEET_FOODS>(.+?)</SWEET_FOODS>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["s"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]
    except Exception as e:
        print(f"| [ERROR] Failed to parse answer: {e}")

    return r


def check_in(fests, exp):
    """Check if any expected festival is in the festivals list."""
    for f in fests:
        for e in exp:
            if e in f.lower():
                return True
    return False


def check_desserts(desserts, valid):
    """Check if desserts contain valid sweet foods with dedicated Wikipedia articles."""
    for d in desserts:
        d_lower = d.lower()
        for v in valid:
            if v in d_lower:
                return True
    return False


def check_ex(fests, exc):
    """Check if any excluded festival is in the festivals list."""
    for f in fests:
        for e in exc:
            if e in f.lower():
                return True
    return False


def verify(wd):
    """Main verification function."""
    print("=" * 70)
    print("| VERIFICATION: Chinese Festival Analyzer")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    ans = parse_ans(msgs["text"])
    print(f"| Festivals found: {ans['f']}")
    print(f"| Dates found: {ans['d']}")
    print(f"| Desserts found: {ans['s']}")
    print("| " + "-" * 68)

    ok = True

    # Check required festivals: Chinese New Year
    if not check_in(ans["f"], EXPECTED):
        print("| [FAILED] Chinese New Year/Spring Festival missing")
        print(f"|          Expected to include: {EXPECTED}")
        ok = False
    else:
        print("| [PASSED] Chinese New Year/Spring Festival included")

    # Check required festivals: Lantern Festival
    if not check_in(ans["f"], {"lantern festival"}):
        print("| [FAILED] Lantern Festival missing")
        ok = False
    else:
        print("| [PASSED] Lantern Festival included")

    # Check excluded festivals
    for exc in EXCLUDED:
        if check_ex(ans["f"], {exc}):
            print(f"| [FAILED] Excluded festival '{exc}' incorrectly included")
            ok = False
            break
    else:
        print("| [PASSED] No excluded festivals included")

    # Check dates
    if not ans["d"]:
        print("| [FAILED] No dates provided")
        print("|          Expected: dates in MM/DD format")
        ok = False
    else:
        print(f"| [PASSED] Dates provided: {ans['d']}")

    # Check desserts (Condition B: must be dessert, Condition E: must have dedicated Wikipedia article)
    if not ans["s"]:
        print("| [FAILED] No desserts/sweet foods provided")
        print("|          Expected: sweet foods with dedicated Wikipedia articles")
        ok = False
    elif not check_desserts(ans["s"], VALID_DESSERTS):
        print(f"| [FAILED] Desserts do not match valid sweet foods")
        print(f"|          Found: {ans['s']}")
        print(f"|          Expected valid desserts: nian gao, tangyuan, yuanxiao")
        ok = False
    else:
        print(f"| [PASSED] Valid desserts provided: {ans['s']}")

    print("=" * 70)
    if ok:
        print("| RESULT: Task completed successfully!")
        return True
    else:
        print("| RESULT: Task failed")
        return False


def main():
    try:
        wd = get_work_dir()
        print(f"| Working directory: {wd}")
        result = verify(wd)
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"| [ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
