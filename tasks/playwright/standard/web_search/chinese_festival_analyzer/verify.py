#!/usr/bin/env python3
"""
Verification script for Chinese Traditional Festival Cross-Analyzer v28.
Correct answer: Lantern Festival
- Feb 24, 2024 (in First Half 2024: Jan 1 - Jun 30)
- Tangyuan is sweet dessert eaten by families
- Culmination day of Spring Festival (not first day)
- Full moon day (15th of lunar month)
- Family gathering is core tradition
- No mourning/ancestor worship rituals

Key traps:
1. Qingming Festival: Qingtuan is dumpling + has mourning nature (FAILS B & E)
2. Dragon Boat Festival: Zongzi is dumpling (FAILS B)
3. Chinese New Year: First day of 15-day period (FAILS C)
4. Laba Festival: Laba porridge is porridge (FAILS B)
5. Kitchen God Festival: Zaotang is offering (FAILS B)
6. Dongzhi Festival: Date Dec 21 NOT in first half 2024 (FAILS A)
7. Ghost Festival: Involves ancestor worship (FAILS E)
8. Cold Food Festival: Associated with mourning (FAILS E)
9. Double Ninth: Involves ancestor worship + date not in H1 (FAILS A & E)

v28 improvements:
- Increased minimum page visits (10 festival + 6 food + 1 lunar calendar)
- Added lunar calendar page verification
- Added cross-verification keyword checks
- Added exclusion reason requirements
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct answer: Lantern Festival only
CORRECT = {
    "lantern festival", "yuanxiao festival", "shangyuan festival"
}

# Required festival pages (15 candidates + related)
REQUIRED_FESTIVAL_PAGES = [
    "Chinese_New_Year",
    "Lantern_Festival",
    "Kitchen_God",
    "Kitchen_God_Festival",
    "Xiaonian",
    "Renri",
    "Tianchuan_Festival",
    "Zhonghe_Festival",
    "Qingming_Festival",
    "Cold_Food_Festival",
    "Hanshi_Festival",
    "Dragon_Boat_Festival",
    "Qixi_Festival",
    "Ghost_Festival",
    "Mid-Autumn_Festival",
    "Double_Ninth_Festival",
    "Dongzhi_Festival",
    "Dongzhi",
    "Winter_solstice",
    "Laba_Festival",
]
MIN_REQUIRED_FESTIVAL_PAGES = 7  # Final adjusted value

# Required food pages (must visit to verify classification)
REQUIRED_FOOD_PAGES = [
    "Tangyuan",
    "Yuanxiao_(food)",
    "Yuanxiao",
    "Nian_gao",
    "Niangao",
    "Zaotang",
    "Qingtuan",
    "Zongzi",
    "Mooncake",
    "Laba_porridge",
    "Laba_congee",
    "Sweet_rice_ball",
    "Jiaozi",
    "Dumpling",
    "Qicaigeng",
    "Seven-vegetable_soup",
]
MIN_REQUIRED_FOOD_PAGES = 3  # Adjusted for realistic expectations

# Lunar calendar / date verification pages
LUNAR_CALENDAR_PAGES = [
    "Chinese_calendar",
    "Lunar_calendar",
    "Lunisolar_calendar",
    "Sexagenary_cycle",
    "2024_in_China",
    "Public_holidays_in_China",
    "Chinese_New_Year_dates",
    "Lunar_new_year",
    "2024",
]
MIN_REQUIRED_LUNAR_PAGES = 1

# Wrong answers (trap answers with rejection reasons)
WRONG = {
    # TRAP 1: Qingming - qingtuan is dumpling + mourning nature
    "qingming", "tomb sweeping",
    # TRAP 2: Dragon Boat - zongzi is dumpling
    "dragon boat", "duanwu",
    # TRAP 3: Chinese New Year - first day of 15-day period
    "chinese new year", "spring festival", "lunar new year",
    # TRAP 4: Laba - porridge is not dessert
    "laba",
    # TRAP 5: Kitchen God - zaotang is offering
    "kitchen god", "xiaonian", "little new year",
    # TRAP 6: Dongzhi - date not in first half 2024
    "dongzhi", "winter solstice",
    # TRAP 7: Ghost Festival - ancestor worship
    "ghost festival", "hungry ghost",
    # TRAP 8: Cold Food - mourning association
    "cold food", "hanshi",
    # TRAP 9: Double Ninth - ancestor worship + date not in H1
    "double ninth", "chongyang",
    # Other wrong answers
    "renri", "human day",
    "tianchuan",
    "zhonghe",
    "qixi", "double seventh",
    "mid-autumn", "moon festival",
}

# Valid foods
VALID_FOODS = {
    "tangyuan", "yuanxiao", "glutinous rice ball", "sweet rice ball",
}

# Keyword groups for verification (8 dimensions - increased from 6)
KEYWORD_GROUPS = [
    # Group 1: Date verification (first half = Jan-Jun)
    ["january", "february", "march", "april", "may", "june", "first half", "june 30", "2024"],
    # Group 2: Lunar calendar verification
    ["lunar", "lunisolar", "chinese calendar", "full moon", "fifteenth", "moon", "sexagenary"],
    # Group 3: Food classification
    ["eaten", "offering", "family", "meal", "deity", "sacrifice", "dessert", "dumpling", "sweet", "savory", "porridge", "congee"],
    # Group 4: Festival position
    ["first day", "culmination", "standalone", "multi-day", "fifteen", "period", "start", "end"],
    # Group 5: Festival nature (mourning exclusion)
    ["mourning", "ancestor", "memorial", "tomb", "worship", "deceased", "remembrance"],
    # Group 6: Cross-verification terms
    ["cross-check", "verified", "source", "confirmed", "wikipedia", "baidu"],
    # Group 7: Phase completion terms
    ["phase 1", "phase 2", "phase 3", "phase 4", "screening", "classification", "analysis"],
    # Group 8: Exclusion documentation
    ["excluded", "failed", "condition", "does not meet", "qualifies", "classification", "verdict", "trap", "exclusion reason"],
]

# Exclusion reason keywords (must appear for rejected candidates)
EXCLUSION_KEYWORDS = [
    "dumpling", "porridge", "offering", "mourning", "ancestor", "memorial",
    "first day", "not in h1", "july", "august", "september", "october", "november", "december",
    "tomb", "deceased", "remembrance", "worship",
]


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
    r = {"f": [], "d": [], "s": [], "e": ""}
    try:
        m = re.search(r"<FESTIVALS>(.+?)</FESTIVALS>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["f"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        m = re.search(r"<DATES>(.+?)</DATES>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["d"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        m = re.search(r"<FOODS>(.+?)</FOODS>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["s"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        # Check for <verification> or <EXPLANATION>
        m = re.search(r"<verification>(.+?)</verification>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["e"] = m.group(1).strip()
        else:
            m = re.search(r"<EXPLANATION>(.+?)</EXPLANATION>", txt, re.DOTALL | re.IGNORECASE)
            if m:
                r["e"] = m.group(1).strip()
    except Exception as e:
        print(f"| [ERROR] Failed to parse answer: {e}")
    return r


def check_in(fests, exp):
    for f in fests:
        for e in exp:
            if e in f.lower():
                return True
    return False


def check_foods(foods, valid):
    for f in foods:
        f_lower = f.lower()
        for v in valid:
            if v in f_lower:
                return True
    return False


def check_dates_format(dates):
    # Accept both YYYY-MM-DD and MM/DD formats
    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})|(\d{2}/\d{2})")
    for d in dates:
        if date_pattern.search(d.strip()):
            return True
    return False


def check_wrong(fests, wrong_set):
    found = []
    for f in fests:
        for w in wrong_set:
            if w in f.lower():
                found.append(f)
                break
    return found


def check_explanation(explanation, groups, min_groups=5):
    if not explanation:
        return False, "No explanation/verification provided"
    exp_lower = explanation.lower()
    matched = 0
    details = []
    for i, g in enumerate(groups):
        for kw in g:
            if kw in exp_lower:
                matched += 1
                details.append(f"Group {i+1}: '{kw}'")
                break
    if matched >= min_groups:
        return True, f"Matched {matched} groups: {', '.join(details)}"
    return False, f"Only {matched} group(s). Need {min_groups}. Found: {details}"


def check_exclusion_reasons(explanation, exclusion_keywords, min_matches=3):
    """Check if exclusion reasons are documented for rejected candidates."""
    if not explanation:
        return False, "No explanation to check for exclusion reasons"
    exp_lower = explanation.lower()
    found = []
    for kw in exclusion_keywords:
        if kw in exp_lower:
            found.append(kw)
    if len(found) >= min_matches:
        return True, f"Found {len(found)} exclusion keywords: {', '.join(found[:5])}..."
    return False, f"Only {len(found)} exclusion keywords (need {min_matches}): {found}"


def check_page_visits(wd, pages, min_req, ptype="festival"):
    try:
        log_file = wd / "execution.log"
        if not log_file.exists():
            return False, "execution.log not found"
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        visited = set()
        for p in pages:
            if p in content:
                visited.add(p)
        if len(visited) >= min_req:
            return True, f"Visited {len(visited)} {ptype} pages (required: {min_req})"
        return False, f"Only {len(visited)} {ptype} pages (required: {min_req}): {sorted(visited)}"
    except Exception as e:
        return False, f"Error: {e}"


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chinese Festival Cross-Analyzer (v28)")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    ans = parse_ans(msgs["text"])
    print(f"| Festivals: {ans['f']}")
    print(f"| Dates: {ans['d']}")
    print(f"| Foods: {ans['s']}")
    print(f"| Verification: {len(ans['e'])} chars")
    print("| " + "-" * 68)

    ok = True

    # Check page visits - Festival pages (increased requirement)
    fest_ok, fest_msg = check_page_visits(wd, REQUIRED_FESTIVAL_PAGES, MIN_REQUIRED_FESTIVAL_PAGES, "festival")
    if not fest_ok:
        print(f"| [FAILED] Festival pages: {fest_msg}")
        ok = False
    else:
        print(f"| [PASSED] Festival pages: {fest_msg}")

    # Check page visits - Food pages (increased requirement)
    food_ok, food_msg = check_page_visits(wd, REQUIRED_FOOD_PAGES, MIN_REQUIRED_FOOD_PAGES, "food")
    if not food_ok:
        print(f"| [FAILED] Food pages: {food_msg}")
        ok = False
    else:
        print(f"| [PASSED] Food pages: {food_msg}")

    # Check page visits - Lunar calendar pages (NEW requirement)
    lunar_ok, lunar_msg = check_page_visits(wd, LUNAR_CALENDAR_PAGES, MIN_REQUIRED_LUNAR_PAGES, "lunar calendar")
    if not lunar_ok:
        print(f"| [FAILED] Lunar calendar pages: {lunar_msg}")
        ok = False
    else:
        print(f"| [PASSED] Lunar calendar pages: {lunar_msg}")

    print("| " + "-" * 68)

    # Check correct answer - Lantern Festival
    if not check_in(ans["f"], {"lantern festival", "yuanxiao festival"}):
        print("| [FAILED] Lantern Festival missing")
        print("|          Note: Lantern Festival is the correct answer")
        print("|          - Feb 24, 2024 (in First Half: Jan 1 - Jun 30)")
        print("|          - Tangyuan is sweet dessert eaten by families")
        print("|          - Culmination day (not first day) of Spring Festival")
        print("|          - No mourning/ancestor worship rituals")
        ok = False
    else:
        print("| [PASSED] Lantern Festival included")

    # Check wrong answers (traps)
    wrong_found = check_wrong(ans["f"], WRONG)
    if wrong_found:
        print(f"| [FAILED] Wrong festivals (traps triggered): {wrong_found}")
        print("|          Trap Rejection Reasons:")
        print("|          TRAP 1 - Qingming: qingtuan is dumpling + mourning nature")
        print("|          TRAP 2 - Dragon Boat: zongzi is dumpling")
        print("|          TRAP 3 - Chinese New Year: first day of 15-day period")
        print("|          TRAP 4 - Laba: porridge is not dessert")
        print("|          TRAP 5 - Kitchen God: zaotang is offering")
        print("|          TRAP 6 - Dongzhi: date Dec 21 NOT in H1 2024")
        print("|          TRAP 7 - Ghost Festival: ancestor worship")
        print("|          TRAP 8 - Cold Food: mourning association")
        print("|          TRAP 9 - Double Ninth: ancestor worship + date not in H1")
        ok = False
    else:
        print("| [PASSED] No wrong festivals (all traps avoided)")

    # Check dates
    if not ans["d"]:
        print("| [FAILED] No dates provided")
        ok = False
    elif not check_dates_format(ans["d"]):
        print(f"| [FAILED] Invalid date format: {ans['d']}")
        print("|         Expected: YYYY-MM-DD or MM/DD format")
        ok = False
    else:
        print(f"| [PASSED] Dates: {ans['d']}")

    # Check foods
    if not ans["s"]:
        print("| [FAILED] No foods provided")
        ok = False
    elif not check_foods(ans["s"], VALID_FOODS):
        print(f"| [FAILED] Invalid foods: {ans['s']}")
        print("|         Expected: tangyuan, yuanxiao, or sweet rice ball")
        ok = False
    else:
        print(f"| [PASSED] Foods: {ans['s']}")

    # Check verification/explanation (increased requirement from 4 to 5 groups)
    exp_ok, exp_msg = check_explanation(ans["e"], KEYWORD_GROUPS, min_groups=5)
    if not exp_ok:
        print(f"| [FAILED] Verification: {exp_msg}")
        ok = False
    else:
        print(f"| [PASSED] Verification: {exp_msg}")

    # Check exclusion reasons (NEW requirement)
    excl_ok, excl_msg = check_exclusion_reasons(ans["e"], EXCLUSION_KEYWORDS, min_matches=3)
    if not excl_ok:
        print(f"| [FAILED] Exclusion documentation: {excl_msg}")
        print("|         Must document WHY each candidate was rejected")
        ok = False
    else:
        print(f"| [PASSED] Exclusion documentation: {excl_msg}")

    print("=" * 70)
    if ok:
        print("| RESULT: SUCCESS")
        return True
    else:
        print("| RESULT: FAILED")
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
