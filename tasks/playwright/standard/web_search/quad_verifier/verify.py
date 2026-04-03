#!/usr/bin/env python3
"""
Verification for Wikipedia Framework Release Investigator (v71).

Task: Investigate Wikipedia edit history to find the original editor who first
added "Initial release" info for 4 JS frameworks, and determine which was added first.

v71 changes:
- Clarified "to the article" → "to that framework's own Wikipedia article" to eliminate
  ambiguity with the Comparison page (which caused 75% of failures on Vue.js date)

Key principle: verify.py checks "final answer correctness + key investigation evidence"
"""
import sys
import json
import os
import re
import datetime
from pathlib import Path

# Required frameworks to investigate
REQUIRED_FRAMEWORKS = ["react", "vue", "angular", "svelte"]

# Framework URL patterns for history page detection
# Use word boundaries to avoid substring false positives (e.g., "react" matching "reactive")
FRAMEWORK_URL_PATTERNS = {
    # Use lookbehind/lookahead instead of \b to handle underscores in Wikipedia titles
    # e.g. "React_(software)" — underscore is a word char, so \b fails after "React"
    "react": [r'(?<![a-z])react(?!ive)', r'(?<![a-z])reactjs'],
    "vue": [r'(?<![a-z])vue\.js', r'(?<![a-z])vuejs', r'(?<![a-z])vue(?![a-z])'],
    "angular": [r'(?<![a-z])angular(?!js)', r'(?<![a-z])angularjs'],
    "svelte": [r'(?<![a-z])svelte(?![a-z])'],
}

# Mapping from framework display names to label keys
FRAMEWORK_LABEL_MAP = {
    "react": "react",
    "vue.js": "vue",
    "vue": "vue",
    "angular": "angular",
    "svelte": "svelte",
}

# Wikipedia URL patterns
HISTORY_PATTERN = re.compile(r'action=history', re.I)
PAGE_URL_PATTERN = re.compile(r'Page URL:\s*(https?://[^\s]+)', re.I)

# Known wrong authors — framework creators, not Wikipedia editors
FRAMEWORK_CREATORS = {
    'dan abramov', 'jordan walke', 'evan you', 'misko hevery',
    'rich harris', 'ryan carniato',
}

# Placeholder / invalid author patterns
INVALID_AUTHORS = {
    'unknown', 'n/a', 'none', 'todo', 'tbd', 'test', 'example',
    'facebook', 'google', 'microsoft', 'wikipedia', 'admin',
    'anonymous', 'editor', 'contributor', 'user',
}

# Ground truth — answers verified against these values
GROUND_TRUTH = {
    'first_framework': 'react',
    'first_author': 'Patcito',
    'first_date': '2015-01-02',
    'react_date': '2015-01-02',
    'vue_date': '2017-03-05',
    'angular_date': '2017-03-05',
    'svelte_date': '2019-12-19',
}


def get_work_dir():
    p = os.getenv("MCP_MESSAGES")
    if p and Path(p).exists():
        return Path(p).parent
    return Path(".")


def get_ground_truth():
    """Return ground truth answers (inlined, no external file)."""
    return dict(GROUND_TRUTH)


def parse_messages(wd):
    """Parse messages.json to extract text and tool calls."""
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
            if m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))

            if "name" in m and m.get("type") == "function_call":
                tool_name = m.get("name", "")
                args_str = m.get("arguments", "{}")
                try:
                    args = json.loads(args_str) if isinstance(args_str, str) else args_str
                except json.JSONDecodeError:
                    args = {}
                tool_calls.append({"name": tool_name, "input": args})

            if m.get("type") == "function_call_output":
                output = m.get("output", "")
                if output:
                    tool_calls.append({"name": "output", "result": output})

        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts), "tool_calls": tool_calls}


def extract_urls(tool_calls):
    """Extract all URLs from tool calls (both input and output)."""
    urls = []
    for call in tool_calls:
        if "input" in call:
            inp = call["input"]
            if isinstance(inp, dict):
                url = inp.get("url", "")
                if url:
                    urls.append(url)
        if "result" in call:
            result = call["result"]
            if isinstance(result, str):
                for match in PAGE_URL_PATTERN.finditer(result):
                    urls.append(match.group(1))
    return urls


def check_history_evidence(urls):
    """Check how many frameworks had their history pages visited or diff/oldid pages accessed."""
    frameworks_found = set()
    diff_pattern = re.compile(r'(?:oldid|diff)=', re.I)
    for url in urls:
        # Check both history pages and diff/oldid pages
        is_history = HISTORY_PATTERN.search(url)
        is_diff = diff_pattern.search(url)
        if is_history or is_diff:
            url_lower = url.lower()
            for fw, patterns in FRAMEWORK_URL_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, url_lower, re.I):
                        frameworks_found.add(fw)
                        break
    return frameworks_found


def check_investigation_evidence(tool_calls):
    """Check if the model used investigation tools (history search, filter, WikiBlame).

    Evidence: URLs with qs= (history search), filter parameters, WikiBlame,
    diff/oldid URLs, clicks on revision/diff links, or tool inputs containing 'Initial release'.
    """
    found = False
    for call in tool_calls:
        if "input" in call:
            inp = call["input"]
            if isinstance(inp, dict):
                url = inp.get("url", "")

                # Wikipedia history search: action=history&qs=...
                if url and 'action=history' in url.lower() and 'qs=' in url.lower():
                    found = True
                    break

                # Filter revisions: filter parameter in history URL
                if url and re.search(r'action=history.*filter|filter.*action=history', url, re.I):
                    found = True
                    break

                # Diff/oldid URL (direct navigation to a diff page)
                if url and re.search(r'(?:oldid|diff)=', url, re.I):
                    found = True
                    break

                # WikiBlame external tool
                if url and 'wikiblame' in url.lower():
                    found = True
                    break

                # browser_type with "Initial release" text
                text_val = inp.get("text", "") or inp.get("value", "") or ""
                if "initial release" in text_val.lower():
                    found = True
                    break

                # Click on filter-related elements
                element = inp.get("element", "") or inp.get("name", "") or ""
                el_lower = element.lower()

                if "filter" in el_lower:
                    found = True
                    break

                # Click on revision/diff links (investigation within history page)
                if any(kw in el_lower for kw in [
                    'revision', 'diff', 'oldest', 'earliest', 'prev',
                    'first revision', 'compare', 'cur ',
                ]):
                    found = True
                    break

    return found


def extract_answer(text):
    """Extract the 3 answer fields from XML output.

    Uses findall to handle multiple <answer> blocks — takes the last one.
    """
    answers = re.findall(
        r'<answer>\s*(.*?)\s*</answer>', text, re.DOTALL | re.I
    )
    if not answers:
        return None

    # Take the last <answer> block
    content = answers[-1]

    result = {}
    fw_match = re.search(
        r'<first_framework>\s*(.+?)\s*</first_framework>', content, re.DOTALL | re.I
    )
    author_match = re.search(
        r'<first_author>\s*(.+?)\s*</first_author>', content, re.DOTALL | re.I
    )
    date_match = re.search(
        r'<first_date>\s*(\d{4}-\d{2}-\d{2})\s*</first_date>', content, re.I
    )

    if fw_match:
        fw_text = fw_match.group(1).strip().lower()
        for fw in REQUIRED_FRAMEWORKS:
            if re.search(rf'\b{re.escape(fw)}\b', fw_text, re.I):
                result['framework'] = fw
                break

    if author_match:
        result['author'] = author_match.group(1).strip()
    if date_match:
        result['date'] = date_match.group(1)

    return result


def extract_all_dates(text):
    """Extract the all_dates section from XML output.

    Returns dict mapping framework name (lowercase) to dict with 'date' and 'author'.
    """
    answers = re.findall(
        r'<answer>\s*(.*?)\s*</answer>', text, re.DOTALL | re.I
    )
    if not answers:
        return None

    content = answers[-1]

    # Find <all_dates> block
    all_dates_match = re.search(
        r'<all_dates>\s*(.*?)\s*</all_dates>', content, re.DOTALL | re.I
    )
    if not all_dates_match:
        return None

    all_dates_text = all_dates_match.group(1)

    # Extract framework name="X" author="Y" and date
    # Support both with and without author attribute
    dates = {}
    for m in re.finditer(
        r'<framework\s+name=["\']([^"\']+)["\'](?:\s+author=["\']([^"\']*)["\'])?\s*>\s*(\d{4}-\d{2}-\d{2})\s*</framework>',
        all_dates_text, re.I
    ):
        fw_name = m.group(1).strip().lower()
        fw_author = m.group(2).strip() if m.group(2) else ""
        fw_date = m.group(3)
        # Normalize to label key
        label_key = FRAMEWORK_LABEL_MAP.get(fw_name, fw_name)
        dates[label_key] = {'date': fw_date, 'author': fw_author}

    return dates if dates else None


def is_valid_date(date_str):
    """Check if a date string is a valid calendar date."""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_invalid_author(author):
    """Check if the author is a placeholder, bot, IP, or framework creator."""
    if not author:
        return True

    author_lower = author.lower().strip()

    # Empty / placeholder
    if author_lower in INVALID_AUTHORS:
        return True

    # IP address (require exactly 4 octets)
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', author):
        return True

    # Bot name patterns
    if re.search(r'(?:bot\d*$|bot[_-]|[_-]bot$)', author_lower):
        return True
    if re.match(r'^[A-Z][a-z]*Bot$', author):
        return True

    # Framework creators (not Wikipedia editors)
    if author_lower in FRAMEWORK_CREATORS:
        return True

    return False


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Wikipedia Framework Release Investigator (v71)")
    print("| Output: 3 XML fields + all_dates section")
    print("| Checks: Answer correctness, History evidence, Investigation, Traps, All dates")
    print("=" * 70)

    # Load ground truth
    label = get_ground_truth()

    print(f"| Ground truth: framework={label.get('first_framework')}, "
          f"author={label.get('first_author')}, "
          f"date={label.get('first_date')}")

    # Parse messages
    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    tool_calls = msgs["tool_calls"]

    # Extract URLs
    try:
        urls = extract_urls(tool_calls)
    except Exception as e:
        print(f"| [ERROR] Failed to extract URLs: {e}")
        return False

    # --- CHECK 1: Answer completeness ---
    print("|")
    print("| [CHECK 1] Answer Completeness")

    answer = extract_answer(text)
    if not answer or not answer.get('framework'):
        print("| [FAILED] No valid <answer> block found")
        print("|          Must include <first_framework>, <first_author>, <first_date>")
        print("=" * 70)
        return False

    missing = []
    if not answer.get('framework'):
        missing.append('first_framework')
    if not answer.get('author'):
        missing.append('first_author')
    if not answer.get('date'):
        missing.append('first_date')

    if missing:
        print(f"| [FAILED] Missing fields: {missing}")
        print("=" * 70)
        return False

    print(f"| [OK] All 3 fields present:")
    print(f"|       framework: {answer['framework']}")
    print(f"|       author: {answer['author'][:40]}")
    print(f"|       date: {answer['date']}")

    # --- CHECK 2: Answer correctness against ground truth ---
    print("|")
    print("| [CHECK 2] Answer Correctness (Ground Truth)")

    expected_fw = label.get('first_framework', '').lower()
    expected_author = label.get('first_author', '').strip()
    expected_date = label.get('first_date', '').strip()

    fw_match = answer['framework'].lower() == expected_fw
    author_match = answer['author'].strip().lower() == expected_author.lower()
    date_match = answer['date'].strip() == expected_date

    if not fw_match:
        print(f"| [FAILED] Framework mismatch: got '{answer['framework']}', expected '{expected_fw}'")
        print("=" * 70)
        return False

    if not date_match:
        print(f"| [FAILED] Date mismatch: got '{answer['date']}', expected '{expected_date}'")
        print("=" * 70)
        return False

    if not author_match:
        print(f"| [FAILED] Author mismatch: got '{answer['author']}', expected '{expected_author}'")
        print("=" * 70)
        return False

    print(f"| [OK] Answer matches ground truth")

    # --- CHECK 3: History page evidence ---
    print("|")
    print("| [CHECK 3] History Page Evidence (All 4 Frameworks)")

    frameworks_visited = check_history_evidence(urls)
    print(f"| Frameworks with history visited: {frameworks_visited}")

    if len(frameworks_visited) < len(REQUIRED_FRAMEWORKS):
        missing = set(REQUIRED_FRAMEWORKS) - frameworks_visited
        print(f"| [FAILED] Missing history for: {missing}")
        print("|          Model must visit history pages for ALL 4 frameworks")
        print("=" * 70)
        return False

    print(f"| [OK] All 4 frameworks have history pages visited")

    # --- CHECK 4: Investigation evidence ---
    print("|")
    print("| [CHECK 4] Investigation Evidence")

    used_tools = check_investigation_evidence(tool_calls)
    if used_tools:
        print(f"| [OK] Investigation tools detected (history search, filter, sort, or WikiBlame)")
    else:
        print(f"| [FAILED] No investigation tool usage detected")
        print("|          Model must use Wikipedia's built-in tools (filter, search, sort, or view diffs)")
        print("=" * 70)
        return False

    # --- CHECK 5: Trap detection ---
    print("|")
    print("| [CHECK 5] Trap Detection (Invalid Authors)")

    if is_invalid_author(answer['author']):
        print(f"| [FAILED] Invalid author detected: '{answer['author']}'")
        print("|          Must be a real Wikipedia username (not bot, IP, placeholder, or framework creator)")
        print("=" * 70)
        return False

    print(f"| [OK] Author '{answer['author']}' is valid (not a bot, IP, placeholder, or creator)")

    # --- CHECK 6: All dates verification (presence, format, accuracy, author validity) ---
    print("|")
    print("| [CHECK 6] All Dates Verification")

    all_dates = extract_all_dates(text)
    if not all_dates:
        print("| [FAILED] No <all_dates> section found in answer")
        print("|          Must include <all_dates> with date for each framework")
        print("=" * 70)
        return False

    # Check all 4 frameworks are present
    missing_fw = set(REQUIRED_FRAMEWORKS) - set(all_dates.keys())
    if missing_fw:
        print(f"| [FAILED] Missing entries for frameworks: {missing_fw}")
        print("=" * 70)
        return False

    # Check each framework: date format, date accuracy, author presence and validity
    errors = []
    for fw in REQUIRED_FRAMEWORKS:
        entry = all_dates.get(fw, {})
        d = entry.get('date', '')
        a = entry.get('author', '')

        # Date format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', d):
            errors.append(f"{fw}: invalid date format '{d}'")
            continue

        # Date validity (real calendar date)
        if not is_valid_date(d):
            errors.append(f"{fw}: invalid date '{d}'")
            continue

        # Author present
        if not a:
            errors.append(f"{fw}: missing author attribute")
            continue

        # Author validity (not bot, IP, placeholder, or framework creator)
        if is_invalid_author(a):
            errors.append(f"{fw}: invalid author '{a}' (bot, IP, placeholder, or framework creator)")
            continue

        # Date accuracy (comma-separated = multiple acceptable dates)
        label_key = fw
        label_val = label.get(f'{label_key}_date', '').strip()
        if label_val:
            acceptable = [x.strip() for x in label_val.split(',') if x.strip()]
            if d not in acceptable:
                errors.append(f"{fw}: got date '{d}', expected one of {acceptable}")

    if errors:
        print("| [FAILED] Errors in all_dates:")
        for err in errors:
            print(f"|          {err}")
        print("=" * 70)
        return False

    # Print summary
    print(f"| [OK] All 4 frameworks have valid dates and authors:")
    for fw in REQUIRED_FRAMEWORKS:
        entry = all_dates.get(fw, {})
        print(f"|       {fw}: {entry.get('date', 'N/A')} by {entry.get('author', 'N/A')}")

    # Success
    print("|")
    print(f"| [PASSED] All checks passed!")
    print(f"|          Answer: {answer['framework']} by {answer['author']} on {answer['date']}")
    print(f"|          History pages visited: all 4 frameworks")
    print(f"|          All dates verified")
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
