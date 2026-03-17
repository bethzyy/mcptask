#!/usr/bin/env python3
"""Verification for Botanical Garden ID (v35). Correct: Forsythia suspensa"""
import os, sys, json, re

EXPECTED = ["forsythia suspensa", "forsythia  suspensa", "forsythia"]
WRONG = [
    # Jasminum genus (main trap - matches "5-6 separate petals" observation)
    "jasminum nudiflorum", "winter jasmine", "迎春", "迎春花",
    "jasminum floridum", "jasminum mesnyi", "jasminum humile", "探春花",
    "jasminum mesnyi f. holosericeum", "jasminum humile var. humile",
    "primrose jasmine", "italian jasmine", "yunnan jasmine", "himalayan jasmine",
    # Other Forsythia species (correct genus, wrong species)
    "forsythia viridissima", "forsythia × intermedia", "forsythia koreana",
    "forsythia ovata", "forsythia europaea", "forsythia mandshurica",
    "forsythia giraldiana", "forsythia saxatilis", "forsythia velutina",
    "forsythia mira", "forsythia likiangensis",
    # Other yellow-flowering shrubs
    "kerria japonica", "edgeworthia chrysantha", "paperbush", "chimonanthus praecox",
    "hamamelis mollis", "cornus mas", "cornus officinalis", "corylopsis spicata",
    "mahonia bealei", "mahonia aquifolium", "hypericum patulum",
    "abeliophyllum distichum", "white forsythia", "berberis", "stachyurus",
]

# Key feature verification groups - at least 2/3 must be present
KEYWORD_GROUPS = [
    ["hollow", "中空", "空心", "pith hollow", "internodes hollow"],  # Stem structure
    ["4-parted", "4 lobes", "four lobes", "四裂", "corolla 4", "4 corolla lobes", "4-lobed"],  # Corolla structure
    ["fused", "tube", "campanulate", "合生", "corolla tube"],  # Corolla tube (Forsythia has fused petals)
]

def get_response():
    try:
        path = os.getenv("MCP_MESSAGES")
        if not path: return None
        with open(path, 'r', encoding='utf-8') as f:
            msgs = json.load(f)
        for m in reversed(msgs):
            if m.get('role') == 'assistant':
                c = m.get('content', [])
                if isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict) and i.get('type') in ['text', 'output_text']:
                            return i.get('text', '')
                elif isinstance(c, str): return c
        return None
    except:
        return None

def extract_tag(r, tag):
    m = re.search(rf'<{tag}>\s*(.*?)\s*</{tag}>', r, re.DOTALL | re.I)
    return m.group(1).strip() if m else None

def norm(s): return s.lower().strip()

def check_keywords(reasoning):
    """Check if reasoning contains key features - need at least 2/3 groups"""
    r_lower = reasoning.lower()
    found_groups = 0
    found_keywords = []

    for group in KEYWORD_GROUPS:
        for kw in group:
            if kw.lower() in r_lower:
                found_groups += 1
                found_keywords.append(kw)
                break

    return found_groups, found_keywords

def verify():
    print("=" * 60)
    print("| VERIFICATION: v35")
    print("=" * 60)

    r = get_response()
    if not r:
        print("| [ERROR] No response")
        return False

    # Extract answer and reasoning
    ans = extract_tag(r, "answer")
    reasoning = extract_tag(r, "reasoning") or ""

    if not ans:
        print("| [ERROR] No <answer> tag found")
        return False

    an = norm(ans)
    print(f"| Answer: {ans}")

    # Check for trap answers (wrong species)
    for w in WRONG:
        if norm(w) in an:
            print(f"| [FAILED] Wrong answer: {w}")
            print("| TRAP: Your field observations may be misleading!")
            print("| Hint: Check corolla structure carefully - are the petals truly separate?")
            return False

    # Check for correct answer
    if not any(norm(e) in an for e in EXPECTED):
        print("| [FAILED] Incorrect species")
        print("| Expected: Forsythia suspensa")
        return False

    print("| [PASSED] Correct species: Forsythia suspensa")

    # Check reasoning for key features (at least 2/3 groups)
    if reasoning:
        groups_found, keywords = check_keywords(reasoning)
        print(f"| Keywords found: {keywords} ({groups_found}/3 groups)")

        if groups_found < 2:
            print("| [WARNING] Reasoning lacks key feature explanation")
            print("| Expected: hollow stem, 4-parted corolla, fused corolla tube")
    else:
        print("| [WARNING] No reasoning found to verify key features")

    print("| [SUCCESS] Verification passed!")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
