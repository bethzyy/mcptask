#!/usr/bin/env python3
"""
Verification for Chinese Philosophy Concept Classification Task v6.
Correct answer: Ziran (自然) - Naturalness/Spontaneity

v6 Changes:
- Fixed TRAP_TIAN: removed bare "tian" to prevent false positives with "ziran"
- Added "wu" to TRAP_WU_WEI for standalone detection
- Aligned description.md candidate list with verify.py traps (added P'u)

v5 Design:
- Removed explicit hints about answer meaning
- 6 criteria with subtle distinctions
- Multi-condition trap: 6 layered traps
- TRAP 1: Wu Wei (about action/behavior, not metaphysical)
- TRAP 2: De (also Confucian, not uniquely Daoist)
- TRAP 3: Qi (predates Warring States period)
- TRAP 4: Tian (connected to political authority)
- TRAP 5: Yin-Yang (predates Warring States, multiple traditions)
- TRAP 6: P'u (metaphor, not metaphysical concept)
- STRICT: Must use <answer> tag (no fallback)
- Correct answer takes priority over trap mentions
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct: Ziran (naturalness/spontaneity)
CORRECT = {
    "ziran", "tzu-jan", "zìrán", "ziran naturalness",
    "ziran spontaneity", "naturalness daoism", "spontaneity daoism"
}

# TRAP 1: Wu Wei (about governance/action, not metaphysics)
TRAP_WU_WEI = {
    "wu wei", "wuwei", "wú wéi", "non-action", "non action",
    "inaction", "effortless action", "wu wei er wei",
    "wu"  # Standalone "wu" refers to non-action concept
}

# TRAP 2: De (also Confucian, not uniquely Daoist)
TRAP_DE = {
    "de virtue", "de power", "te virtue", "dé virtue",
    "daoist virtue", "taoist virtue"
}

# TRAP 3: Qi (predates Warring States)
TRAP_QI = {
    "qi energy", "qi chi", "ch'i energy", "qi cosmology",
    "qi metaphysical", "vital energy chinese"
}

# TRAP 4: Tian (connected to political authority)
# Note: Avoid bare "tian" to prevent false positives with "ziran"
TRAP_TIAN = {
    "tian concept", "tien concept", "heaven chinese philosophy",
    "mandate of heaven", "tianming", "tian ming", "tian heaven"
}

# TRAP 5: Yin-Yang (predates Warring States, multiple traditions)
TRAP_YINYANG = {
    "yin yang", "yinyang", "yin-yang", "yin and yang",
    "dual cosmic forces"
}

# TRAP 6: P'u (metaphor, not metaphysical concept)
TRAP_PU = {
    "p'u", "pu", "uncarved block", "uncut block",
    "raw silk", "simplicity daoist"
}


def get_work_dir():
    p = os.getenv("MCP_MESSAGES")
    if p and Path(p).exists():
        return Path(p).parent
    return Path(".")


def parse_messages(wd):
    """Parse messages and extract text."""
    f = wd / "messages.json"
    if not f.exists():
        return {"ok": False, "text": ""}

    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"| [ERROR] Failed to parse messages.json: {e}")
        return {"ok": False, "text": ""}

    text_parts = []

    for m in data:
        try:
            if m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))
        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts)}


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Chinese Philosophy Concept Classification (v5)")
    print("| Correct: Ziran (Naturalness/Spontaneity)")
    print("| Trap 1: Wu Wei (governance, not metaphysics)")
    print("| Trap 2: De (also Confucian)")
    print("| Trap 3: Qi (predates Warring States)")
    print("| Trap 4: Tian (political authority)")
    print("| Trap 5: Yin-Yang (predates, multiple traditions)")
    print("| Trap 6: P'u (metaphor, not metaphysical)")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]

    # Extract answer from <answer> tag
    answer = extract_tag(text, "answer")
    if not answer:
        print("| [FAILED] No <answer> tag found in output")
        print("|          You must output your answer in the format:")
        print("|          <answer>")
        print("|          [Concept name]")
        print("|          </answer>")
        print("=" * 70)
        return False

    answer_lower = answer.lower()
    print(f"| [INFO] Answer: {answer[:100]}")

    # Check correct answer and trap detection
    # Priority: if correct answer found, ignore trap mentions
    found_correct = False
    for correct in CORRECT:
        if correct in answer_lower:
            found_correct = True
            break

    if found_correct:
        print("| [PASSED] Correct answer: Ziran")
    else:
        # No correct answer found, check if trap was selected
        trap_found = None
        trap_reason = ""

        for trap in TRAP_WU_WEI:
            if trap in answer_lower:
                trap_found = "Wu Wei"
                trap_reason = "Wu Wei is about governance/action, not metaphysics"
                break

        if not trap_found:
            for trap in TRAP_DE:
                if trap in answer_lower:
                    trap_found = "De"
                    trap_reason = "De is also heavily used in Confucianism"
                    break

        if not trap_found:
            for trap in TRAP_QI:
                if trap in answer_lower:
                    trap_found = "Qi"
                    trap_reason = "Qi predates the Warring States period"
                    break

        if not trap_found:
            for trap in TRAP_TIAN:
                if trap in answer_lower:
                    trap_found = "Tian"
                    trap_reason = "Tian is connected to political authority (Mandate of Heaven)"
                    break

        if not trap_found:
            for trap in TRAP_YINYANG:
                if trap in answer_lower:
                    trap_found = "Yin-Yang"
                    trap_reason = "Yin-Yang predates Warring States and is found in multiple traditions"
                    break

        if not trap_found:
            for trap in TRAP_PU:
                if trap in answer_lower:
                    trap_found = "P'u"
                    trap_reason = "P'u is a metaphor (uncarved block), not a metaphysical concept"
                    break

        if trap_found:
            print(f"| [FAILED] TRAP: {trap_found} selected")
            print(f"|          {trap_reason}")
            print("|          Correct: Ziran (Naturalness/Spontaneity)")
            print("=" * 70)
            return False

        # Neither correct nor trap found
        print("| [FAILED] Correct answer not found")
        print("|          Expected: Ziran")
        print("|          The Daoist metaphysical concept about naturalness")
        print("=" * 70)
        return False

    print("| [PASSED] Did NOT select any traps")

    print("=" * 70)
    print("| RESULT: SUCCESS")
    print("| Model identified Ziran as the Daoist metaphysical concept")
    print("| Model correctly avoided all six traps")
    print("=" * 70)
    return True


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
