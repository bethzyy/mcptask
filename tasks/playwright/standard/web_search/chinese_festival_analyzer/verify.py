#!/usr/bin/env python3
"""
Verification script for v127 - Link-Chain Exploration.
Checks:
1. Correct festival selection in <answer> tag
2. No trap keywords in answer

Note: Page count is only a description requirement, NOT verified here.
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

# Trap keywords - if these appear in the answer, it's wrong
TRAP_KEYWORDS = {
    "dragon boat", "duanwu", "qu yuan",
    "cold food", "hanshi", "jie zitui",
    "qingming", "qingtuan",
    "lantern", "yuanxiao",
    "mid-autumn", "mooncake",
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
        # Check for trap keywords in answer
        answer_lower = answer_content.lower()
        for trap in TRAP_KEYWORDS:
            if trap in answer_lower:
                return False, f"Trap detected in <answer>: selected '{trap}'"

        # Check for correct festival in answer
        for correct in CORRECT_FESTIVALS:
            if correct in answer_lower:
                return True, f"Correct festival in <answer>: {correct}"

        return False, f"No valid festival found in <answer>: {answer_content[:100]}"

    # Fallback: Look for festival line in answer - multiple possible formats
    text_lower = text.lower()
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

            # Check for trap keywords
            for trap in TRAP_KEYWORDS:
                if trap in festival_line:
                    return False, f"Trap detected: selected '{trap}'"

            # Check for correct festival
            for correct in CORRECT_FESTIVALS:
                if correct in festival_line or festival_line in correct:
                    return True, f"Correct festival: {correct}"

    return False, "No valid festival found in output"


def check_output_format(text):
    """Loose check for output format tags (INFO only, does not affect pass/fail)."""
    results = {}

    # Check <answer> tag
    answer = extract_tag(text, "answer")
    results["answer_tag"] = answer is not None

    # Check <page_chain> tag
    page_chain = extract_tag(text, "page_chain")
    results["page_chain_tag"] = page_chain is not None

    # Check <reasoning> tag
    reasoning = extract_tag(text, "reasoning")
    results["reasoning_tag"] = reasoning is not None

    return results


def verify(wd):
    """Main verification function - v127."""
    print("=" * 70)
    print("| VERIFICATION: v127 - Link-Chain Exploration")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]

    # === CHECK: FESTIVAL SELECTION (CRITICAL) ===
    print("| " + "-" * 68)
    print("| FESTIVAL SELECTION CHECK (CRITICAL)")
    print("| Correct answers: Shangsi Festival, Renri")
    print("| Traps: Dragon Boat, Cold Food, Qingming, Lantern, Mid-Autumn")
    print("| " + "-" * 68)

    festival_ok, festival_msg = check_festival_selection(text)

    if festival_ok:
        print(f"| [PASSED] {festival_msg}")
    else:
        print(f"| [FAILED] {festival_msg}")

    # === CHECK: OUTPUT FORMAT (INFO ONLY) ===
    print("| " + "-" * 68)
    print("| OUTPUT FORMAT CHECK (INFO ONLY - does not affect pass/fail)")
    print("| " + "-" * 68)

    format_results = check_output_format(text)

    for tag_name, found in format_results.items():
        status = "[OK]" if found else "[MISSING]"
        print(f"| {status} <{tag_name.replace('_tag', '')}> tag")

    # === FINAL RESULT ===
    print("=" * 70)

    if festival_ok:
        print("| RESULT: SUCCESS [OK]")
        print("| - Festival selection: PASSED")
    else:
        print("| RESULT: FAILED [X]")
        print("| - Festival selection: FAILED")
    print("=" * 70)

    return festival_ok


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
