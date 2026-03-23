#!/usr/bin/env python3
"""
Verification script for v137 - Link-Chain Exploration.
Checks:
1. Correct festival selection in <answer> tag
2. <page_chain> contains at least 4 Wikipedia URLs
3. <reasoning> contains evidence for at least 4/6 criteria
"""
import sys
import json
import os
import re
from pathlib import Path


def extract_tag(text, tag):
    """Extract content from XML-style tag. Returns the LAST match if multiple exist."""
    matches = re.findall(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else None


# Correct festival answers
CORRECT_FESTIVALS = {
    "shangsi", "double third", "shangsi festival", "shangsi (double third)",
    "renri", "human day", "renri (human day)",
}


def get_work_dir():
    """Get working directory from MCP_MESSAGES environment variable."""
    try:
        p = os.getenv("MCP_MESSAGES")
        if p and Path(p).exists():
            return Path(p).parent
        return Path(".")
    except Exception as e:
        print(f"| [ERROR] {e}")
        return Path(".")


def parse_messages(wd):
    """Parse messages.json and extract all assistant text."""
    try:
        f = wd / "messages.json"
        if not f.exists():
            print(f"| [ERROR] messages.json not found at {f}")
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
        print(f"| [ERROR] Failed to parse messages: {e}")
        return {"ok": False, "text": "", "raw": []}


def check_festival_selection(text):
    """Check if correct festival is selected in the <answer> tag."""
    # First try to extract from <answer> tag
    answer_content = extract_tag(text, "answer")

    if answer_content:
        answer_lower = answer_content.lower()

        # Check for correct festival in answer
        for correct in CORRECT_FESTIVALS:
            if correct in answer_lower:
                return True, f"Correct festival in <answer>: {correct}"

        return False, f"No valid festival found in <answer>: {answer_content[:100]}"

    # Fallback: Look for festival line in answer - multiple possible formats
    festival_patterns = [
        r'Festival:\s*(.+?)(?:\n|$)',
        r'Selected Festival:\s*(.+?)(?:\n|$)',
        r'Final Festival:\s*(.+?)(?:\n|$)',
        r'\*\*Festival:\*\*\s*(.+?)(?:\n|$)',
        r'Festival name:\s*(.+?)(?:\n|$)',
        r'Answer:\s*(.+?)(?:\n|$)',
    ]

    for pattern in festival_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            festival_line = m.group(1).strip().lower()
            festival_line = re.sub(r'\*\*', '', festival_line)
            festival_line = re.sub(r'\s*\(.*?\)', '', festival_line)
            festival_line = festival_line.strip()

            # Check for correct festival
            for correct in CORRECT_FESTIVALS:
                if correct in festival_line or festival_line in correct:
                    return True, f"Correct festival: {correct}"

    return False, "No valid festival found in output"


def count_urls_in_page_chain(text):
    """Count URLs in <page_chain> tag."""
    content = extract_tag(text, "page_chain")
    if not content:
        return 0
    urls = re.findall(r'https?://[^\s\)\]\}]+', content)
    return len(urls)


def check_reasoning_evidence(text):
    """Check if <reasoning> contains evidence for at least 4/6 criteria."""
    content = extract_tag(text, "reasoning")
    if not content:
        return False, "<reasoning> tag not found"

    content_lower = content.lower()
    # More precise keywords to reduce false positives/negatives
    criteria_keywords = {
        "food_color": [
            "green food", "green color", "green rice", "green cake",
            "mugwort", "herbs", "green vegetables", "green vegetable"
        ],
        "food_taste": [
            "not sweet", "savory", "bitter", "no sugar", "without sugar",
            "unsweetened", "salty", "non-sweet", "no honey", "sugar-free",
            "unsweet"
        ],
        "symbolism": [
            "health", "purification", "warding off", "ward off",
            "evil spirits", "cleansing", "protection", "warding evil"
        ],
        "region": [
            "jiangnan", "north china plain", "southern china",
            "yangtze river", "south of the yangtze", "yangtze delta"
        ],
        "era": [
            "before tang", "pre-tang", "prior to 618", "before 618",
            "han dynasty", "jin dynasty", "wei dynasty"
        ],
        "poet": [
            "demotion", "exiled", "forced out", "political exile",
            "banished", "demoted", "forced to leave", "removed from office"
        ],
    }

    found = 0
    for key, keywords in criteria_keywords.items():
        if any(kw in content_lower for kw in keywords):
            found += 1

    if found >= 4:
        return True, f"Found evidence for {found}/6 criteria"
    return False, f"Only found evidence for {found}/6 criteria (need >=4)"


def verify(wd):
    """Main verification function - v137."""
    print("=" * 70)
    print("| VERIFICATION: v137 - Link-Chain Exploration")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    all_passed = True

    # === CHECK 1: FESTIVAL SELECTION ===
    print("| " + "-" * 68)
    print("| CHECK 1: FESTIVAL SELECTION")
    print("| Valid answers: Shangsi Festival, Renri")
    print("| " + "-" * 68)

    festival_ok, festival_msg = check_festival_selection(text)

    if festival_ok:
        print(f"| [PASSED] {festival_msg}")
    else:
        print(f"| [FAILED] {festival_msg}")
        all_passed = False

    # === CHECK 2: <page_chain> URL COUNT ===
    print("| " + "-" * 68)
    print("| CHECK 2: <page_chain> URL COUNT (>=4 required)")
    print("| " + "-" * 68)

    url_count = count_urls_in_page_chain(text)
    page_chain_ok = url_count >= 4
    if page_chain_ok:
        print(f"| [PASSED] Found {url_count} URLs")
    else:
        print(f"| [FAILED] Only {url_count} URLs (need >=4)")
        all_passed = False

    # === CHECK 3: <reasoning> EVIDENCE ===
    print("| " + "-" * 68)
    print("| CHECK 3: <reasoning> EVIDENCE (>=4/6 criteria)")
    print("| " + "-" * 68)

    evidence_ok, evidence_msg = check_reasoning_evidence(text)
    if evidence_ok:
        print(f"| [PASSED] {evidence_msg}")
    else:
        print(f"| [FAILED] {evidence_msg}")
        all_passed = False

    # === FINAL RESULT ===
    print("=" * 70)

    if all_passed:
        print("| RESULT: SUCCESS [OK]")
        print("| - Festival selection: PASSED")
        print("| - <page_chain> URLs (>=4): PASSED")
        print("| - <reasoning> evidence (>=4/6): PASSED")
    else:
        print("| RESULT: FAILED [X]")
        print(f"| - Festival selection: {'PASSED' if festival_ok else 'FAILED'}")
        print(f"| - <page_chain> URLs (>=4): {'PASSED' if page_chain_ok else 'FAILED'}")
        print(f"| - <reasoning> evidence (>=4/6): {'PASSED' if evidence_ok else 'FAILED'}")
    print("=" * 70)

    return all_passed


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
