#!/usr/bin/env python3
"""
Verification for Daoist Concept Investigation (v50).
Correct answer: Xu (虚) - Emptiness/Void - State concept, personal cultivation

v50 Changes:
- Simplified description.md: removed unverifiable requirements (Phase 3 comparison table, etc.)
- Aligned description.md REQUIREMENTS with verify.py checks
- Description now only requires what verify.py actually validates

v49 Changes:
- CRITICAL FIX: Correct answer priority principle (check correct answer BEFORE traps)
- Removed generic English words from CORRECT (emptiness, void, vacuity, etc.)
- Removed compound phrase from TRAP_QINGJING (clarity and stillness)
- Prevents false negatives when model mentions trap while giving correct answer

v48 Changes:
- Fixed trap detection: removed generic words (clarity, stillness, spirit, virtue, etc.)
- Only use unique identifiers (pinyin, Chinese characters, compound phrases) for trap detection
- Prevents false positives when correct answer contains descriptive words

v47 Changes:
- Phase 1 subcategories requirement: 2 → 3
- Added evidence_quote field (requires quote from Tao Te Ching)
- 7 output fields (answer, historical_figure, ttc_chapter, evidence_quote, category_navigation, toc_sections_used, pages_browsed)
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct: Xu (emptiness, void - a STATE of being, personal cultivation, in Tao Te Ching)
# Only use unique identifiers (pinyin + Chinese) to prevent false positives
CORRECT = {
    "xu", "hsu", "虚", "xū", "hsü"  # pinyin variants + Chinese character only
}

# Historical figures associated with Xu
HISTORICAL_FIGURES = {
    "laozi", "lao-tzu", "lao tzu", "老子", "lǎozǐ",
    "zhuangzi", "chuang-tzu", "chuang tzu", "庄子", "莊子", "zhuāngzǐ",
    "wang bi", "王弼", "wáng bì",
    "ge hong", "葛洪", "gě hóng"
}

# TRAP 1: De - Not a state concept (Condition 1)
# Fixed: removed generic words "virtue", "power" - only use unique identifiers
TRAP_DE = {
    "de", "te", "德", "dé"  # pinyin + Chinese character only
}

# TRAP 2: Qingjing - Later development, not in original TTC (Condition 3)
# Fixed: removed "clarity", "stillness" - these are common descriptive words
TRAP_QINGJING = {
    "qingjing", "ching-ching", "清静", "清靜", "qīngjìng"
    # Removed "clarity and stillness" - could be used to describe correct answer
}

# TRAP 3: Ling - Not clearly a state concept (Condition 1)
# Fixed: removed "spirit", "numinous" - these are common words
TRAP_LING = {
    "ling", "靈", "灵", "líng"  # pinyin + Chinese character only
}

# TRAP 4: Jing - Not standalone in TTC (Condition 3)
# Fixed: removed "stillness", "quietude" - these are common descriptive words
TRAP_JING = {
    "jing", "ching", "静", "靜", "jìng"  # pinyin + Chinese character only
}

# TRAP 5: Tian - From Zhuangzi, not TTC (Condition 3)
# Fixed: removed "tranquility", "contentment" - these are common words
TRAP_TIAN = {
    "tian", "t'ien", "恬", "tián"  # pinyin + Chinese character only
}

# TRAP 6: Baoyi - Not an independent concept, it's an action (Condition 1)
# Fixed: removed "embracing the one", "embrace the one" - could match descriptions
TRAP_BAOYI = {
    "baoyi", "pao-i", "抱一", "bàoyī"  # pinyin + Chinese character only
}

# TRAP 7: Shouzhong - Not an independent concept, it's an action (Condition 1)
# Fixed: removed "guarding the center", "guard the center" - could match descriptions
TRAP_SHOUZHONG = {
    "shouzhong", "shou-chung", "守中", "shǒuzhōng"  # pinyin + Chinese character only
}


def get_work_dir():
    p = os.getenv("MCP_MESSAGES")
    if p and Path(p).exists():
        return Path(p).parent
    return Path(".")


def parse_messages(wd):
    """Parse messages and extract text and tool calls."""
    f = wd / "messages.json"
    if not f.exists():
        return {"ok": False, "text": "", "tool_calls": []}

    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"| [ERROR] Failed to parse messages.json: {e}")
        return {"ok": False, "text": "", "tool_calls": []}

    text_parts = []
    tool_calls = []

    for m in data:
        try:
            if m.get("type") == "function_call":
                tool_calls.append(m)
            elif m.get("type") == "function_call_output":
                output = m.get("output", "")
                if isinstance(output, str):
                    text_parts.append(output)
            elif m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))
                            elif i.get("type") == "tool_use":
                                tool_calls.append(i)
            elif m.get("role") == "tool":
                content = m.get("content", "")
                if isinstance(content, str):
                    text_parts.append(content)
        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts), "tool_calls": tool_calls}


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def check_historical_figure(text):
    """Check if historical figure is mentioned."""
    figure = extract_tag(text, "historical_figure")
    if not figure:
        return False, "No <historical_figure> tag found"

    figure_lower = figure.lower()
    for hf in HISTORICAL_FIGURES:
        if hf in figure_lower:
            return True, f"Historical figure: {figure}"

    return False, f"Historical figure not recognized: {figure}"


def check_ttc_chapter(text):
    """Check if TTC chapter is cited."""
    chapter = extract_tag(text, "ttc_chapter")
    if not chapter:
        return False, "No <ttc_chapter> tag found"

    # Check if it contains a number
    if re.search(r'\d+', chapter):
        return True, f"TTC chapter cited: {chapter}"

    return False, f"No valid chapter number in: {chapter}"


def check_evidence_quote(text):
    """Check if evidence quote is provided from Tao Te Ching."""
    quote = extract_tag(text, "evidence_quote")
    if not quote:
        return False, "No <evidence_quote> tag found"

    # Must be at least 20 characters (a meaningful quote)
    if len(quote) < 20:
        return False, f"Evidence quote too short ({len(quote)} chars) - need at least 20"

    return True, f"Evidence quote: {quote[:100]}..."


def check_category_navigation(text):
    """Check if category navigation is documented."""
    nav = extract_tag(text, "category_navigation")
    if not nav:
        return False, "No <category_navigation> tag found"

    # Must contain "Category:" and at least one arrow or "→" or "->"
    nav_lower = nav.lower()
    has_category = "category:" in nav_lower or "category" in nav_lower
    has_path = "→" in nav or "->" in nav or ">" in nav

    if not has_category:
        return False, f"Category navigation missing 'Category:' - got: {nav[:100]}"

    if not has_path:
        return False, f"Category navigation missing path separator (→ or ->) - got: {nav[:100]}"

    return True, f"Category navigation: {nav[:100]}"


def check_toc_sections(text):
    """Check if TOC sections are documented."""
    toc = extract_tag(text, "toc_sections_used")
    if not toc:
        return False, "No <toc_sections_used> tag found"

    # Must contain at least 3 section names (separated by comma)
    sections = [s.strip() for s in toc.split(",") if s.strip()]
    if len(sections) < 3:
        return False, f"TOC sections must list at least 3 sections - got {len(sections)}: {toc}"

    return True, f"TOC sections ({len(sections)}): {toc[:100]}"


def check_pages_browsed(text):
    """Check if pages browsed count is documented."""
    pages = extract_tag(text, "pages_browsed")
    if not pages:
        return False, "No <pages_browsed> tag found"

    # Must contain a number
    match = re.search(r'\d+', pages)
    if not match:
        return False, f"Pages browsed missing number - got: {pages}"

    count = int(match.group())
    if count < 1:
        return False, f"Pages browsed must be at least 1 - got: {count}"

    return True, f"Pages browsed: {pages}"


def count_tool_interactions(tool_calls, text):
    """Count actual interactive elements used (informational)."""
    category_visits = 0
    pagination_used = 0
    sep_toc_used = 0

    text_lower = text.lower()

    for tc in tool_calls:
        try:
            args = tc.get("arguments", {})
            if isinstance(args, str):
                args = json.loads(args) if args else {}
            url = args.get("url", "").lower()

            # Category page visits
            if "category:" in url:
                category_visits += 1

            # Pagination indicators
            if "page=" in url or "from=" in url or "offset=" in url:
                pagination_used += 1

            # SEP TOC navigation (anchor links)
            if "plato.stanford.edu" in url and "#" in url:
                sep_toc_used += 1

        except (json.JSONDecodeError, TypeError):
            continue

    # Also check text output for pagination indicators
    if "next page" in text_lower or "previous page" in text_lower:
        pagination_used += 1

    return category_visits, pagination_used, sep_toc_used


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Daoist Concept Investigation (v50)")
    print("|")
    print("| Criteria:")
    print("|   1. Nature: STATE (describes how things ARE)")
    print("|   2. Scope: NOT cosmological/metaphysical")
    print("|   3. Source: Must be in Tao Te Ching (cite chapter)")
    print("|   4. Usage: Associated with personal cultivation/meditation")
    print("|   5. History: Has associated historical figure")
    print("|")
    print("| Interactive Requirements:")
    print("|   - evidence_quote: REQUIRED (quote from Tao Te Ching)")
    print("|   - category_navigation: REQUIRED")
    print("|   - toc_sections_used: REQUIRED (at least 3 sections)")
    print("|   - pages_browsed: REQUIRED (at least 1)")
    print("|")
    print("| Correct: Xu (虚) - State of emptiness/void")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    tool_calls = msgs["tool_calls"]

    # Report interaction stats (informational)
    cat_visits, pag_used, toc_used = count_tool_interactions(tool_calls, text)
    print(f"| [INFO] Tool-based category visits: {cat_visits}")
    print(f"| [INFO] Tool-based pagination: {pag_used}")
    print(f"| [INFO] Tool-based SEP TOC navigation: {toc_used}")
    print("|")

    # Check 1: Answer tag present
    answer = extract_tag(text, "answer")
    if not answer:
        print("| [FAILED] No <answer> tag found")
        print("|          Format: <answer>[concept]</answer>")
        print("=" * 70)
        return False
    answer_lower = answer.lower()
    print(f"| [INFO] Answer: {answer[:100]}")

    # Check 2: Find correct answer FIRST (correct answer priority principle)
    # Per review_lessons.md: If model mentions correct answer, ignore trap mentions
    # (model may be explaining reasoning: "Xu (not Qingjing)")
    found_correct = False
    for correct in CORRECT:
        if correct in answer_lower:
            found_correct = True
            break

    if not found_correct:
        # Check 3: Trap detection (only if no correct answer found)
        all_traps = [
            (TRAP_DE, "De", "Fails Condition 1: Not a state concept"),
            (TRAP_QINGJING, "Qingjing", "Fails Condition 3: Not in original TTC"),
            (TRAP_LING, "Ling", "Fails Condition 1: Not clearly a state"),
            (TRAP_JING, "Jing", "Fails Condition 3: Not standalone in TTC"),
            (TRAP_TIAN, "Tian", "Fails Condition 3: From Zhuangzi, not TTC"),
            (TRAP_BAOYI, "Baoyi", "Fails Condition 1: Not an independent concept (action phrase)"),
            (TRAP_SHOUZHONG, "Shouzhong", "Fails Condition 1: Not an independent concept (action phrase)"),
        ]

        for trap_set, trap_name, trap_reason in all_traps:
            for trap in trap_set:
                if trap in answer_lower:
                    print(f"| [FAILED] Incorrect answer: {trap_name}")
                    print(f"|          {trap_reason}")
                    print("|          The correct concept satisfies ALL 5 conditions")
                    print("=" * 70)
                    return False

        # No correct answer, no trap → unknown answer
        print("| [FAILED] Correct answer not found")
        print("|          Expected: A concept that passes ALL 5 conditions")
        print("=" * 70)
        return False

    # Check 4: Historical figure (only for correct answer)
    fig_ok, fig_msg = check_historical_figure(text)
    if not fig_ok:
        print(f"| [FAILED] {fig_msg}")
        print("|          Required: <historical_figure>[name]</historical_figure>")
        print("=" * 70)
        return False
    print(f"| [OK] {fig_msg}")

    # Check 5: TTC chapter (only for correct answer)
    chapter_ok, chapter_msg = check_ttc_chapter(text)
    if not chapter_ok:
        print(f"| [FAILED] {chapter_msg}")
        print("|          Required: <ttc_chapter>[number]</ttc_chapter>")
        print("=" * 70)
        return False
    print(f"| [OK] {chapter_msg}")

    # Check 6: Evidence quote (REQUIRED)
    quote_ok, quote_msg = check_evidence_quote(text)
    if not quote_ok:
        print(f"| [FAILED] {quote_msg}")
        print("|          Required: <evidence_quote>[quote from Tao Te Ching]</evidence_quote>")
        print("=" * 70)
        return False
    print(f"| [OK] {quote_msg}")

    # Check 7: Category navigation (REQUIRED)
    cat_ok, cat_msg = check_category_navigation(text)
    if not cat_ok:
        print(f"| [FAILED] {cat_msg}")
        print("|          Required: <category_navigation>[Category:... → ... → ...]</category_navigation>")
        print("=" * 70)
        return False
    print(f"| [OK] {cat_msg}")

    # Check 8: TOC sections used (REQUIRED - at least 3)
    toc_ok, toc_msg = check_toc_sections(text)
    if not toc_ok:
        print(f"| [FAILED] {toc_msg}")
        print("|          Required: <toc_sections_used>[Section1, Section2, Section3]</toc_sections_used>")
        print("=" * 70)
        return False
    print(f"| [OK] {toc_msg}")

    # Check 9: Pages browsed (REQUIRED)
    pages_ok, pages_msg = check_pages_browsed(text)
    if not pages_ok:
        print(f"| [FAILED] {pages_msg}")
        print("|          Required: <pages_browsed>[N pages]</pages_browsed>")
        print("=" * 70)
        return False
    print(f"| [OK] {pages_msg}")

    print("|")
    print("| [PASSED] Correct answer: Xu")
    print("|          State of emptiness / Void")
    print("|          Passes all 5 conditions:")
    print("|            1. Describes a STATE of being")
    print("|            2. NOT cosmological (personal cultivation)")
    print("|            3. Mentioned in Tao Te Ching")
    print("|            4. Associated with meditation practice")
    print("|            5. Has associated historical figures")
    print("|")
    print("|          Interactive requirements met:")
    print("|            - Evidence quote provided")
    print("|            - Category navigation documented")
    print("|            - TOC sections documented (at least 3)")
    print("|            - Pages browsed documented")
    print("=" * 70)
    print("| RESULT: SUCCESS")
    print("=" * 70)
    return True


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
