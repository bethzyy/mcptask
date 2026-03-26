#!/usr/bin/env python3
"""
Verification for Wikipedia Edit History Investigation v86.
Task: Find ORIGINAL authors who added oxidation, tea roller machine, AND drying/firing content to Tea_processing page.

v86 Design: Four Traps + Original Author Requirement + Three Different Editors + Checkpoints + Reliability Check
- Must find ORIGINAL authors, not recent editors (Trap 1)
- Must assess expertise, not just edit count (Trap 2)
- Must verify all THREE editors are DIFFERENT people (Trap 3)
- Must check for blocks/warnings on each editor (Trap 4)
- Must output checkpoints at phases 4, 8, and 12
- Minimum 20 turns required (reduced from 25 in v85)
- Must explain how each trap was avoided (4 traps)
- The three editors MUST be different people (key requirement)

Target page: https://en.wikipedia.org/wiki/Tea_processing
Target content #1: Tea oxidation/fermentation chemistry (originally by Sjschen, 2007)
Target content #2: Tea roller machines / mechanical rolling equipment (originally by Stephensalan79, 2022)
Target content #3: Drying/firing methods (requires investigation)
"""
import sys
import json
import os
import re
from pathlib import Path
from datetime import datetime

# Target page
TARGET_PAGE = "tea_processing"
TARGET_URL = "en.wikipedia.org/wiki/Tea_processing"

# Keywords for oxidation content
OXIDATION_KEYWORDS = [
    "oxidation", "enzymatic", "theaflavin", "thearubigin",
    "polyphenol", "fermentation", "catechin", "oxidize"
]

# Keywords for tea roller machine content
ROLLER_MACHINE_KEYWORDS = [
    "roller", "rotorvane", "rolling table", "orthodox",
    "mechanical rolling", "rolling process", "machine"
]

# Keywords for drying/firing content
DRYING_KEYWORDS = [
    "drying", "firing", "hot air", "moisture",
    "dryer", "temperature", "final drying", "oven"
]

# Minimum requirements
MIN_NAVIGATION_EVIDENCE = 15
MIN_TARGET_INFO_LENGTH = 50
MIN_REASONING_LENGTH = 80
MIN_TRAP_ANALYSIS_LENGTH = 30
MIN_CHECKPOINT_LENGTH = 20
MIN_TURNS = 20


def get_work_dir():
    p = os.getenv("MCP_MESSAGES")
    if p and Path(p).exists():
        return Path(p).parent
    return Path(".")


def parse_messages(wd):
    """Parse messages and extract text, tool calls, and count turns."""
    f = wd / "messages.json"
    if not f.exists():
        return {"ok": False, "text": "", "tool_calls": [], "urls": [], "turns": 0}

    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"| [ERROR] Failed to parse messages.json: {e}")
        return {"ok": False, "text": "", "tool_calls": [], "urls": [], "turns": 0}

    text_parts = []
    tool_calls = []
    urls_visited = []
    turns = 0
    seen_tool_call_ids = set()

    for m in data:
        try:
            role = m.get("role", "")

            if role == "assistant":
                turns += 1
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
                                args = i.get("input", {})
                                if "url" in args:
                                    urls_visited.append(args["url"].lower())
            elif role == "tool":
                content = m.get("content", "")
                if isinstance(content, str):
                    text_parts.append(content)

            elif "name" in m and "arguments" in m:
                call_id = m.get("call_id", m.get("id", ""))
                if call_id and call_id not in seen_tool_call_ids:
                    seen_tool_call_ids.add(call_id)
                    turns += 1

                tool_call = {
                    "name": m.get("name", ""),
                    "input": m.get("arguments", {})
                }
                tool_calls.append(tool_call)

                args = m.get("arguments", {})
                if isinstance(args, dict) and "url" in args:
                    urls_visited.append(args["url"].lower())

            elif m.get("type") == "tool_result" or ("call_id" in m and "output" in m):
                output = m.get("output", "")
                if isinstance(output, str):
                    text_parts.append(output)

        except Exception:
            continue

    if turns == 0 and tool_calls:
        turns = len(tool_calls)

    return {
        "ok": True,
        "text": " ".join(text_parts),
        "tool_calls": tool_calls,
        "urls": urls_visited,
        "turns": turns
    }


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}[^>]*>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def extract_subtag(content, tag):
    """Extract content from a sub-tag."""
    pattern = rf'<{tag}[^>]*>\s*(.*?)\s*</{tag}>'
    match = re.search(pattern, content, re.DOTALL | re.I)
    return match.group(1).strip() if match else ""


def check_view_history_accessed(tool_calls, urls, text):
    """Check if model accessed View history page."""
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("input", {}) or tc.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except:
                args = {}

        if name == "browser_navigate":
            url = args.get("url", "").lower() if isinstance(args, dict) else ""
            if "action=history" in url or "history" in url:
                return True, "Navigated to history page via URL"

        if name == "browser_click":
            element = str(args.get("element", "")).lower() if isinstance(args, dict) else ""
            text_content = str(args.get("text", "")).lower() if isinstance(args, dict) else ""
            if "history" in element or "history" in text_content:
                return True, "Clicked on history element"

    for url in urls:
        if "action=history" in url:
            return True, "History page URL detected"

    text_lower = text.lower()
    history_indicators = [
        "view history", "edit history", "revision history",
        "page history", "history tab", "action=history"
    ]
    for indicator in history_indicators:
        if indicator in text_lower:
            return True, f"History access mentioned in output"

    return False, "No evidence of View history access"


def check_wikiblame_used(tool_calls, urls, text):
    """Check if model used WikiBlame or 'Find addition/removal' tool."""
    # Check URLs for WikiBlame
    for url in urls:
        if "wikiblame" in url or "wikipedia.org/w/index.php?title=Special:" in url:
            return True, "WikiBlame or Special page accessed via URL"

    # Check tool calls
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("input", {}) or tc.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except:
                args = {}

        if name == "browser_navigate":
            url = args.get("url", "").lower() if isinstance(args, dict) else ""
            if "wikiblame" in url:
                return True, "Navigated to WikiBlame"
            if "special:" in url:
                return True, "Accessed Wikipedia Special page"

        if name == "browser_click":
            element = str(args.get("element", "")).lower() if isinstance(args, dict) else ""
            text_content = str(args.get("text", "")).lower() if isinstance(args, dict) else ""
            if "find addition" in element or "find addition" in text_content:
                return True, "Clicked 'Find addition/removal' link"
            if "wikiblame" in element or "wikiblame" in text_content:
                return True, "Clicked WikiBlame link"

    # Check text output
    text_lower = text.lower()
    wikiblame_indicators = [
        "wikiblame", "find addition", "find removal",
        "original author", "first added", "originally added",
        "who added", "when was this added"
    ]
    for indicator in wikiblame_indicators:
        if indicator in text_lower:
            return True, f"WikiBlame-related term found: '{indicator}'"

    return False, "No evidence of WikiBlame or 'Find addition/removal' tool usage"


def check_version_comparison(tool_calls, urls, text):
    """Check if model performed version comparison (diff)."""
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("input", {}) or tc.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except:
                args = {}

        if name == "browser_navigate":
            url = args.get("url", "").lower() if isinstance(args, dict) else ""
            if "diff=" in url or "oldid=" in url or "compare" in url:
                return True, "Navigated to diff/comparison page"

        if name == "browser_click":
            element = str(args.get("element", "")).lower() if isinstance(args, dict) else ""
            text_content = str(args.get("text", "")).lower() if isinstance(args, dict) else ""
            if "compare" in element or "compare" in text_content:
                return True, "Clicked compare element"
            if "radio" in element or "checkbox" in element or "select" in element:
                return True, f"Version selection detected: {element[:50]}"

    for url in urls:
        if "diff=" in url or ("oldid=" in url and "diff=" in url):
            return True, "Diff URL detected"

    text_lower = text.lower()
    diff_indicators = [
        "compare selected", "version comparison", "show changes",
        "diff=", "revision comparison", "difference between"
    ]
    for indicator in diff_indicators:
        if indicator in text_lower:
            return True, f"Comparison mentioned: {indicator}"

    return False, "No evidence of version comparison"


def check_editor_page_visited(tool_calls, urls, text):
    """Check if model visited editor's user page."""
    user_visits = 0
    for url in urls:
        if "user:" in url or "user_talk:" in url or "special:contributions" in url:
            user_visits += 1

    if user_visits >= 3:
        return True, f"Visited {user_visits} user pages"
    elif user_visits >= 2:
        return True, f"Visited {user_visits} user pages (partial)"

    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("input", {}) or tc.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except:
                args = {}

        if name == "browser_navigate":
            url = args.get("url", "").lower() if isinstance(args, dict) else ""
            if "user:" in url or "special:contributions" in url:
                return True, "Navigated to user page"

        if name == "browser_click":
            element = str(args.get("element", "")).lower() if isinstance(args, dict) else ""
            if "user:" in element or "contributions" in element:
                return True, "Clicked user link"

    text_lower = text.lower()
    user_indicators = ["user page", "contributions", "editor's page", "user profile"]
    for indicator in user_indicators:
        if indicator in text_lower:
            return True, f"User page mentioned: {indicator}"

    return False, "No evidence of visiting editor's user page"


def check_checkpoints(text):
    """Check if all three checkpoints are present."""
    report = extract_tag(text, "investigation_report")
    if not report:
        return {"ok": False, "reason": "No investigation report found"}

    checkpoints_found = []
    missing_checkpoints = []

    for i in range(1, 4):
        checkpoint = extract_subtag(report, f"checkpoint_{i}")
        if checkpoint:
            current_findings = extract_subtag(checkpoint, "current_findings")
            next_steps = extract_subtag(checkpoint, "next_steps")

            if len(current_findings) >= MIN_CHECKPOINT_LENGTH:
                checkpoints_found.append(i)
            else:
                missing_checkpoints.append(f"checkpoint_{i}: current_findings too short ({len(current_findings)} chars)")
        else:
            missing_checkpoints.append(f"checkpoint_{i}: not found")

    if len(checkpoints_found) == 3:
        return {
            "ok": True,
            "checkpoints_found": checkpoints_found,
            "message": "All three checkpoints present"
        }
    elif len(checkpoints_found) > 0:
        return {
            "ok": False,
            "reason": f"Only {len(checkpoints_found)}/3 checkpoints found: {missing_checkpoints}"
        }
    else:
        return {"ok": False, "reason": f"No checkpoints found: {missing_checkpoints}"}


def check_investigation_report(text):
    """Check if the investigation report has all required fields for v85."""
    report = extract_tag(text, "investigation_report")
    if not report:
        return {"ok": False, "reason": "No <investigation_report> block found"}

    # Check content 1 investigation
    content1 = extract_subtag(report, "content_1_investigation")
    if not content1:
        return {"ok": False, "reason": "No <content_1_investigation> found"}

    target_text1 = extract_subtag(content1, "target_text")
    editor1 = extract_subtag(content1, "editor_username")
    timestamp1 = extract_subtag(content1, "edit_timestamp")

    if len(target_text1) < MIN_TARGET_INFO_LENGTH:
        return {"ok": False, "reason": f"Content 1 target_text too short ({len(target_text1)} chars)"}
    if not editor1:
        return {"ok": False, "reason": "Content 1 editor_username missing"}
    if not timestamp1:
        return {"ok": False, "reason": "Content 1 edit_timestamp missing"}

    # Check reliability check for content 1
    reliability1 = extract_subtag(content1, "reliability_check")
    if not reliability1:
        return {"ok": False, "reason": "Content 1 reliability_check missing (required in v85)"}

    # Check content 2 investigation
    content2 = extract_subtag(report, "content_2_investigation")
    if not content2:
        return {"ok": False, "reason": "No <content_2_investigation> found"}

    target_text2 = extract_subtag(content2, "target_text")
    editor2 = extract_subtag(content2, "editor_username")
    timestamp2 = extract_subtag(content2, "edit_timestamp")

    if len(target_text2) < MIN_TARGET_INFO_LENGTH:
        return {"ok": False, "reason": f"Content 2 target_text too short ({len(target_text2)} chars)"}
    if not editor2:
        return {"ok": False, "reason": "Content 2 editor_username missing"}
    if not timestamp2:
        return {"ok": False, "reason": "Content 2 edit_timestamp missing"}

    # Check reliability check for content 2
    reliability2 = extract_subtag(content2, "reliability_check")
    if not reliability2:
        return {"ok": False, "reason": "Content 2 reliability_check missing (required in v85)"}

    # Check content 3 investigation (NEW in v85)
    content3 = extract_subtag(report, "content_3_investigation")
    if not content3:
        return {"ok": False, "reason": "No <content_3_investigation> found (required in v85)"}

    target_text3 = extract_subtag(content3, "target_text")
    editor3 = extract_subtag(content3, "editor_username")
    timestamp3 = extract_subtag(content3, "edit_timestamp")

    if len(target_text3) < MIN_TARGET_INFO_LENGTH:
        return {"ok": False, "reason": f"Content 3 target_text too short ({len(target_text3)} chars)"}
    if not editor3:
        return {"ok": False, "reason": "Content 3 editor_username missing (required in v85)"}
    if not timestamp3:
        return {"ok": False, "reason": "Content 3 edit_timestamp missing (required in v85)"}

    # Check reliability check for content 3
    reliability3 = extract_subtag(content3, "reliability_check")
    if not reliability3:
        return {"ok": False, "reason": "Content 3 reliability_check missing (required in v85)"}

    # Check editor comparison
    editor_comparison = extract_subtag(report, "editor_comparison")
    if not editor_comparison:
        return {"ok": False, "reason": "No <editor_comparison> found"}

    all_different = extract_subtag(editor_comparison, "all_different")
    verification_method = extract_subtag(editor_comparison, "verification_method")

    if not all_different:
        return {"ok": False, "reason": "all_different field missing in editor_comparison"}
    if not verification_method:
        return {"ok": False, "reason": "verification_method field missing in editor_comparison"}

    # Check credibility comparison
    comparison = extract_subtag(report, "credibility_comparison")
    if not comparison:
        return {"ok": False, "reason": "No <credibility_comparison> found"}

    more_reliable = extract_subtag(comparison, "most_reliable")
    reasoning = extract_subtag(comparison, "reasoning")
    editor3_name = extract_subtag(comparison, "editor_3_name")

    if not more_reliable:
        return {"ok": False, "reason": "most_reliable field missing in comparison"}
    if not editor3_name:
        return {"ok": False, "reason": "editor_3_name field missing in comparison (required in v85)"}
    if len(reasoning) < MIN_REASONING_LENGTH:
        return {"ok": False, "reason": f"Reasoning too short ({len(reasoning)} chars, need {MIN_REASONING_LENGTH})"}

    # Check trap analysis (now 4 traps in v85)
    trap_analysis = extract_subtag(report, "trap_analysis")
    if not trap_analysis:
        return {"ok": False, "reason": "No <trap_analysis> found"}

    trap1 = extract_subtag(trap_analysis, "trap_1_avoided")
    trap2 = extract_subtag(trap_analysis, "trap_2_avoided")
    trap3 = extract_subtag(trap_analysis, "trap_3_avoided")
    trap4 = extract_subtag(trap_analysis, "trap_4_avoided")

    if len(trap1) < MIN_TRAP_ANALYSIS_LENGTH:
        return {"ok": False, "reason": f"trap_1_avoided too short ({len(trap1)} chars, need {MIN_TRAP_ANALYSIS_LENGTH})"}
    if len(trap2) < MIN_TRAP_ANALYSIS_LENGTH:
        return {"ok": False, "reason": f"trap_2_avoided too short ({len(trap2)} chars, need {MIN_TRAP_ANALYSIS_LENGTH})"}
    if len(trap3) < MIN_TRAP_ANALYSIS_LENGTH:
        return {"ok": False, "reason": f"trap_3_avoided too short ({len(trap3)} chars, need {MIN_TRAP_ANALYSIS_LENGTH})"}
    if len(trap4) < MIN_TRAP_ANALYSIS_LENGTH:
        return {"ok": False, "reason": f"trap_4_avoided too short ({len(trap4)} chars, need {MIN_TRAP_ANALYSIS_LENGTH}) - required in v85"}

    # Check navigation evidence (increased to 15 in v85)
    nav_evidence = extract_subtag(report, "navigation_evidence")
    nav_items = len(re.findall(r'\d+\.', nav_evidence))
    if nav_items < MIN_NAVIGATION_EVIDENCE:
        return {"ok": False, "reason": f"Only {nav_items} navigation items (need {MIN_NAVIGATION_EVIDENCE})"}

    # Check investigation summary
    summary = extract_subtag(report, "investigation_summary")
    if not summary or len(summary) < 30:
        return {"ok": False, "reason": "investigation_summary missing or too short"}

    return {
        "ok": True,
        "editor1": editor1,
        "timestamp1": timestamp1,
        "editor2": editor2,
        "timestamp2": timestamp2,
        "editor3": editor3,
        "timestamp3": timestamp3,
        "all_different": all_different,
        "verification_method": verification_method,
        "most_reliable": more_reliable,
        "nav_items": nav_items,
        "trap1": trap1,
        "trap2": trap2,
        "trap3": trap3,
        "trap4": trap4
    }


def check_different_editors(text):
    """Check if model verified that all three editors are different.

    In v85, all THREE editors MUST be different people.
    """
    report = extract_tag(text, "investigation_report")
    if not report:
        return False, "No investigation report found"

    editor_comparison = extract_subtag(report, "editor_comparison")
    if not editor_comparison:
        return False, "No editor_comparison section"

    all_different = extract_subtag(editor_comparison, "all_different")
    verification_method = extract_subtag(editor_comparison, "verification_method")

    if not all_different:
        return False, "all_different field missing"

    all_different_lower = all_different.lower().strip()

    # Check for YES answer
    if all_different_lower in ["yes", "true", "different", "y", "all different"]:
        if len(verification_method) >= 10:
            return True, f"All editors confirmed different: {verification_method[:60]}..."
        else:
            return True, "All editors confirmed different (minimal verification)"

    # Check for NO answer - this is WRONG
    if all_different_lower in ["no", "false", "same", "n"]:
        return False, f"Editors are INCORRECTLY reported as same. They MUST all be different people."

    return True, f"Editor comparison provided: {all_different}"


def check_trap_analysis(text):
    """Check if trap analysis explains how all FOUR traps were avoided (v85)."""
    report = extract_tag(text, "investigation_report")
    if not report:
        return {"ok": False, "reason": "No investigation report found"}

    trap_analysis = extract_subtag(report, "trap_analysis")
    if not trap_analysis:
        return {"ok": False, "reason": "No trap_analysis section found"}

    trap1 = extract_subtag(trap_analysis, "trap_1_avoided")
    trap2 = extract_subtag(trap_analysis, "trap_2_avoided")
    trap3 = extract_subtag(trap_analysis, "trap_3_avoided")
    trap4 = extract_subtag(trap_analysis, "trap_4_avoided")

    issues = []

    if len(trap1) < MIN_TRAP_ANALYSIS_LENGTH:
        issues.append(f"Trap 1 analysis too short ({len(trap1)} chars)")
    if len(trap2) < MIN_TRAP_ANALYSIS_LENGTH:
        issues.append(f"Trap 2 analysis too short ({len(trap2)} chars)")
    if len(trap3) < MIN_TRAP_ANALYSIS_LENGTH:
        issues.append(f"Trap 3 analysis too short ({len(trap3)} chars)")
    if len(trap4) < MIN_TRAP_ANALYSIS_LENGTH:
        issues.append(f"Trap 4 analysis too short ({len(trap4)} chars) - required in v85")

    if issues:
        return {"ok": False, "reason": "; ".join(issues)}

    # Check for keywords indicating proper trap avoidance
    trap1_lower = trap1.lower()
    trap2_lower = trap2.lower()
    trap3_lower = trap3.lower()
    trap4_lower = trap4.lower()

    quality_indicators = []

    # Trap 1: Should mention original/first/wikiblame
    if any(kw in trap1_lower for kw in ["original", "first", "wikiblame", "addition", "earliest"]):
        quality_indicators.append("Trap 1: mentions finding original author")

    # Trap 2: Should mention expertise/topic/specialty
    if any(kw in trap2_lower for kw in ["expertise", "topic", "specialty", "quality", "subject"]):
        quality_indicators.append("Trap 2: mentions assessing expertise")

    # Trap 3: Should mention comparing/verifying/username
    if any(kw in trap3_lower for kw in ["compare", "verify", "username", "different", "same"]):
        quality_indicators.append("Trap 3: mentions verifying editors")

    # Trap 4: Should mention blocks/warnings/reliability
    if any(kw in trap4_lower for kw in ["block", "warning", "ban", "reliability", "user talk", "check"]):
        quality_indicators.append("Trap 4: mentions checking reliability")

    return {
        "ok": True,
        "trap1_len": len(trap1),
        "trap2_len": len(trap2),
        "trap3_len": len(trap3),
        "trap4_len": len(trap4),
        "quality_indicators": quality_indicators
    }


def check_content_relevance(target_text, content_type):
    """Check if target text is relevant to the content type."""
    target_lower = target_text.lower()

    if content_type == "oxidation":
        matches = [kw for kw in OXIDATION_KEYWORDS if kw in target_lower]
        return len(matches) >= 2, matches
    elif content_type == "roller":
        matches = [kw for kw in ROLLER_MACHINE_KEYWORDS if kw in target_lower]
        return len(matches) >= 2, matches
    elif content_type == "drying":
        matches = [kw for kw in DRYING_KEYWORDS if kw in target_lower]
        return len(matches) >= 2, matches

    return False, []


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Wikipedia Edit History Investigation v85")
    print("| Mission: Find ORIGINAL authors who added oxidation, roller machine,")
    print("|          AND drying/firing content to Tea_processing page")
    print("| Requirements:")
    print("|   1. Access View history tab")
    print("|   2. Use WikiBlame or 'Find addition/removal' tool")
    print("|   3. Perform version comparison")
    print("|   4. Visit ALL THREE editors' user pages")
    print("|   5. Verify all THREE editors are DIFFERENT people")
    print("|   6. Investigate THREE content pieces")
    print("|   7. Compare editor credibility")
    print("|   8. Check reliability (blocks/warnings) for each editor")
    print("|   9. Output checkpoints at phases 4, 8, and 12")
    print("|  10. Explain how ALL FOUR traps were avoided")
    print("|  11. Complete in >= 20 turns")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False
    text = msgs["text"]
    tool_calls = msgs["tool_calls"]
    urls = msgs["urls"]
    turns = msgs["turns"]

    # CHECK 0: Minimum turns requirement
    print("|")
    print("| [CHECK 0] Minimum Turns Requirement")

    if turns < MIN_TURNS:
        print(f"| [FAILED] Only {turns} turns (minimum required: {MIN_TURNS})")
        print("|          Task requires thorough investigation with multiple steps!")
        print("=" * 70)
        return False
    print(f"| [OK] Completed in {turns} turns (minimum: {MIN_TURNS})")

    # CHECK 1: View history access
    print("|")
    print("| [CHECK 1] View History Access")

    history_ok, history_reason = check_view_history_accessed(tool_calls, urls, text)
    if not history_ok:
        print(f"| [FAILED] {history_reason}")
        print("|          You MUST use the 'View history' tab to investigate edits!")
        print("=" * 70)
        return False
    print(f"| [OK] {history_reason}")

    # CHECK 2: WikiBlame usage
    print("|")
    print("| [CHECK 2] WikiBlame / 'Find addition/removal' Tool Usage")

    wikiblame_ok, wikiblame_reason = check_wikiblame_used(tool_calls, urls, text)
    if not wikiblame_ok:
        print(f"| [FAILED] {wikiblame_reason}")
        print("|          You MUST use WikiBlame or 'Find addition/removal' to find ORIGINAL authors!")
        print("=" * 70)
        return False
    print(f"| [OK] {wikiblame_reason}")

    # CHECK 3: Version comparison
    print("|")
    print("| [CHECK 3] Version Comparison (Diff)")

    diff_ok, diff_reason = check_version_comparison(tool_calls, urls, text)
    if not diff_ok:
        print(f"| [FAILED] {diff_reason}")
        print("|          You MUST compare versions to find who added content!")
        print("=" * 70)
        return False
    print(f"| [OK] {diff_reason}")

    # CHECK 4: Editor page visits
    print("|")
    print("| [CHECK 4] Editor Page Visits (3 editors)")

    editor_ok, editor_reason = check_editor_page_visited(tool_calls, urls, text)
    if not editor_ok:
        print(f"| [FAILED] {editor_reason}")
        print("|          You MUST visit all THREE editors' user pages to assess credibility!")
        print("=" * 70)
        return False
    print(f"| [OK] {editor_reason}")

    # CHECK 5: Checkpoints (NEW in v85)
    print("|")
    print("| [CHECK 5] Checkpoints Output")

    checkpoint_check = check_checkpoints(text)
    if not checkpoint_check["ok"]:
        print(f"| [FAILED] {checkpoint_check['reason']}")
        print("|          You MUST output checkpoints at phases 4, 8, and 12!")
        print("=" * 70)
        return False
    print(f"| [OK] {checkpoint_check['message']}")

    # CHECK 6: Different editors verification
    print("|")
    print("| [CHECK 6] Different Editors Verification (3 editors)")

    different_ok, different_reason = check_different_editors(text)
    if not different_ok:
        print(f"| [FAILED] {different_reason}")
        print("|          You MUST verify that all THREE editors are different people!")
        print("=" * 70)
        return False
    print(f"| [OK] {different_reason}")

    # CHECK 7: Trap analysis (4 traps in v85)
    print("|")
    print("| [CHECK 7] Trap Analysis (4 traps)")

    trap_check = check_trap_analysis(text)
    if not trap_check["ok"]:
        print(f"| [FAILED] {trap_check['reason']}")
        print("|          You MUST explain how you avoided ALL FOUR traps!")
        print("=" * 70)
        return False
    print(f"| [OK] Trap analysis provided:")
    print(f"|      - Trap 1 (Recent Editor): {trap_check['trap1_len']} chars")
    print(f"|      - Trap 2 (High-Frequency): {trap_check['trap2_len']} chars")
    print(f"|      - Trap 3 (Same Person): {trap_check['trap3_len']} chars")
    print(f"|      - Trap 4 (Unreliable Editor): {trap_check['trap4_len']} chars")
    if trap_check["quality_indicators"]:
        for indicator in trap_check["quality_indicators"]:
            print(f"|      - {indicator}")

    # CHECK 8: Investigation report structure
    print("|")
    print("| [CHECK 8] Investigation Report Structure")

    report_check = check_investigation_report(text)
    if not report_check["ok"]:
        print(f"| [FAILED] {report_check['reason']}")
        print("=" * 70)
        return False

    print("| [OK] All required fields present:")
    print(f"|      - Content 1 Editor: {report_check['editor1'][:40]}")
    print(f"|      - Content 1 Timestamp: {report_check['timestamp1'][:30]}")
    print(f"|      - Content 2 Editor: {report_check['editor2'][:40]}")
    print(f"|      - Content 2 Timestamp: {report_check['timestamp2'][:30]}")
    print(f"|      - Content 3 Editor: {report_check['editor3'][:40]}")
    print(f"|      - Content 3 Timestamp: {report_check['timestamp3'][:30]}")
    print(f"|      - All Different: {report_check['all_different']}")
    print(f"|      - Most reliable: {report_check['most_reliable'][:30]}")
    print(f"|      - Navigation items: {report_check['nav_items']}")

    # CHECK 9: Content relevance
    print("|")
    print("| [CHECK 9] Content Relevance")

    report = extract_tag(text, "investigation_report")
    content1 = extract_subtag(report, "content_1_investigation")
    content2 = extract_subtag(report, "content_2_investigation")
    content3 = extract_subtag(report, "content_3_investigation")
    target_text1 = extract_subtag(content1, "target_text")
    target_text2 = extract_subtag(content2, "target_text")
    target_text3 = extract_subtag(content3, "target_text")

    ox_ok, ox_matches = check_content_relevance(target_text1, "oxidation")
    roller_ok, roller_matches = check_content_relevance(target_text2, "roller")
    drying_ok, drying_matches = check_content_relevance(target_text3, "drying")

    if not ox_ok:
        print(f"| [WARNING] Content 1 may not be about oxidation")
    else:
        print(f"| [OK] Content 1 contains oxidation keywords: {ox_matches}")

    if not roller_ok:
        print(f"| [WARNING] Content 2 may not be about tea roller machines")
    else:
        print(f"| [OK] Content 2 contains roller machine keywords: {roller_matches}")

    if not drying_ok:
        print(f"| [WARNING] Content 3 may not be about drying/firing")
    else:
        print(f"| [OK] Content 3 contains drying keywords: {drying_matches}")

    # CHECK 10: Credibility reasoning quality
    print("|")
    print("| [CHECK 10] Credibility Reasoning")

    comparison = extract_subtag(report, "credibility_comparison")
    reasoning = extract_subtag(comparison, "reasoning")
    reasoning_lower = reasoning.lower()
    quality_indicators = ["edit", "account", "experience", "contribution", "expertise", "reliable", "history", "block", "warning"]

    mentioned = [ind for ind in quality_indicators if ind in reasoning_lower]
    if len(mentioned) < 2:
        print(f"| [WARNING] Reasoning could be more detailed")
    else:
        print(f"| [OK] Reasoning mentions quality factors: {mentioned}")

    print("|")
    print(f"| Content 1 Editor: {report_check['editor1']}")
    print(f"| Content 2 Editor: {report_check['editor2']}")
    print(f"| Content 3 Editor: {report_check['editor3']}")
    print(f"| All Different: {report_check['all_different']}")
    print(f"| Most Reliable: {report_check['most_reliable']}")
    print("|")
    print("|" + "-" * 68)
    print("| RESULT: SUCCESS")
    print("| All verification checks passed!")
    print("=" * 70)
    return True


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
