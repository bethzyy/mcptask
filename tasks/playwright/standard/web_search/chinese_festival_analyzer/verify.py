#!/usr/bin/env python3
"""
Verification script for v114 - Open Exploration.
Checks: 20+ turns, correct festival selection, 5/5 conditions verified.
v114: Removed candidate list for open exploration, kept trap warnings.
"""
import sys
import json
import os
import re
from pathlib import Path

# === CONFIGURATION ===
MIN_TURNS = 20


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    m = re.search(rf'<{tag}>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return m.group(1).strip() if m else None

# Correct festival answers
CORRECT_FESTIVALS = {
    "shangsi", "double third", "shangsi festival", "上巳", "上巳节",
    "renri", "human day", "人日", "人日节",
}

# Trap keywords - if these appear in the Festival line, it's wrong
TRAP_KEYWORDS = {
    "dragon boat", "duanwu", "端午节", "zongzi", "qu yuan", "屈原",
    "qingming", "清明节", "qingtuan", "青团",
    "lantern", "元宵节", "yuanxiao", "元宵",
    "mid-autumn", "中秋节", "mooncake", "月饼",
}

# Suicide indicators - demotion must NOT be suicide
SUICIDE_INDICATORS = {
    "suicide", "drowned", "投江", "278 bc", "miluo river", "汨罗江",
    "自沉", "自杀",
}

# Demotion indicators
DEMOTION_INDICATORS = {
    "demoted", "exile", "banished", "贬谪", "贬", "demotion",
    "governor", "刺史", "左迁", "流放",
}

# Condition verification keywords (at least one from each group must appear)
CONDITION_KEYWORDS = {
    "food_color": ["green", "青", "绿色", "翠绿"],
    "food_taste": ["savory", "bitter", "咸", "苦", "not sweet", "非甜", "药", "herb"],
    "symbolism": ["health", "健康", "purification", "净化", "warding off", "驱邪", "辟邪"],
    "region": ["jiangnan", "江南", "north china", "华北", "北方"],
    "era": ["pre-tang", "tang dynasty", "唐代", "han", "汉", "jin", "晋", "zhou", "周", "618"],
    "demotion": ["demoted", "exile", "banished", "贬谪", "贬", "demotion"],
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


def count_documented_turns(text):
    """Count documented turns (=== TURN N === pattern)."""
    turn_pattern = r'===\s*TURN\s+(\d+)\s*==='
    turns = re.findall(turn_pattern, text, re.IGNORECASE)
    if turns:
        return len(set(int(t) for t in turns))

    # Alternative pattern
    turn_pattern2 = r'Turn\s+(\d+):'
    turns2 = re.findall(turn_pattern2, text, re.IGNORECASE)
    if turns2:
        return len(set(int(t) for t in turns2))

    return 0


def count_actual_turns(raw_msgs):
    """Count actual assistant turns in messages."""
    return sum(1 for m in raw_msgs if m.get("role") == "assistant")


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
        r'\*\*Festival:\*\*\s*(.+?)(?:\n|$)',  # Markdown bold
        r'Festival name:\s*(.+?)(?:\n|$)',
        r'Answer:\s*(.+?)(?:\n|$)',  # Catch "Final Answer:" format
    ]

    for pattern in festival_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            festival_line = m.group(1).strip().lower()
            # Clean up markdown formatting and extra text
            festival_line = re.sub(r'\*\*', '', festival_line)
            festival_line = re.sub(r'\s*\(.*?\)', '', festival_line)  # Remove parenthetical text
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


def check_demotion_event(text):
    """Check for demotion event (not suicide) - ONLY in final answer, not reasoning.

    IMPORTANT: This only checks the <answer> tag to avoid false positives from
    the model's reasoning process where it correctly identifies traps.
    """
    # Extract only the final answer content
    answer_content = extract_tag(text, "answer")

    if answer_content:
        # Only check suicide indicators in the final answer
        answer_lower = answer_content.lower()

        # Check for suicide indicators in answer - if found, it's wrong
        for s in SUICIDE_INDICATORS:
            if s in answer_lower:
                return False, f"Suicide detected in <answer>: {s}"

        # Check for demotion indicators in answer
        found_demotion = [d for d in DEMOTION_INDICATORS if d in answer_lower]
        if found_demotion:
            return True, f"Demotion found in <answer>: {found_demotion[:3]}"

        # If answer exists but no demotion/suicide keywords, that's acceptable
        # (the model may have chosen a festival without a demotion connection)
        return True, "No suicide indicators in <answer> (acceptable)"

    # Fallback: If no <answer> tag, check for festival line patterns
    text_lower = text.lower()
    festival_patterns = [
        r'Festival:\s*(.+?)(?:\n|$)',
        r'Selected Festival:\s*(.+?)(?:\n|$)',
        r'Final Festival:\s*(.+?)(?:\n|$)',
        r'\*\*Festival:\*\*\s*(.+?)(?:\n|$)',
    ]

    for pattern in festival_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            festival_line = m.group(1).strip().lower()

            # Only check suicide in this specific line
            for s in SUICIDE_INDICATORS:
                if s in festival_line:
                    return False, f"Suicide detected in festival line: {s}"

            return True, "No suicide indicators in festival line (acceptable)"

    # No answer found at all - but don't fail here, let other checks handle it
    return True, "No <answer> tag found, but no suicide indicators either"


def check_condition_coverage(text):
    """Check if all 6 conditions are addressed in the output."""
    text_lower = text.lower()
    results = {}

    for condition, keywords in CONDITION_KEYWORDS.items():
        found = [kw for kw in keywords if kw in text_lower]
        results[condition] = {
            "found": len(found) > 0,
            "keywords": found[:3]
        }

    return results


def verify(wd):
    """Main verification function."""
    print("=" * 70)
    print("| VERIFICATION: v114 - Open Exploration")
    print(f"| Required: {MIN_TURNS}+ turns, correct festival, 5/5 conditions")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    raw = msgs["raw"]

    ok = True

    # === 1. TURN COUNT CHECK ===
    print("| " + "-" * 68)
    print("| [1/5] TURN COUNT CHECK")
    print(f"| Required: {MIN_TURNS}+ turns")

    documented_turns = count_documented_turns(text)
    actual_turns = count_actual_turns(raw)
    effective_turns = max(documented_turns, actual_turns)

    print(f"| Documented turns: {documented_turns}")
    print(f"| Actual turns: {actual_turns}")
    print(f"| Effective turns: {effective_turns}")

    if effective_turns < MIN_TURNS:
        print(f"| [FAILED] Only {effective_turns} turns (need {MIN_TURNS}+)")
        ok = False
    else:
        print(f"| [PASSED] {effective_turns} turns")

    # === 2. FESTIVAL SELECTION CHECK ===
    print("| " + "-" * 68)
    print("| [2/5] FESTIVAL SELECTION CHECK")

    festival_ok, festival_msg = check_festival_selection(text)
    if festival_ok:
        print(f"| [PASSED] {festival_msg}")
    else:
        print(f"| [FAILED] {festival_msg}")
        ok = False

    # === 3. DEMOTION EVENT CHECK ===
    print("| " + "-" * 68)
    print("| [3/5] DEMOTION EVENT CHECK (Condition 6)")

    demotion_ok, demotion_msg = check_demotion_event(text)
    if demotion_ok:
        print(f"| [PASSED] {demotion_msg}")
    else:
        print(f"| [FAILED] {demotion_msg}")
        ok = False

    # === 4. CONDITION COVERAGE CHECK ===
    print("| " + "-" * 68)
    print("| [4/5] CONDITION COVERAGE CHECK (Conditions 1-5)")

    # Try to extract from <reasoning> tag first
    reasoning_content = extract_tag(text, "reasoning") or text
    condition_results = check_condition_coverage(reasoning_content)
    conditions_passed = 0
    for condition, result in condition_results.items():
        status = "[OK]" if result["found"] else "[X]"
        keywords = result["keywords"] if result["found"] else ["none"]
        print(f"|   {status} {condition}: {keywords}")
        if result["found"]:
            conditions_passed += 1

    # Require 5/5 conditions (excluding demotion which is checked separately)
    other_conditions = {k: v for k, v in condition_results.items() if k != "demotion"}
    other_passed = sum(1 for v in other_conditions.values() if v["found"])
    missing_conditions = [k for k, v in other_conditions.items() if not v["found"]]

    if other_passed == 5:
        print(f"| [PASSED] {other_passed}/5 conditions verified")
    else:
        print(f"| [FAILED] Only {other_passed}/5 conditions verified (need 5/5)")
        print(f"|   Missing: {missing_conditions}")
        ok = False

    # === 5. TRAP AVOIDANCE CHECK ===
    print("| " + "-" * 68)
    print("| [5/5] TRAP AVOIDANCE CHECK")

    text_lower = text.lower()
    traps_found = [t for t in TRAP_KEYWORDS if t in text_lower]

    if traps_found:
        # Check if traps are mentioned in context of avoiding them
        trap_context_ok = True
        for trap in traps_found:
            # Look for patterns like "avoid dragon boat" or "dragon boat is wrong"
            trap_pattern = rf'(avoid|not|wrong|trap|incorrect).{{0,50}}{re.escape(trap)}|{re.escape(trap)}.{{0,50}}(avoid|not|wrong|trap|incorrect)'
            if not re.search(trap_pattern, text_lower):
                # Trap mentioned without avoidance context
                trap_context_ok = False
                break

        if trap_context_ok:
            print(f"| [PASSED] Traps mentioned but correctly identified as wrong")
        else:
            print(f"| [WARNING] Potential trap keywords found: {traps_found[:3]}")
    else:
        print(f"| [PASSED] No trap keywords found")

    # === FINAL RESULT ===
    print("=" * 70)
    if ok:
        print("| RESULT: SUCCESS [OK]")
        print(f"| Turns: {effective_turns}")
        print(f"| Conditions: {other_passed}/5 verified")
        print("=" * 70)
        return True
    else:
        print("| RESULT: FAILED [X]")
        print("=" * 70)
        return False


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
