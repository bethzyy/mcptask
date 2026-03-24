#!/usr/bin/env python3
"""
Verification for Chinese Tea Classification Task v22.
Correct answer: Huangjin Gui - Golden Osmanthus

v22 Design:
- Requires 20+ Wikipedia page visits
- Fragrance trap: Osmanthus vs Orchid
- Tie Guan Yin = TRAP (has orchid, not osmanthus)
- STRICT: Must use <answer> tag (no fallback)
- CORRECT set narrowed to unique identifiers only (removed generic "golden osmanthus")
- Added more trap variations (tieguanyin tea, tianguanyin)
- Extract URLs from both tool outputs AND tool call arguments
- Fixed: Correct answer takes priority over trap mentions (model may explain reasoning)
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct: Huangjin Gui (only unique identifiers, avoid generic words like "golden")
CORRECT = {
    "huangjin gui", "huang jin gui", "huangjgui",
    "huangjingui"
}

# TRAP: Tie Guan Yin (orchid, not osmanthus)
TRAP_TIE_GUAN_YIN = {
    "tie guan yin", "ti kuan yin", "tieguanyin",
    "iron goddess", "iron bodhisattva", "tgy",
    "tieguanyin tea", "tianguanyin"
}

MIN_PAGES = 20


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

            # Also extract URLs from tool call arguments (e.g., browser_navigate)
            tool_calls = m.get("tool_calls", [])
            if isinstance(tool_calls, list):
                for tc in tool_calls:
                    if isinstance(tc, dict):
                        args = tc.get("function", {}).get("arguments", "")
                        if isinstance(args, str):
                            found = re.findall(r'https?://en\.wikipedia\.org/wiki/[^\s<>"\']+', args)
                            urls.update(found)
        except Exception as e:
            # Skip malformed message, continue processing
            continue

    return {"ok": True, "text": " ".join(text_parts), "urls": urls}


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chinese Tea Classification (v22)")
    print("| Correct: Huangjin Gui - Golden Osmanthus")
    print("| Trap: Tie Guan Yin - ORCHID fragrance, NOT osmanthus")
    print("| Requirement: 20+ Wikipedia pages + <answer> tag")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    urls = msgs["urls"]
    text_lower = text.lower()

    # Count unique Wikipedia pages
    unique_pages = len(urls)
    print(f"| [INFO] Unique Wikipedia pages visited: {unique_pages}")
    print(f"| [INFO] Required minimum: {MIN_PAGES}")
    print("| " + "-" * 68)

    # CHECK 1: Page count
    if unique_pages < MIN_PAGES:
        print(f"| [FAILED] Insufficient exploration: {unique_pages} < {MIN_PAGES} pages")
        print("|          You must visit at least 20 Wikipedia pages")
        print("=" * 70)
        return False
    print(f"| [PASSED] Page count: {unique_pages} >= {MIN_PAGES}")

    # Extract answer from <answer> tag
    answer = extract_tag(text, "answer")
    if not answer:
        print("| [FAILED] No <answer> tag found in output")
        print("|          You must output your answer in the format:")
        print("|          <answer>")
        print("|          [Tea name]")
        print("|          </answer>")
        print("=" * 70)
        return False

    answer_lower = answer.lower()
    print(f"| [INFO] Answer: {answer[:100]}")

    # CHECK 2 & 3: Correct answer and trap detection
    # Priority: if correct answer found, ignore trap mentions (model may explain reasoning)
    found_correct = False
    for correct in CORRECT:
        if correct in answer_lower:
            found_correct = True
            break

    if found_correct:
        print("| [PASSED] Correct answer: Huangjin Gui")
        # Even if trap is mentioned, we trust the correct answer is the choice
    else:
        # No correct answer found, check if trap was selected
        for trap in TRAP_TIE_GUAN_YIN:
            if trap in answer_lower:
                print(f"| [FAILED] TRAP: Tie Guan Yin selected")
                print("|          Tie Guan Yin has ORCHID fragrance")
                print("|          The answer must have OSMANTHUS fragrance")
                print("|          Correct: Huangjin Gui (Golden Osmanthus)")
                print("=" * 70)
                return False

        # Neither correct nor trap found
        print("| [FAILED] Correct answer not found")
        print("|          Expected: Huangjin Gui")
        print("|          The Anxi oolong with OSMANTHUS (not orchid) fragrance")
        print("=" * 70)
        return False

    print("| [PASSED] Did NOT select Tie Guan Yin as final answer")

    print("| " + "-" * 68)
    print("| [INFO] Wikipedia pages visited: {}".format(unique_pages))
    print("=" * 70)
    print("| RESULT: SUCCESS")
    print("| Model identified Huangjin Gui with Osmanthus fragrance")
    print("| Model correctly avoided Tie Guan Yin (orchid) trap")
    print("=" * 70)
    return True


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
