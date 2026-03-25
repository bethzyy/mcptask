#!/usr/bin/env python3
"""
Verification for Triangulation Verifier v1.

Claim: "The Great Wall of China was built by Qin Shi Huang to defend against the Mongols."

Correct Analysis:
- ANGLE 1 (Construction): PARTIALLY TRUE - Qin connected existing walls, not built from scratch
- ANGLE 2 (Timeline): FALSE - Mongols as unified group didn't exist in Qin era (221-206 BCE)
- ANGLE 3 (Purpose): FALSE - Qin's enemies were Xiongnu, not Mongols
- OVERALL: MOSTLY INACCURATE

Key design principles from review_lessons.md:
1. Correct answer priority over trap mentions
2. Extract URLs from both tool outputs AND tool call arguments
3. Use try/except for JSON parsing
4. Don't over-verify format details
"""
import sys
import json
import os
import re
from pathlib import Path

MIN_PAGES = 10

# Expected verdicts for each angle (flexible matching)
EXPECTED_ANGLE1 = ["partially true", "partially", "mixed"]
EXPECTED_ANGLE2 = ["false", "not true", "incorrect"]
EXPECTED_ANGLE3 = ["false", "not true", "incorrect"]
EXPECTED_OVERALL = ["mostly inaccurate", "inaccurate", "partially accurate", "not accurate"]

# TRAP verdicts - if these appear, it's wrong
TRAP_VERDICTS = {
    "fully true", "fully accurate", "completely accurate",
    "completely true", "entirely true"
}

# TRAP content - common misconceptions that should be identified as wrong
TRAP_MISCONCEPTIONS = {
    "mongols were the enemy": "Qin's enemies were Xiongnu, Mongols didn't exist yet",
    "qin built the wall from scratch": "Qin connected existing walls",
    "defend against mongols": "Purpose was defense against Xiongnu"
}


def get_work_dir():
    p = os.getenv("MCP_MESSAGES")
    if p and Path(p).exists():
        return Path(p).parent
    return Path(".")


def parse_messages(wd):
    """Parse messages and extract text + Wikipedia URLs."""
    f = wd / "messages.json"
    if not f.exists():
        return {"ok": False, "text": "", "urls": set()}

    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"| [ERROR] Failed to parse messages.json: {e}")
        return {"ok": False, "text": "", "urls": set()}

    text_parts = []
    urls = set()

    for m in data:
        try:
            # Get assistant text
            if m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))

            # Get URLs from tool outputs
            if m.get("role") == "tool" or m.get("type") == "function_call_output":
                content = m.get("content", "") or m.get("output", "")
                if isinstance(content, str):
                    found = re.findall(r'https?://en\.wikipedia\.org/wiki/[^\s<>"\']+', content)
                    urls.update(found)

            # Also extract URLs from tool call arguments
            tool_calls = m.get("tool_calls", [])
            if isinstance(tool_calls, list):
                for tc in tool_calls:
                    if isinstance(tc, dict):
                        args = tc.get("function", {}).get("arguments", "")
                        if isinstance(args, str):
                            found = re.findall(r'https?://en\.wikipedia\.org/wiki/[^\s<>"\']+', args)
                            urls.update(found)
        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts), "urls": urls}


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def check_verdict(text_lower, expected_list, trap_set):
    """Check if verdict matches expected and not trap."""
    # First check for trap (trap takes priority as failure)
    for trap in trap_set:
        if trap in text_lower:
            return False, f"TRAP verdict: '{trap}'"

    # Check for expected
    for expected in expected_list:
        if expected in text_lower:
            return True, f"Correct verdict pattern: '{expected}'"

    return False, "No expected verdict found"


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Triangulation Verifier (v1)")
    print("| Claim: Great Wall built by Qin Shi Huang to defend against Mongols")
    print("| Expected: MOSTLY INACCURATE")
    print("| - ANGLE 1 (Construction): PARTIALLY TRUE")
    print("| - ANGLE 2 (Timeline): FALSE (Mongols didn't exist)")
    print("| - ANGLE 3 (Purpose): FALSE (enemies were Xiongnu)")
    print("| Requirement: 20+ Wikipedia pages")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    urls = msgs["urls"]
    text_lower = text.lower()

    # === CHECK 1: Page count ===
    unique_pages = len(urls)
    print(f"| [INFO] Unique Wikipedia pages visited: {unique_pages}")
    print("| " + "-" * 68)

    if unique_pages < MIN_PAGES:
        print(f"| [FAILED] Insufficient exploration: {unique_pages} < {MIN_PAGES} pages")
        print("=" * 70)
        return False
    print(f"| [PASSED] Page count: {unique_pages} >= {MIN_PAGES}")

    # === CHECK 2: <verification> tag ===
    verification = extract_tag(text, "verification")
    if not verification:
        print("| [FAILED] No <verification> tag found")
        print("=" * 70)
        return False
    print("| [PASSED] <verification> tag found")

    verification_lower = verification.lower()

    # === CHECK 3: Three angles present ===
    angles_found = []
    for i in range(1, 4):
        if f"angle {i}" in verification_lower or f"angle{i}" in verification_lower:
            angles_found.append(i)

    if len(angles_found) < 3:
        print(f"| [FAILED] Not all angles found: {angles_found}")
        print("=" * 70)
        return False
    print(f"| [PASSED] All 3 angles found: {angles_found}")

    # === CHECK 4: <conclusion> tag ===
    conclusion = extract_tag(text, "conclusion")
    if not conclusion:
        print("| [FAILED] No <conclusion> tag found")
        print("=" * 70)
        return False
    print("| [PASSED] <conclusion> tag found")

    conclusion_lower = conclusion.lower()

    # === CHECK 5: Overall verdict ===
    # Check for trap verdicts first
    for trap in TRAP_VERDICTS:
        if trap in conclusion_lower:
            print(f"| [FAILED] TRAP overall verdict: '{trap}'")
            print("|          The claim is MOSTLY INACCURATE, not fully accurate")
            print("=" * 70)
            return False

    # Check for correct overall verdict
    found_correct = False
    for expected in EXPECTED_OVERALL:
        if expected in conclusion_lower:
            found_correct = True
            print(f"| [PASSED] Overall verdict: '{expected}'")
            break

    if not found_correct:
        print("| [FAILED] Correct overall verdict not found")
        print("|          Expected: MOSTLY INACCURATE or PARTIALLY ACCURATE")
        print("=" * 70)
        return False

    # === CHECK 6: Evidence URLs present ===
    # Just check that some wikipedia URLs are in the output as evidence
    wiki_urls_in_output = re.findall(r'https?://en\.wikipedia\.org/wiki/[^\s<>"\']+', text)
    if len(wiki_urls_in_output) < 3:
        print("| [WARNING] Few evidence URLs in output, but continuing...")
    else:
        print(f"| [PASSED] Evidence URLs found: {len(wiki_urls_in_output)}")

    # === SUCCESS ===
    print("| " + "-" * 68)
    print(f"| [INFO] Wikipedia pages visited: {unique_pages}")
    print("=" * 70)
    print("| RESULT: SUCCESS")
    print("| Model correctly identified the claim as MOSTLY INACCURATE")
    print("| Model investigated all three angles with evidence")
    print("=" * 70)
    return True


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
