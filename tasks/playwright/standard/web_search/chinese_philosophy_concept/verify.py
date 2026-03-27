#!/usr/bin/env python3
"""
Verification for Daoist Concept Investigation (v42).
Correct answer: Xu (虚) - Emptiness/Void - State concept, personal cultivation

v42 Changes:
- Removed MIN_CONCEPT_PAGES check (no forced page count)
- Removed Stanford Encyclopedia forced visit check
- Removed investigation_log forced format check
- Simplified to core answer validation only
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct: Xu (emptiness, void - a STATE of being, personal cultivation, in Tao Te Ching)
CORRECT = {
    "xu", "hsu", "emptiness", "void", "vacuity", "emptied",
    "虚", "xū", "hsü", "voidness", "empty"
}

# Historical figures associated with Xu
HISTORICAL_FIGURES = {
    "laozi", "lao-tzu", "lao tzu", "老子", "lǎozǐ",
    "zhuangzi", "chuang-tzu", "chuang tzu", "庄子", "莊子", "zhuāngzǐ",
    "wang bi", "王弼", "wáng bì",
    "ge hong", "葛洪", "gě hóng"
}

# TRAP 1: Wuji - Primarily cosmological (Condition 2)
TRAP_WUJI = {
    "wuji", "wu-chi", "无极", "無極", "limitless", "ultimate nothingness",
    "wújí"
}

# TRAP 2: Taiji - Primarily cosmological (Condition 2)
TRAP_TAIJI = {
    "taiji", "t'ai-chi", "太极", "太極", "supreme ultimate", "tàijí"
}

# TRAP 3: De - Not a state concept (Condition 1)
TRAP_DE = {
    "de", "te", "德", "virtue", "power", "dé"
}

# TRAP 4: Qingjing - Later development, not in original TTC (Condition 3)
TRAP_QINGJING = {
    "qingjing", "ching-ching", "清静", "清靜", "clarity and stillness",
    "clarity", "stillness", "qīngjìng"
}

# TRAP 5: Ling - Not clearly a state concept (Condition 1)
TRAP_LING = {
    "ling", "靈", "灵", "spirit", "numinous", "líng"
}

# TRAP 6: Jing - Not standalone in TTC (Condition 3)
TRAP_JING = {
    "jing", "ching", "静", "靜", "stillness", "quietude", "jìng"
}

# TRAP 7: Tian - From Zhuangzi, not TTC (Condition 3)
TRAP_TIAN = {
    "tian", "t'ien", "恬", "tranquility", "contentment", "tián"
}

# TRAP 8: Chun - Not central in TTC (Condition 3)
TRAP_CHUN = {
    "chun", "ch'un", "淳", "purity", "simplicity", "chún"
}

# TRAP 9: Dan - Not central in TTC (Condition 3)
TRAP_DAN = {
    "dan", "tan", "澹", "serenity", "calmness", "dàn"
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


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Daoist Concept Investigation (v42)")
    print("|")
    print("| Criteria:")
    print("|   1. Nature: STATE (describes how things ARE)")
    print("|   2. Scope: NOT cosmological/metaphysical")
    print("|   3. Source: Must be in Tao Te Ching (cite chapter)")
    print("|   4. Usage: Associated with personal cultivation/meditation")
    print("|   5. History: Has associated historical figure")
    print("|")
    print("| Correct: Xu (虚) - State of emptiness/void")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]

    # Check 1: Answer tag present
    answer = extract_tag(text, "answer")
    if not answer:
        print("| [FAILED] No <answer> tag found")
        print("|          Format: <answer>[concept]</answer>")
        print("=" * 70)
        return False
    answer_lower = answer.lower()
    print(f"| [INFO] Answer: {answer[:100]}")

    # Check 2: Trap detection (PRIORITY: check traps before other validations)
    all_traps = [
        (TRAP_WUJI, "Wuji", "Fails Condition 2: Primarily cosmological"),
        (TRAP_TAIJI, "Taiji", "Fails Condition 2: Primarily cosmological"),
        (TRAP_DE, "De", "Fails Condition 1: Not a state concept"),
        (TRAP_QINGJING, "Qingjing", "Fails Condition 3: Not in original TTC"),
        (TRAP_LING, "Ling", "Fails Condition 1: Not clearly a state"),
        (TRAP_JING, "Jing", "Fails Condition 3: Not standalone in TTC"),
        (TRAP_TIAN, "Tian", "Fails Condition 3: From Zhuangzi, not TTC"),
        (TRAP_CHUN, "Chun", "Fails Condition 3: Not central in TTC"),
        (TRAP_DAN, "Dan", "Fails Condition 3: Not central in TTC"),
    ]

    for trap_set, trap_name, trap_reason in all_traps:
        for trap in trap_set:
            if trap in answer_lower:
                print(f"| [FAILED] Incorrect answer: {trap_name}")
                print(f"|          {trap_reason}")
                print("|          The correct concept satisfies ALL 5 conditions")
                print("=" * 70)
                return False

    # Check 3: Correct answer
    found_correct = False
    for correct in CORRECT:
        if correct in answer_lower:
            found_correct = True
            break

    if not found_correct:
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

    print("| [PASSED] Correct answer: Xu")
    print("|          State of emptiness / Void")
    print("|          Passes all 5 conditions:")
    print("|            1. Describes a STATE of being")
    print("|            2. NOT cosmological (personal cultivation)")
    print("|            3. Mentioned in Tao Te Ching")
    print("|            4. Associated with meditation practice")
    print("|            5. Has associated historical figures")
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
