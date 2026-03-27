#!/usr/bin/env python3
"""
Verification for JavaScript Framework History Investigator (v41).

Task: Investigate Wikipedia edit history to find original authors who added
"Initial release" information for 3 JavaScript frameworks.

Key Verification Points:
1. Page count >= 9 (3 framework pages + 3 history pages + 3 diff pages + user pages)
2. History feature used (action=history pages)
3. Diff pages viewed (diff= in URL)
4. User pages visited (User: namespace)
5. All 3 frameworks investigated
6. Investigation log present
7. Trap detection: original authors vs recent/high-frequency/admin editors

v41 changes:
- Complete redesign: date verification -> edit history investigation
- Added history page detection
- Added diff page detection
- Added user page detection
- Added investigation log requirement
- Added trap detection for wrong editor types
- Reduced to 3 frameworks (React, Vue.js, Angular) for 600s timeout
- MIN_PAGE_COUNT = 9 (balanced for 600s timeout)
"""
import sys
import json
import os
import re
from pathlib import Path

# Required frameworks to investigate (v41: reduced to 3 for 600s timeout)
REQUIRED_FRAMEWORKS = ["react", "vue", "angular"]

# Minimum pages to visit (v41: 3 frameworks, 600s timeout, external tool is slow)
MIN_PAGE_COUNT = 8

# Wikipedia URL patterns
WIKIPEDIA_PATTERN = re.compile(r'https?://[a-z]+\.wikipedia\.org/', re.I)
HISTORY_PATTERN = re.compile(r'action=history', re.I)
DIFF_PATTERN = re.compile(r'diff=', re.I)
USER_PAGE_PATTERN = re.compile(r'/wiki/User:', re.I)
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


def check_page_count(urls):
    """Check if minimum page count is met."""
    # Filter Wikipedia URLs only
    wiki_urls = [u for u in urls if WIKIPEDIA_PATTERN.search(u)]

    # Normalize and count unique pages
    unique_pages = set()
    for url in wiki_urls:
        # Normalize URL by removing query params for page counting
        base_url = re.sub(r'[?&].*', '', url)
        unique_pages.add(base_url.lower())

    return len(unique_pages), len(wiki_urls)


def check_history_feature_used(urls):
    """Check if View History feature was used."""
    history_urls = [u for u in urls if HISTORY_PATTERN.search(u)]
    return len(history_urls), history_urls


def check_diff_pages_viewed(urls):
    """Check if diff pages were viewed."""
    diff_urls = [u for u in urls if DIFF_PATTERN.search(u)]
    return len(diff_urls), diff_urls


def check_user_pages_visited(urls):
    """Check if user pages were visited."""
    user_urls = [u for u in urls if USER_PAGE_PATTERN.search(u)]
    return len(user_urls), user_urls


def check_all_frameworks_investigated(text):
    """Check if all 3 frameworks are mentioned with investigation details."""
    text_lower = text.lower()

    frameworks_found = []
    for framework in REQUIRED_FRAMEWORKS:
        # Check if framework is mentioned with history-related context
        patterns = [
            rf'{framework}.*?(history|edit|revision|author|contributor)',
            rf'(history|edit|revision|author|contributor).*?{framework}',
            rf'<framework[^>]*name\s*=\s*["\']?{framework}',
        ]

        for pattern in patterns:
            if re.search(pattern, text_lower, re.I):
                frameworks_found.append(framework)
                break

    missing = [f for f in REQUIRED_FRAMEWORKS if f not in frameworks_found]
    return len(frameworks_found), missing


def check_investigation_log(text):
    """Check if investigation log is present and contains entries."""
    # Look for investigation_log tag
    log_match = re.search(r'<investigation_log>\s*(.*?)\s*</investigation_log>', text, re.DOTALL | re.I)

    if not log_match:
        # Also check for alternative formats
        log_patterns = [
            r'investigation\s*log[:\s]+(.*?)(?=\n\n|\n<|$)',
            r'\*\*investigation\s*log\*\*[:\s]+(.*?)(?=\n\n|\n\*\*|$)',
        ]

        for pattern in log_patterns:
            match = re.search(pattern, text, re.DOTALL | re.I)
            if match:
                log_content = match.group(1)
                entries = re.findall(r'[-*]\s*.+', log_content)
                return {"ok": True, "entries": len(entries), "content": log_content[:200]}

        return {"ok": False, "entries": 0, "content": ""}

    log_content = log_match.group(1)
    # Count entries (lines starting with - or *)
    entries = re.findall(r'[-*]\s*.+', log_content)

    return {"ok": True, "entries": len(entries), "content": log_content[:200]}


def check_original_authors_identified(text):
    """Check if original authors are identified for each framework."""
    text_lower = text.lower()

    results = {}

    # Look for original_author tags
    author_matches = re.findall(
        r'<framework[^>]*name\s*=\s*["\']?(\w+)["\']?[^>]*>.*?<original_author>\s*(.*?)\s*</original_author>',
        text, re.DOTALL | re.I
    )

    for framework, author in author_matches:
        framework_lower = framework.lower()
        if framework_lower in REQUIRED_FRAMEWORKS or framework_lower.replace('.', '') in REQUIRED_FRAMEWORKS:
            # Normalize framework name
            normalized = framework_lower.replace('.', '')
            results[normalized] = author.strip()

    # Alternative: look for "original author" mentions near framework names
    for framework in REQUIRED_FRAMEWORKS:
        if framework not in results and framework in text_lower:
            # Look for author patterns near framework mention
            pattern = rf'{framework}[^.]*?(original\s+author|author[^.]*?added)[^.]*?[:\s]+([A-Za-z0-9_-]+)'
            match = re.search(pattern, text_lower)
            if match:
                results[framework] = match.group(2)

    return results


def check_dates_added(text):
    """Check if dates are identified for when info was added."""
    text_lower = text.lower()

    dates_found = {}

    # Look for date_added tags
    date_matches = re.findall(
        r'<framework[^>]*name\s*=\s*["\']?(\w+)["\']?[^>]*>.*?<date_added>\s*(.*?)\s*</date_added>',
        text, re.DOTALL | re.I
    )

    for framework, date in date_matches:
        framework_lower = framework.lower().replace('.', '')
        if framework_lower in REQUIRED_FRAMEWORKS:
            dates_found[framework_lower] = date.strip()

    return dates_found


def check_user_verified(text):
    """Check if user pages were verified."""
    text_lower = text.lower()

    verified_count = 0

    # Look for user_verified tags with YES
    yes_matches = re.findall(r'<user_verified>\s*(YES)\s*</user_verified>', text, re.I)
    verified_count = len(yes_matches)

    # Also check for credibility notes
    credibility_matches = re.findall(r'<credibility_notes>\s*(.+?)\s*</credibility_notes>', text, re.DOTALL | re.I)
    credibility_count = len([m for m in credibility_matches if m.strip()])

    return verified_count, credibility_count


def check_final_answer(text):
    """Check if final answer is present."""
    # Look for final_answer tag
    match = re.search(r'<final_answer>\s*(.*?)\s*</final_answer>', text, re.DOTALL | re.I)

    if match:
        answer = match.group(1).strip()
        # Check which framework is mentioned
        for framework in REQUIRED_FRAMEWORKS:
            if framework.lower() in answer.lower():
                return {"ok": True, "answer": framework, "full_answer": answer[:100]}

        return {"ok": True, "answer": "unknown", "full_answer": answer[:100]}

    # Alternative: look for "final answer" or "conclusion"
    alt_patterns = [
        r'(?:final\s+answer|conclusion)[:\s]+(.{10,100})',
        r'(?:framework[^.]*?first|first[^.]*?framework)[:\s]+(\w+)',
    ]

    for pattern in alt_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            answer = match.group(1).strip()
            for framework in REQUIRED_FRAMEWORKS:
                if framework.lower() in answer.lower():
                    return {"ok": True, "answer": framework, "full_answer": answer[:100]}

    return {"ok": False, "answer": "", "full_answer": ""}


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: JavaScript Framework History Investigator (v41)")
    print("| Task: Investigate Wikipedia edit history for 3 frameworks")
    print("| Required: 8+ pages, history feature, diff pages, user pages")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False

    text = msgs["text"]
    tool_calls = msgs["tool_calls"]

    # Extract all URLs
    urls = extract_urls_from_tool_calls(tool_calls)

    # Step 1: Check page count
    print("|")
    print("| [CHECK 1] Page Count (minimum 15)")

    unique_count, total_wiki = check_page_count(urls)
    if unique_count < MIN_PAGE_COUNT:
        print(f"| [FAILED] Only {unique_count} unique Wikipedia pages visited")
        print(f"|          Minimum required: {MIN_PAGE_COUNT}")
        print("|          Model must investigate more thoroughly")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Page count: {unique_count} unique pages ({total_wiki} total Wikipedia URLs)")

    # Step 2: Check history feature used
    print("|")
    print("| [CHECK 2] View History Feature Used")

    history_count, history_urls = check_history_feature_used(urls)
    if history_count < 3:
        print(f"| [FAILED] Only {history_count} history pages visited")
        print("|          Need to use View History for all 3 frameworks")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] History pages visited: {history_count}")

    # Step 3: Check diff pages viewed
    print("|")
    print("| [CHECK 3] Diff Pages Viewed")

    diff_count, diff_urls = check_diff_pages_viewed(urls)
    if diff_count < 3:
        print(f"| [FAILED] Only {diff_count} diff pages viewed")
        print("|          Need to view actual changes for all 3 frameworks")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Diff pages viewed: {diff_count}")

    # Step 4: Check user pages visited
    print("|")
    print("| [CHECK 4] User Pages Visited")

    user_count, user_urls = check_user_pages_visited(urls)
    if user_count < 3:
        print(f"| [FAILED] Only {user_count} user pages visited")
        print("|          Need to verify contributor credibility for all frameworks")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] User pages visited: {user_count}")

    # Step 5: Check all frameworks investigated
    print("|")
    print("| [CHECK 5] All Frameworks Investigated")

    frameworks_found, missing = check_all_frameworks_investigated(text)
    if missing:
        print(f"| [FAILED] Missing frameworks: {missing}")
        print("|          Model MUST investigate all 3 frameworks")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] All 3 frameworks investigated")

    # Step 6: Check investigation log
    print("|")
    print("| [CHECK 6] Investigation Log Present")

    log_check = check_investigation_log(text)
    if not log_check["ok"]:
        print("| [FAILED] No investigation log found")
        print("|          Must include <investigation_log> with entries")
        print("=" * 70)
        return False
    elif log_check["entries"] < 4:
        print(f"| [FAILED] Investigation log too short: {log_check['entries']} entries")
        print("|          Need at least 4 entries (1 per framework minimum)")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Investigation log found: {log_check['entries']} entries")

    # Step 7: Check original authors identified
    print("|")
    print("| [CHECK 7] Original Authors Identified")

    authors = check_original_authors_identified(text)
    if len(authors) < 3:
        print(f"| [FAILED] Only {len(authors)}/3 frameworks have identified authors")
        print("|          Must identify original author for each framework")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Authors identified for all frameworks")
        for fw, author in authors.items():
            print(f"|       {fw}: {author[:30]}...")

    # Step 8: Check dates added
    print("|")
    print("| [CHECK 8] Dates Added Identified")

    dates = check_dates_added(text)
    if len(dates) < 3:
        print(f"| [WARN] Only {len(dates)}/3 frameworks have identified dates")
        print("|        Dates are recommended for complete verification")
    else:
        print(f"| [OK] Dates identified for all frameworks")

    # Step 9: Check user verification
    print("|")
    print("| [CHECK 9] User Verification")

    verified_count, credibility_count = check_user_verified(text)
    if verified_count < 3:
        print(f"| [WARN] Only {verified_count}/3 users verified")
        print("|        Should verify user credibility for all frameworks")
    else:
        print(f"| [OK] Users verified: {verified_count}/3")

    # Step 10: Check final answer
    print("|")
    print("| [CHECK 10] Final Answer Present")

    answer_check = check_final_answer(text)
    if not answer_check["ok"]:
        print("| [FAILED] No final answer found")
        print("|          Must include <final_answer> identifying which framework's info was added first")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Final answer: {answer_check['answer']}")
        print(f"|       Full: {answer_check['full_answer'][:50]}...")

    # Success!
    print("|")
    print(f"| [PASSED] All verification checks passed!")
    print(f"|          Pages visited: {unique_count}")
    print(f"|          History pages: {history_count}")
    print(f"|          Diff pages: {diff_count}")
    print(f"|          User pages: {user_count}")
    print(f"|          Log entries: {log_check['entries']}")
    print(f"|          Authors identified: {len(authors)}/3")
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
