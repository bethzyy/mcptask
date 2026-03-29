#!/usr/bin/env python3
"""
Verification for JavaScript Framework History Investigator (v59).

Task: Investigate Wikipedia edit history to find original authors who added
"Initial release" information for 4 JavaScript frameworks,
and determine which framework's Initial release was added FIRST chronologically.

v59 changes (Increased Difficulty with More Traps):
- Reduced from 5 to 4 frameworks (removed Solid.js)
- Total: 4 frameworks × 2 + 2 final = 10 fields (complies with red line)
- NEW TRAP: Chronological order validation (first_framework must be earliest)
- NEW TRAP: Known wrong authors detection
- NEW TRAP: Date range validation (2013-2020)
- NEW TRAP: Suspicious pattern detection (all same author/date)
- Improved is_bot_or_ip detection to avoid false positives

Key principle: verify.py 只检查"最终答案 + 关键动作证据"
"""
import sys
import json
import os
import re
from pathlib import Path

# Required frameworks to investigate (4 frameworks = 10 fields, complies with red line)
REQUIRED_FRAMEWORKS = ["react", "vue", "angular", "svelte"]

# Known wrong authors that models commonly mistake as correct
# These are common placeholder names, company names, or obviously wrong answers
KNOWN_WRONG_AUTHORS = {
    # Placeholder patterns
    'unknown', 'n/a', 'none', 'todo', 'tbd', 'test', 'example',
    # Company names (not individual Wikipedia editors)
    'facebook', 'google', 'microsoft', 'amazon', 'apple', 'netflix',
    # Generic terms
    'wikipedia', 'wikimedia', 'admin', 'administrator', 'moderator',
    'editor', 'contributor', 'user', 'anonymous', 'guest',
    # Framework creators (not Wikipedia editors)
    'dan abramov', 'jordan walke', 'evan you', 'misko hevery',
    'rich harris', 'ryan carniato',
    # Common mistakes
    'react team', 'vue team', 'angular team', 'svelte team',
    'original author', 'first editor', 'the author',
}

# Valid date range for Initial release info being added to Wikipedia
# These frameworks were created 2013-2019, so Initial release info
# should have been added between 2013-2020
MIN_VALID_DATE = "2013-01-01"
MAX_VALID_DATE = "2020-12-31"

# Wikipedia URL patterns (for minimal evidence check)
WIKIPEDIA_PATTERN = re.compile(r'https?://[a-z]+\.wikipedia\.org/', re.I)
HISTORY_PATTERN = re.compile(r'action=history', re.I)
DIFF_PATTERN = re.compile(r'diff=\d+|oldid=\d+', re.I)
PAGE_URL_PATTERN = re.compile(r'Page URL:\s*(https?://[^\s]+)', re.I)


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
            # Extract assistant text
            if m.get("role") == "assistant":
                c = m.get("content", "")
                if isinstance(c, str):
                    text_parts.append(c)
                elif isinstance(c, list):
                    for i in c:
                        if isinstance(i, dict):
                            if i.get("type") in ("text", "output_text"):
                                text_parts.append(i.get("text", ""))

            # Extract tool calls from messages with 'name' field (type='function_call')
            if "name" in m and m.get("type") == "function_call":
                tool_name = m.get("name", "")
                args_str = m.get("arguments", "{}")
                try:
                    args = json.loads(args_str) if isinstance(args_str, str) else args_str
                except json.JSONDecodeError:
                    args = {}
                tool_calls.append({"name": tool_name, "input": args})

            # Extract URLs from function_call_output messages (contains Page URL)
            if m.get("type") == "function_call_output":
                output = m.get("output", "")
                if output:
                    tool_calls.append({"name": "output", "result": output})

        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts), "tool_calls": tool_calls}


def extract_urls_from_tool_calls(tool_calls):
    """Extract all URLs visited from tool calls."""
    urls = []

    for call in tool_calls:
        # Check tool input for URLs (browser_navigate)
        if "input" in call:
            input_data = call["input"]
            if isinstance(input_data, dict):
                url = input_data.get("url", "")
                if url:
                    urls.append(url)

        # Check tool result for URLs
        if "result" in call:
            result = call["result"]
            if isinstance(result, str):
                for match in PAGE_URL_PATTERN.finditer(result):
                    urls.append(match.group(1))

    return urls


def check_history_evidence(urls):
    """Minimal evidence check: did model visit at least one history page?"""
    history_urls = [u for u in urls if HISTORY_PATTERN.search(u)]
    return len(history_urls) > 0, len(history_urls)


def check_diff_evidence(urls):
    """Check if model viewed at least one diff page."""
    diff_urls = [u for u in urls if DIFF_PATTERN.search(u)]
    return len(diff_urls) > 0, len(diff_urls)


def normalize_framework_name(name):
    """Normalize framework name to match REQUIRED_FRAMEWORKS format."""
    name_lower = name.lower()
    name_lower = name_lower.replace('.js', '').replace('.', '')
    mapping = {
        'vuejs': 'vue',
        'vue': 'vue',
        'react': 'react',
        'angular': 'angular',
        'svelte': 'svelte',
    }
    return mapping.get(name_lower, name_lower)


def validate_date_format(date_str):
    """Check if date is in YYYY-MM-DD format."""
    if not date_str:
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str.strip()))


def is_bot_or_ip(username):
    """Check if username looks like a bot or IP address.

    IMPORTANT: Use precise matching to avoid false positives on real usernames.
    A real username like "RobotLover" or "AutoSales" should NOT be flagged.
    """
    if not username:
        return False
    username_lower = username.lower().strip()

    # Common Wikipedia bot suffixes/prefixes (case-insensitive exact match)
    # Only flag if username ends with "bot" or starts with common bot prefixes
    bot_suffixes = ['bot', 'BOT']
    for suffix in bot_suffixes:
        if username.endswith(suffix) and len(username) > 3:
            # Check it's actually a bot pattern, not a word ending in "bot"
            # e.g., "ClueBot" is a bot, "RobotLover" might not be
            # Additional check: common bot naming patterns
            if re.search(r'(?:bot\d*$|bot[_-]|[_-]bot$)', username_lower):
                return True
            # If username is exactly "XxxBot" pattern (capital B), likely a bot
            if re.match(r'^[A-Z][a-z]*Bot$', username):
                return True

    # Explicit bot prefixes commonly used on Wikipedia
    bot_prefixes = ['bot-', 'Bot-', 'auto-', 'Auto-', 'sock-']
    for prefix in bot_prefixes:
        if username.startswith(prefix):
            return True

    # IP address pattern: must be a complete IPv4 address
    # Pattern: xxx.xxx.xxx.xxx or xxx.xxx.xxx (partial)
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}(\.\d{1,3})?$', username):
        return True

    # Common bot name patterns on Wikipedia
    bot_name_patterns = [
        r'^ClueBot', r'^XLinkBot', r'^Cyberbot', r'^AnomieBOT',
        r'^Materialscientist', r'^RjwilmsiBot', r'^Yobot', r'^Addbot',
        r'^Legobot', r'^Snotbot', r'^MediaWiki',
    ]
    for pattern in bot_name_patterns:
        if re.match(pattern, username, re.I):
            return True

    return False


def extract_framework_data(text):
    """Extract all framework data from the output using XML tag format.

    v58: 4 frameworks investigation (10 fields, complies with red line).
    """
    results = {}

    # Initialize results structure for all required frameworks
    for fw in REQUIRED_FRAMEWORKS:
        results[fw] = {
            'author': None,
            'date': None,
        }

    # Extract <answer> block
    answer_match = re.search(r'<answer>\s*(.*?)\s*</answer>', text, re.DOTALL | re.I)
    if not answer_match:
        return results

    answer_content = answer_match.group(1)

    # Define XML tag mapping for v58: tag name -> (framework, attribute)
    # 4 frameworks × 2 fields + 2 final = 10 fields total
    tag_mapping = {
        # React
        'react_author': ('react', 'author'),
        'react_date': ('react', 'date'),
        # Vue
        'vue_author': ('vue', 'author'),
        'vue_date': ('vue', 'date'),
        # Angular
        'angular_author': ('angular', 'author'),
        'angular_date': ('angular', 'date'),
        # Svelte
        'svelte_author': ('svelte', 'author'),
        'svelte_date': ('svelte', 'date'),
    }

    # Parse XML tags
    for tag_name, (framework, attr) in tag_mapping.items():
        # Pattern: <tag>value</tag>
        pattern = rf'<{tag_name}>\s*(.*?)\s*</{tag_name}>'
        match = re.search(pattern, answer_content, re.DOTALL | re.I)
        if match:
            value = match.group(1).strip()
            results[framework][attr] = value

    return results


def extract_final_answer(text):
    """Extract the final answer from the output using XML tag format.

    v58: first_framework + first_date (for Initial release).
    """
    # Extract <answer> block
    answer_match = re.search(r'<answer>\s*(.*?)\s*</answer>', text, re.DOTALL | re.I)

    result = {
        'framework': None,
        'date': None
    }

    if answer_match:
        answer_content = answer_match.group(1)

        # Extract final answer
        framework_match = re.search(r'<first_framework>\s*(.+?)\s*</first_framework>', answer_content, re.DOTALL | re.I)
        date_match = re.search(r'<first_date>\s*(\d{4}-\d{2}-\d{2})\s*</first_date>', answer_content, re.I)

        if framework_match:
            framework_text = framework_match.group(1).strip().lower()
            for fw in REQUIRED_FRAMEWORKS:
                if re.search(rf'\b{re.escape(fw)}\b', framework_text, re.I):
                    result['framework'] = fw
                    result['date'] = date_match.group(1) if date_match else None
                    break

    return result


def check_trap_answers(framework_data):
    """Check for common trap answers (obviously wrong patterns).

    IMPORTANT: Use EXACT matching to avoid false positives on real usernames.
    """
    traps_found = []

    # Exact trap words that are clearly placeholders, not real usernames
    EXACT_TRAP_WORDS = {
        'unknown', 'n/a', 'none', 'todo', 'tbd',
        '[username]', '[author]', '[name]', '...',
        'anonymous', 'anonymous user', 'unknown user',
        'wikipedia', 'wikipedia user', 'admin', 'administrator',
        'moderator', 'system', 'auto',
    }

    for framework, data in framework_data.items():
        # Check author
        author = data.get('author', '') or ''
        author_lower = author.lower().strip()

        if not author:
            traps_found.append(f"{framework}: Empty author")
        elif author_lower in EXACT_TRAP_WORDS:
            traps_found.append(f"{framework}: Placeholder author '{author}'")
        elif author.startswith('[') and author.endswith(']'):
            traps_found.append(f"{framework}: Bracketed placeholder '{author}'")
        elif len(author) <= 3 and not author.replace('_', '').replace('-', '').isalnum():
            traps_found.append(f"{framework}: Suspicious short author '{author}'")
        elif is_bot_or_ip(author):
            traps_found.append(f"{framework}: Bot/IP address detected '{author}'")

    return traps_found


def check_known_wrong_authors(framework_data):
    """Check if any author matches known wrong answers."""
    wrong_authors = []

    for framework, data in framework_data.items():
        author = data.get('author', '') or ''
        author_lower = author.lower().strip()

        if author_lower in KNOWN_WRONG_AUTHORS:
            wrong_authors.append(f"{framework}: Known wrong author '{author}'")
        # Also check if author contains company/framework names
        for wrong in ['facebook', 'google', 'microsoft', 'react team', 'vue team', 'angular team']:
            if wrong in author_lower:
                wrong_authors.append(f"{framework}: Contains wrong term '{wrong}' in '{author}'")

    return wrong_authors


def check_date_range(framework_data):
    """Check if dates are within reasonable range (2013-2020)."""
    invalid_dates = []

    for framework, data in framework_data.items():
        date = data.get('date', '') or ''
        if not date:
            continue

        try:
            # Compare as strings (YYYY-MM-DD format)
            if date < MIN_VALID_DATE:
                invalid_dates.append(f"{framework}: Date {date} is too early (before {MIN_VALID_DATE})")
            elif date > MAX_VALID_DATE:
                invalid_dates.append(f"{framework}: Date {date} is too late (after {MAX_VALID_DATE})")
        except Exception:
            pass  # Format already validated elsewhere

    return invalid_dates


def check_chronological_order(framework_data, final_answer):
    """Check if first_framework has the earliest date among all frameworks.

    This is a CRITICAL trap: models often pick a random framework without
    actually comparing dates across all frameworks.
    """
    if not final_answer or not final_answer.get('framework'):
        return ["Final answer missing framework"]

    if not final_answer.get('date'):
        return ["Final answer missing date - cannot verify chronological order"]

    first_framework = final_answer['framework']
    first_date = final_answer['date']

    # Collect all framework dates
    all_dates = {}
    for framework, data in framework_data.items():
        date = data.get('date')
        if date:
            all_dates[framework] = date

    if len(all_dates) < len(REQUIRED_FRAMEWORKS):
        return [f"Missing dates for some frameworks, cannot verify chronological order"]

    # Check if first_framework has the earliest date
    earliest_framework = min(all_dates.keys(), key=lambda k: all_dates[k])
    earliest_date = all_dates[earliest_framework]

    # If there's a tie (multiple frameworks with same earliest date), it's acceptable
    # as long as first_framework is one of them
    frameworks_with_earliest = [fw for fw, dt in all_dates.items() if dt == earliest_date]

    if first_framework not in frameworks_with_earliest:
        return [
            f"Chronological order violation: {first_framework} has date {first_date}, "
            f"but {earliest_framework} has earlier date {earliest_date}"
        ]

    return []


def check_suspicious_patterns(framework_data):
    """Check for suspicious patterns like all same author or all same date."""
    patterns = []

    # Collect authors and dates
    authors = [data.get('author', '') for data in framework_data.values() if data.get('author')]
    dates = [data.get('date', '') for data in framework_data.values() if data.get('date')]

    # Check if all authors are the same (suspicious)
    if len(authors) == len(REQUIRED_FRAMEWORKS):
        unique_authors = set(a.lower().strip() for a in authors)
        if len(unique_authors) == 1:
            patterns.append(f"All frameworks have same author '{authors[0]}' - suspicious pattern")

    # Check if all dates are the same (very suspicious - unlikely coincidence)
    if len(dates) == len(REQUIRED_FRAMEWORKS):
        unique_dates = set(dates)
        if len(unique_dates) == 1:
            patterns.append(f"All frameworks have same date '{dates[0]}' - very suspicious pattern")

    return patterns


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: JavaScript Framework History Investigator (v59)")
    print("| Focus: Single-field investigation (Initial Release only)")
    print("| Frameworks: 4 (React, Vue, Angular, Svelte)")
    print("| Format: 10 XML tags (complies with red line)")
    print("| Traps: Chronological order, Wrong authors, Date range, Patterns")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    tool_calls = msgs["tool_calls"]

    # Extract all URLs
    try:
        urls = extract_urls_from_tool_calls(tool_calls)
    except Exception as e:
        print(f"| [ERROR] Failed to extract URLs: {e}")
        return False

    # CHECK 1: Minimal evidence of history investigation
    print("|")
    print("| [CHECK 1] History Investigation Evidence")

    has_history, history_count = check_history_evidence(urls)
    if not has_history:
        print(f"| [FAILED] History pages visited: {history_count} (expected >=1)")
        print("|          Model must use View history to find original authors")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] History pages visited: {history_count}")

    # CHECK 2: Evidence of viewing diff pages
    print("|")
    print("| [CHECK 2] Diff Pages Viewed")

    has_diff, diff_count = check_diff_evidence(urls)
    if not has_diff:
        print(f"| [FAILED] Diff pages viewed: {diff_count} (expected >=1)")
        print("|          Model must view diff pages to confirm original authors")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Diff pages viewed: {diff_count}")

    # CHECK 3: Extract framework data and verify all authors identified
    print("|")
    print("| [CHECK 3] All Initial Release Authors Identified")

    try:
        framework_data = extract_framework_data(text)
    except Exception as e:
        print(f"| [ERROR] Failed to extract framework data: {e}")
        return False

    # Check which frameworks are missing author data
    missing_authors = []
    for framework in REQUIRED_FRAMEWORKS:
        author = framework_data.get(framework, {}).get('author')
        if not author:
            missing_authors.append(framework)

    if missing_authors:
        print(f"| [FAILED] Missing Initial Release authors for: {missing_authors}")
        print("|          Must identify original author for each framework's Initial release")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] All 4 frameworks have author data:")
        for fw in REQUIRED_FRAMEWORKS:
            author = framework_data[fw].get('author', 'N/A')
            print(f"|       {fw}: {author[:40]}...")

    # CHECK 4: Dates in valid format
    print("|")
    print("| [CHECK 4] Dates in Valid Format (YYYY-MM-DD)")

    invalid_dates = []
    for framework in REQUIRED_FRAMEWORKS:
        if framework in framework_data:
            date = framework_data[framework].get('date')
            if not validate_date_format(date):
                invalid_dates.append(f"{framework}: '{date}'")

    if invalid_dates:
        print(f"| [FAILED] Invalid date format for: {invalid_dates}")
        print("|          Dates must be in YYYY-MM-DD format")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] All dates in valid format:")
        for fw in REQUIRED_FRAMEWORKS:
            date = framework_data[fw].get('date', 'N/A')
            print(f"|       {fw}: {date}")

    # CHECK 5: Trap detection
    print("|")
    print("| [CHECK 5] Trap Detection")

    traps = check_trap_answers(framework_data)
    if traps:
        print(f"| [FAILED] Trap answers detected:")
        for trap in traps:
            print(f"|         - {trap}")
        print("|          These look like placeholder, bot, or IP-based answers, not real usernames")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] No basic trap patterns detected")

    # CHECK 5.5: Known wrong authors
    print("|")
    print("| [CHECK 5.5] Known Wrong Authors Detection")

    wrong_authors = check_known_wrong_authors(framework_data)
    if wrong_authors:
        print(f"| [FAILED] Known wrong authors detected:")
        for wa in wrong_authors:
            print(f"|         - {wa}")
        print("|          These are commonly mistaken answers, not real Wikipedia editors")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] No known wrong authors detected")

    # CHECK 5.6: Date range validation
    print("|")
    print("| [CHECK 5.6] Date Range Validation (2013-2020)")

    invalid_dates = check_date_range(framework_data)
    if invalid_dates:
        print(f"| [FAILED] Dates outside valid range:")
        for d in invalid_dates:
            print(f"|         - {d}")
        print("|          Initial release info should have been added between 2013-2020")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] All dates within valid range")

    # CHECK 6: Final answer present
    print("|")
    print("| [CHECK 6] Final Answer Present")

    try:
        final_answer = extract_final_answer(text)
    except Exception as e:
        print(f"| [ERROR] Failed to extract final answer: {e}")
        return False

    if not final_answer.get('framework'):
        print("| [FAILED] No final answer found")
        print("|          Must include first_framework and first_date in <answer>")
        print("=" * 70)
        return False
    elif final_answer['framework'] not in REQUIRED_FRAMEWORKS:
        print(f"| [FAILED] Final answer framework not recognized: {final_answer['framework']}")
        print("|          Must be one of: React, Vue, Angular, Svelte")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Final answer: {final_answer['framework']}")
        if final_answer['date']:
            print(f"|       Date: {final_answer['date']}")

    # CHECK 7: Final answer consistency
    print("|")
    print("| [CHECK 7] Final Answer Consistency")

    if final_answer and final_answer['framework'] in framework_data:
        answer_framework = final_answer['framework']
        answer_date = final_answer['date']
        framework_date = framework_data[answer_framework].get('date')

        # Check: if framework_date exists but answer_date is missing/invalid, fail
        if framework_date and not answer_date:
            print(f"| [FAILED] Final answer missing valid date")
            print(f"|          {answer_framework}'s date is {framework_date}, but final answer date is missing or invalid")
            print("=" * 70)
            return False
        elif answer_date and framework_date and answer_date != framework_date:
            print(f"| [FAILED] Final answer date ({answer_date}) doesn't match {answer_framework}'s date ({framework_date})")
            print("=" * 70)
            return False
        else:
            print(f"| [OK] Final answer is consistent")

    # CHECK 8: Chronological order validation (CRITICAL TRAP)
    print("|")
    print("| [CHECK 8] Chronological Order Validation (CRITICAL)")

    chrono_errors = check_chronological_order(framework_data, final_answer)
    if chrono_errors:
        print(f"| [FAILED] Chronological order violation:")
        for err in chrono_errors:
            print(f"|         - {err}")
        print("|          The first_framework must have the EARLIEST date among all frameworks")
        print("|          This trap catches models that don't properly compare dates")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Chronological order is correct")
        print(f"|       {final_answer['framework']} has the earliest date: {final_answer['date']}")

    # CHECK 9: Suspicious pattern detection
    print("|")
    print("| [CHECK 9] Suspicious Pattern Detection")

    patterns = check_suspicious_patterns(framework_data)
    if patterns:
        print(f"| [FAILED] Suspicious patterns detected:")
        for p in patterns:
            print(f"|         - {p}")
        print("|          This suggests the model didn't actually investigate each framework")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] No suspicious patterns detected")

    # Success!
    print("|")
    print(f"| [PASSED] All 9 verification checks passed!")
    print(f"|          Frameworks: {len(framework_data)}/4")
    print(f"|          Authors: All identified and valid")
    print(f"|          Dates: All valid format and range")
    print(f"|          Chronological Order: Verified")
    print(f"|          Final Answer: {final_answer['framework']} ({final_answer['date']})")
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
