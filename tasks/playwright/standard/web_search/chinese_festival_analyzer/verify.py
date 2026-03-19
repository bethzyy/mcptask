#!/usr/bin/env python3
"""
Verification script for Chinese Traditional Festival Multi-Trap Analysis v43.
Correct answer: Lantern Festival (元宵节/上元节) ONLY

Key features:
- 18 candidates with hidden answer name
- Generic Criterion C explanation (NO direct hints about specific festivals)
- Misleading initial observation (points to Dragon Boat Festival)
- STRICT page visit requirements (10 festivals, 4 foods, 1 Baidu)
- Phase completion required (Phase 1-4 tables)
- 2024-specific date verification
- Baidu Baike visit required

Correct answer validation:
- Date: Feb 24, 2024 (正月十五) - within Jan-Jun 2024 ✅
- Food: Tangyuan/Yuanxiao (sweet dessert eaten by families) ✅
- Position: Culmination day (15th of Spring Festival period) ✅
- Nature: Celebration (no ancestor worship) ✅
- Family: Family gathering is core tradition ✅

Trap layers (L1-L9):
L1: Spring Festival - FIRST day of 15-day period (FAILS C)
L2: Kitchen God - food is OFFERING to deity (FAILS B)
L3: Renri - qicaigeng is SAVORY vegetable soup (FAILS B)
L4: Zhonghe - taiyanggao is RITUAL OFFERING (FAILS B)
L5: Qingming - TOMB SWEEPING, ancestor worship (FAILS E)
L6: Cold Food - MEMORIAL nature (FAILS E)
L7: Dragon Boat - zongzi is DUMPLING, MEMORIAL nature (FAILS B and E)
L8: Autumn/Winter festivals - OUTSIDE Jan-Jun 2024 (FAILS A)
L9: Calendar Type - Must verify 2024 date specifically (lunar varies each year)

v43:
- Generic Criterion C explanation (NO透题)
- Hidden answer name retained
- 10 festival pages, 4 food pages required
- Phase completion strictly enforced
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct answer: Lantern Festival (multiple acceptable names)
CORRECT = {
    "lantern festival", "yuanxiao festival", "shangyuan festival",
    "元宵节", "上元节", "灯节"
}

# Required festival pages (expanded list for search-based approach)
REQUIRED_FESTIVAL_PAGES = [
    "Chinese_New_Year",
    "Spring_Festival",
    "Lantern_Festival",
    "Yuanxiao",
    "Kitchen_God",
    "Kitchen_God_Festival",
    "Xiaonian",
    "Renri",
    "Shangyuan_Festival",
    "Zhonghe_Festival",
    "Tianchuan_Festival",
    "Qingming_Festival",
    "Cold_Food_Festival",
    "Shangsi_Festival",
    "Dragon_Boat_Festival",
    "Duanwu",
    "Tianfu_Festival",
    "Ghost_Festival",
    "Zhongyuan",
    "Mid-Autumn_Festival",
    "Double_Ninth_Festival",
    "Xiayuan_Festival",
    "Dongzhi_Festival",
    "Laba_Festival",
    "Chinese_traditional_festivals",
    "Public_holidays_in_China",
    "List_of_festivals_in_China",
]
MIN_REQUIRED_FESTIVAL_PAGES = 10  # Increased to force extensive exploration

# Required food pages (must visit to verify classification)
REQUIRED_FOOD_PAGES = [
    "Tangyuan",
    "Yuanxiao_(food)",
    "Nian_gao",
    "Zaotang",
    "Guandong_candy",
    "Qingtuan",
    "Zongzi",
    "Mooncake",
    "Laba_porridge",
    "Qicaigeng",
    "Seven-vegetable_soup",
    "Taiyanggao",
    "Sun_cake",
]
MIN_REQUIRED_FOOD_PAGES = 4  # Increased to force food verification

# Calendar/date verification pages
CALENDAR_PAGES = [
    "Chinese_calendar",
    "Lunar_calendar",
    "Lunisolar_calendar",
    "2024_in_China",
    "Public_holidays_in_China",
    "2024",
]
MIN_REQUIRED_CALENDAR_PAGES = 1  # At least 1 calendar reference

# Specific required pages for cross-verification
REQUIRED_SPECIFIC_PAGES = [
    "Chinese_New_Year",
    "Lantern_Festival",
    "Tangyuan",
    "Yuanxiao",
]
MIN_REQUIRED_SPECIFIC_PAGES = 3

# Baidu Baike pages (required for Phase 4)
BAIDU_PAGES = [
    "baidu",
    "baike",
    "元宵节",
    "春节",
    "上元",
]
MIN_BAIDU_PAGES = 1  # Must visit at least 1 Baidu page

# Wrong answers (trap answers with rejection reasons)
WRONG = {
    # L1: First day trap
    "chinese new year", "spring festival", "lunar new year", "春节",
    # L2: Offering trap
    "kitchen god", "xiaonian", "little new year", "祭灶", "小年",
    # L3: Savory food trap
    "renri", "human day", "人日",
    # L4: Ritual offering trap
    "zhonghe", "中和节",
    # L5: Mourning trap
    "qingming", "tomb sweeping", "清明节",
    # L6: Memorial trap
    "cold food", "hanshi", "寒食节",
    # L7: Dumpling trap
    "dragon boat", "duanwu", "端午节",
    # L8: Date range trap (autumn/winter)
    "ghost festival", "zhongyuan", "中元节",
    "mid-autumn", "moon festival", "中秋节",
    "double ninth", "chongyang", "重阳节",
    "xiayuan", "下元节",
    "dongzhi", "winter solstice", "冬至",
    "laba", "腊八节",
    "tianfu", "天贶节",
    # L9: Obscure festival trap
    "tianchuan", "天穿节",
    "shangsi", "上巳节",
}

# Keyword groups for verification (8 groups, need 6/8)
KEYWORD_GROUPS = [
    # Group 1: Date verification (2024 specific)
    ["2024", "february", "january", "june", "first half", "jan-jun"],
    # Group 2: Lunar calendar verification
    ["lunar", "lunisolar", "chinese calendar", "full moon", "fifteenth",
     "正月", "十五", "solar", "阳历", "阴历"],
    # Group 3: Food classification (sweet vs savory/offering)
    ["sweet", "dessert", "tangyuan", "yuanxiao", "汤圆", "元宵",
     "offering", "deity", "worship", "dumpling", "porridge", "savory"],
    # Group 4: Festival nature (mourning exclusion)
    ["family", "gathering", "meal", "eaten", "mourning", "ancestor",
     "memorial", "tomb", "sweeping"],
    # Group 5: Festival position (first day vs culmination)
    ["first day", "culmination", "standalone", "15-day", "period",
     "spring festival period", "position"],
    # Group 6: Cultural context (ancient names, origins)
    ["shangyuan", "上元", "taoist", "buddhist", "ancient", "historical",
     "alias", "also known", "originally"],
    # Group 7: Verification & cross-check terms
    ["converted", "verified", "cross-check", "sources", "wikipedia",
     "baidu", "baike", "calendar", "gregorian", "fixed date", "varying", "varies"],
    # Group 8: Phase completion indicators (NEW for v37)
    ["phase 1", "phase 2", "phase 3", "phase 4", "table complete",
     "date conversion", "food classification", "nature", "cross-verif"],
]
MIN_KEYWORD_GROUPS = 6  # Increased from 4 to 6


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
    r = {"f": [], "e": ""}
    try:
        # Try <answer> tag first
        m = re.search(r"<answer>(.+?)</answer>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["f"] = [x.strip() for x in m.group(1).split("\n") if x.strip()]

        # Check for <verification> or <reasoning>
        m = re.search(r"<verification>(.+?)</verification>", txt, re.DOTALL | re.IGNORECASE)
        if m:
            r["e"] = m.group(1).strip()
        else:
            m = re.search(r"<reasoning>(.+?)</reasoning>", txt, re.DOTALL | re.IGNORECASE)
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


def check_wrong(fests, wrong_set):
    found = []
    for f in fests:
        for w in wrong_set:
            if w in f.lower():
                found.append(f)
                break
    return found


def check_explanation(explanation, groups, min_groups=6):
    if not explanation:
        return False, "No reasoning/verification provided"
    exp_lower = explanation.lower()
    matched = 0
    details = []
    for i, g in enumerate(groups):
        for kw in g:
            if kw.lower() in exp_lower:
                matched += 1
                details.append(f"Group {i+1}: '{kw}'")
                break
    if matched >= min_groups:
        return True, f"Matched {matched} groups: {', '.join(details)}"
    return False, f"Only {matched} group(s). Need {min_groups}. Found: {details}"


def check_page_visits(wd, pages, min_req, ptype="festival"):
    try:
        log_file = wd / "execution.log"
        if not log_file.exists():
            return False, "execution.log not found"
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        visited = set()
        for p in pages:
            if p.lower() in content.lower():
                visited.add(p)
        if len(visited) >= min_req:
            return True, f"Visited {len(visited)} {ptype} pages (required: {min_req})"
        return False, f"Only {len(visited)} {ptype} pages (required: {min_req}): {sorted(visited)}"
    except Exception as e:
        return False, f"Error: {e}"


def check_phase_completion(reasoning):
    """Check if the reasoning includes evidence of phased completion."""
    if not reasoning:
        return False, "No reasoning to check phase completion"

    exp_lower = reasoning.lower()
    phases_found = []

    # Check for Phase 1 indicators
    phase1_indicators = ["phase 1", "date conversion", "2024 gregorian", "date table"]
    if any(ind in exp_lower for ind in phase1_indicators):
        phases_found.append("Phase 1")

    # Check for Phase 2 indicators
    phase2_indicators = ["phase 2", "food classification", "sweet/savory", "food table"]
    if any(ind in exp_lower for ind in phase2_indicators):
        phases_found.append("Phase 2")

    # Check for Phase 3 indicators
    phase3_indicators = ["phase 3", "nature", "position", "celebration/memorial"]
    if any(ind in exp_lower for ind in phase3_indicators):
        phases_found.append("Phase 3")

    # Check for Phase 4 indicators
    phase4_indicators = ["phase 4", "cross-verif", "baidu", "baike"]
    if any(ind in exp_lower for ind in phase4_indicators):
        phases_found.append("Phase 4")

    if len(phases_found) >= 3:
        return True, f"Found {len(phases_found)} phases: {phases_found}"
    return False, f"Only {len(phases_found)} phases found: {phases_found}"


def check_table_format(reasoning):
    """Check if the reasoning includes properly formatted tables."""
    if not reasoning:
        return False, "No reasoning to check table format"

    exp_lower = reasoning.lower()

    # Check for table indicators
    table_indicators = 0
    if "|" in reasoning:  # Markdown table separator
        table_indicators += 1
    if re.search(r'\|.*\|.*\|', reasoning):  # At least 3 columns
        table_indicators += 1
    if "id" in exp_lower and "festival" in exp_lower:
        table_indicators += 1

    if table_indicators >= 2:
        return True, f"Found {table_indicators} table indicators"
    return False, f"Only {table_indicators} table indicators found"


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chinese Festival Multi-Trap Analysis (v43)")
    print("=" * 70)

    msgs = parse_msgs(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    ans = parse_ans(msgs["text"])
    print(f"| Answer: {ans['f']}")
    print(f"| Verification: {len(ans['e'])} chars")
    print("| " + "-" * 68)

    ok = True

    # Check page visits - Festival pages
    fest_ok, fest_msg = check_page_visits(wd, REQUIRED_FESTIVAL_PAGES, MIN_REQUIRED_FESTIVAL_PAGES, "festival")
    if not fest_ok:
        print(f"| [FAILED] Festival pages: {fest_msg}")
        ok = False
    else:
        print(f"| [PASSED] Festival pages: {fest_msg}")

    # Check page visits - Food pages
    food_ok, food_msg = check_page_visits(wd, REQUIRED_FOOD_PAGES, MIN_REQUIRED_FOOD_PAGES, "food")
    if not food_ok:
        print(f"| [FAILED] Food pages: {food_msg}")
        ok = False
    else:
        print(f"| [PASSED] Food pages: {food_msg}")

    # Check page visits - Calendar pages
    cal_ok, cal_msg = check_page_visits(wd, CALENDAR_PAGES, MIN_REQUIRED_CALENDAR_PAGES, "calendar")
    if not cal_ok:
        print(f"| [FAILED] Calendar pages: {cal_msg}")
        ok = False
    else:
        print(f"| [PASSED] Calendar pages: {cal_msg}")

    # Check specific page visits
    spec_ok, spec_msg = check_page_visits(wd, REQUIRED_SPECIFIC_PAGES, MIN_REQUIRED_SPECIFIC_PAGES, "specific")
    if not spec_ok:
        print(f"| [FAILED] Specific pages: {spec_msg}")
        ok = False
    else:
        print(f"| [PASSED] Specific pages: {spec_msg}")

    # Check Baidu Baike visit (required for Phase 4)
    baidu_ok, baidu_msg = check_page_visits(wd, BAIDU_PAGES, MIN_BAIDU_PAGES, "Baidu Baike")
    if not baidu_ok:
        print(f"| [FAILED] Baidu Baike: {baidu_msg}")
        print("|          Phase 4 requires Baidu Baike cross-verification!")
        ok = False
    else:
        print(f"| [PASSED] Baidu Baike: {baidu_msg}")

    print("| " + "-" * 68)

    # Check phase completion
    phase_ok, phase_msg = check_phase_completion(ans["e"])
    if not phase_ok:
        print(f"| [FAILED] Phase completion: {phase_msg}")
        print("|          Expected evidence of Phase 1-4 completion in reasoning")
        ok = False
    else:
        print(f"| [PASSED] Phase completion: {phase_msg}")

    # Check table format
    table_ok, table_msg = check_table_format(ans["e"])
    if not table_ok:
        print(f"| [FAILED] Table format: {table_msg}")
        print("|          Expected markdown tables with | separators")
        ok = False
    else:
        print(f"| [PASSED] Table format: {table_msg}")

    print("| " + "-" * 68)

    # Check correct answer
    if not check_in(ans["f"], CORRECT):
        print("| [FAILED] Lantern Festival missing")
        print("|          Correct answer: Lantern Festival (元宵节/上元节)")
        print("|          - Date: Feb 24, 2024 (正月十五)")
        print("|          - Food: Tangyuan (sweet dessert)")
        print("|          - Position: Culmination of Spring Festival period")
        print("|          - Nature: Celebration (no ancestor worship)")
        ok = False
    else:
        print("| [PASSED] Lantern Festival is the answer")

    # Check wrong answers (traps)
    wrong_found = check_wrong(ans["f"], WRONG)
    if wrong_found:
        print(f"| [FAILED] Wrong festival (trap triggered): {wrong_found}")
        print("|          Trap Rejection Reasons:")
        print("|          L1 - Spring Festival: FIRST day of 15-day period")
        print("|          L2 - Kitchen God: food is OFFERING to deity")
        print("|          L3 - Renri: qicaigeng is SAVORY vegetable soup")
        print("|          L4 - Zhonghe: taiyanggao is RITUAL OFFERING")
        print("|          L5 - Qingming: TOMB SWEEPING, ancestor worship")
        print("|          L6 - Cold Food: MEMORIAL nature")
        print("|          L7 - Dragon Boat: zongzi is DUMPLING")
        print("|          L8 - Autumn/Winter festivals: OUTSIDE Jan-Jun 2024")
        print("|          L9 - Calendar Type: Must verify 2024 date specifically")
        print("|                           (lunar dates vary each year!)")
        ok = False
    else:
        print("| [PASSED] No wrong festivals (traps avoided)")

    # Check reasoning (6/8 groups required)
    exp_ok, exp_msg = check_explanation(ans["e"], KEYWORD_GROUPS, min_groups=MIN_KEYWORD_GROUPS)
    if not exp_ok:
        print(f"| [FAILED] Reasoning: {exp_msg}")
        ok = False
    else:
        print(f"| [PASSED] Reasoning: {exp_msg}")

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
