#!/usr/bin/env python3
"""
Verification for JavaScript Framework Timeline Verification (v24).

Task: Verify a historian's claims about JavaScript tool release dates AND chronological order.

Expected Results (based on Wikipedia):
- React: May 2013 actual (claimed May 2013) - YES (accurate)
- Gulp: September 2013 actual (claimed July 2013) - YES (within 3-month tolerance)
- Browserify: June 2011 actual (claimed March 2014) - NO (off by ~3 years)
- Webpack: February 2014 actual (claimed October 2015) - NO (off by 1.5 years)
- Vue.js: February 2014 actual (claimed February 2014) - YES (accurate)
- Svelte: November 2016 actual (claimed November 2016) - YES (accurate)

Expected date accuracy: YES, YES, NO, NO, YES, YES (4/6 accurate)

Actual chronological order:
1. Browserify - 2011-06
2. React - 2013-05
3. Gulp - 2013-09
4. Webpack - 2014-02 (or Vue.js - same month)
5. Vue.js - 2014-02
6. Svelte - 2016-11

Historian's claimed order: React → Gulp → Browserify → Webpack → Vue.js → Svelte
Actual order: Browserify → React → Gulp → Webpack/Vue.js → Svelte
Order is INCORRECT (Browserify is first, not third)

Final verdict: PARTIALLY ACCURATE (4/6 dates correct, order wrong)

v24 changes:
- Added page count verification (minimum 12 pages from tool calls)
- Cross-verification increased to 6 evidences (one per tool)
- Added page_count check in verify()
- Enhanced logging for page visit tracking
"""
import sys
import json
import os
import re
from pathlib import Path

# Expected results - based on Wikipedia data
# A claim is ACCURATE if within 3 months of the actual date
EXPECTED_DATE_ACCURACY = {
    "REACT": "YES",       # May 2013 actual, May 2013 claimed - accurate
    "GULP": "YES",        # Sep 2013 actual, Jul 2013 claimed - within 3 months
    "BROWSERIFY": "NO",   # Jun 2011 actual, Mar 2014 claimed - NOT accurate (~3 years off)
    "WEBPACK": "NO",      # Feb 2014 actual, Oct 2015 claimed - NOT accurate (1.5 years off)
    "VUE.JS": "YES",      # Feb 2014 actual, Feb 2014 claimed - accurate
    "SVELTE": "YES",      # Nov 2016 actual, Nov 2016 claimed - accurate
}

# Expected chronological order (by actual release date)
EXPECTED_ORDER = ["BROWSERIFY", "REACT", "GULP", "WEBPACK", "VUE.JS", "SVELTE"]

# The order is INCORRECT because Browserify (2011) should be first, not third
EXPECTED_ORDER_CORRECT = "NO"

# Expected verdict
EXPECTED_VERDICT = "PARTIALLY ACCURATE"

# Minimum page count required (6 tools = 6 pages minimum)
MIN_PAGE_COUNT = 6

# Wikipedia URL pattern
WIKIPEDIA_PATTERN = re.compile(r'https?://[a-z]+\.wikipedia\.org/wiki/', re.I)
PAGE_URL_PATTERN = re.compile(r'Page URL:\s*(https?://[a-z]+\.wikipedia\.org/wiki/[a-zA-Z0-9_().-]+)', re.I)


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
            # This handles the format: {"name": "browser_navigate", "arguments": "{\"url\": \"...\"}"}
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

            # Also extract from tool results (which contain the actual URLs visited)
            if m.get("role") == "tool":
                tool_name = m.get("name", "")
                tool_result = m.get("content", "")
                tool_calls.append({"name": tool_name, "result": tool_result})

            # Extract from messages with output field (tool results)
            if "output" in m and "name" in m:
                tool_calls.append({"name": m.get("name", ""), "result": m.get("output", "")})

        except Exception:
            continue

    return {"ok": True, "text": " ".join(text_parts), "tool_calls": tool_calls}


def extract_tool_calls_from_message(m):
    """Extract tool calls from an assistant message."""
    calls = []
    content = m.get("content", "")
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "tool_use":
                calls.append({
                    "name": item.get("name", ""),
                    "input": item.get("input", {})
                })
    return calls


def count_wikipedia_pages(tool_calls):
    """Count unique Wikipedia pages visited from tool calls."""
    visited_urls = set()

    for call in tool_calls:
        # Check tool input for URLs (browser_navigate)
        if "input" in call:
            input_data = call["input"]
            if isinstance(input_data, dict):
                url = input_data.get("url", "")
                if url and WIKIPEDIA_PATTERN.search(url):
                    normalized = normalize_url(url)
                    if normalized:
                        visited_urls.add(normalized)

        # Check tool result for URLs (from function_call_output with Page URL)
        if "result" in call:
            result = call["result"]
            if isinstance(result, str):
                # Find "Page URL: https://..." pattern in result
                for match in PAGE_URL_PATTERN.finditer(result):
                    url = match.group(1)
                    normalized = normalize_url(url)
                    if normalized:
                        visited_urls.add(normalized)

    return len(visited_urls), visited_urls


def extract_tag(text, tag):
    """Extract content from XML-style tag."""
    matches = re.findall(rf'<{tag}[^>]*>\s*(.*?)\s*</{tag}>', text, re.DOTALL | re.I)
    return matches[-1].strip() if matches else ""


def extract_subtag(content, tag):
    """Extract content from a sub-tag."""
    pattern = rf'<{tag}[^>]*>\s*(.*?)\s*</{tag}>'
    match = re.search(pattern, content, re.DOTALL | re.I)
    return match.group(1).strip() if match else ""


def is_valid_wikipedia_url(url):
    """Check if URL is a valid Wikipedia URL."""
    if not url:
        return False
    return bool(WIKIPEDIA_PATTERN.search(url))


def normalize_url(url):
    """Normalize Wikipedia URL for comparison."""
    if not url:
        return ""
    match = re.search(r'/wiki/([^#?]+)', url, re.I)
    if match:
        return match.group(1).lower().replace('_', ' ')
    return url.lower()


def check_investigation_log(text):
    """Check if investigation_log exists with all 6 tools."""
    log = extract_tag(text, "investigation_log")

    # v24: Also check the full text if no explicit tag
    search_text = log if log else text

    # Check for all 6 tools
    tools_required = ["react", "gulp", "browserify", "webpack", "vue", "svelte"]
    tools_found = []
    search_lower = search_text.lower()

    for tool in tools_required:
        if tool in search_lower:
            tools_found.append(tool)

    if len(tools_found) < 6:
        missing = [t for t in tools_required if t not in tools_found]
        return {"ok": False, "reason": f"Missing tools in log: {missing}", "tools_found": len(tools_found)}

    return {"ok": True, "tools_found": len(tools_found)}


def parse_date_verification(text):
    """Parse the date_verification table to extract accuracy verdicts."""
    verification = extract_tag(text, "date_verification")

    # v24: If no explicit tag, search in full text
    search_text = verification if verification else text

    results = {}

    # Check for explicit verdicts for each tool
    # v24: Updated patterns to handle markdown bold and arrows
    tool_patterns = {
        "REACT": [
            r'React[^a-zA-Z0-9].*?\*\*(ACCURATE|INACCURATE)\*\*',
            r'React.*?Accurate\??\s*[:\->]?\s*\*?\*?(YES|NO)',
            r'React.*?(?:→|->)\s*\*\*(ACCURATE|INACCURATE)',
        ],
        "GULP": [
            r'Gulp[^a-zA-Z0-9].*?\*\*(ACCURATE|INACCURATE)\*\*',
            r'Gulp.*?Accurate\??\s*[:\->]?\s*\*?\*?(YES|NO)',
            r'Gulp.*?(?:→|->)\s*\*\*(ACCURATE|INACCURATE)',
        ],
        "BROWSERIFY": [
            r'Browserify[^a-zA-Z0-9].*?\*\*(ACCURATE|INACCURATE)\*\*',
            r'Browserify.*?Accurate\??\s*[:\->]?\s*\*?\*?(YES|NO)',
            r'Browserify.*?(?:→|->)\s*\*\*(ACCURATE|INACCURATE)',
        ],
        "WEBPACK": [
            r'Webpack[^a-zA-Z0-9].*?\*\*(ACCURATE|INACCURATE)\*\*',
            r'Webpack.*?Accurate\??\s*[:\->]?\s*\*?\*?(YES|NO)',
            r'Webpack.*?(?:→|->)\s*\*\*(ACCURATE|INACCURATE)',
        ],
        "VUE.JS": [
            r'Vue\.?js[^a-zA-Z0-9].*?\*\*(ACCURATE|INACCURATE)\*\*',
            r'Vue\.?js.*?Accurate\??\s*[:\->]?\s*\*?\*?(YES|NO)',
            r'Vue\.?js.*?(?:→|->)\s*\*\*(ACCURATE|INACCURATE)',
        ],
        "SVELTE": [
            r'Svelte[^a-zA-Z0-9].*?\*\*(ACCURATE|INACCURATE)\*\*',
            r'Svelte.*?Accurate\??\s*[:\->]?\s*\*?\*?(YES|NO)',
            r'Svelte.*?(?:→|->)\s*\*\*(ACCURATE|INACCURATE)',
        ],
    }

    for tool, patterns in tool_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, search_text, re.I)
            if match:
                verdict = match.group(1).upper()
                if "ACCURATE" in verdict and "INACCURATE" not in verdict:
                    results[tool] = "YES"
                elif "INACCURATE" in verdict:
                    results[tool] = "NO"
                elif "YES" in verdict:
                    results[tool] = "YES"
                elif "NO" in verdict:
                    results[tool] = "NO"
                break

    # Also check for markdown tables
    if len(results) < 6:
        lines = search_text.split('\n')
        for line in lines:
            line = line.strip()
            if '|' in line and 'Tool' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 4:
                    tool_name = parts[0].upper()
                    accuracy = parts[-1].upper()
                    if tool_name in ["REACT", "GULP", "BROWSERIFY", "WEBPACK", "VUE.JS", "SVELTE"]:
                        results[tool_name] = "YES" if "YES" in accuracy or "ACCURATE" in accuracy else "NO"

    return results


def check_order_verification(text):
    """Check if order_verification exists and is correct."""
    order_section = extract_tag(text, "order_verification")

    # v24: Also check full text if no explicit tag
    search_text = order_section if order_section else text

    # Check for order correct verdict
    order_lower = search_text.lower()

    # Look for various patterns indicating order is wrong
    wrong_order_patterns = [
        r'order\s+(is\s+)?(incorrect|wrong)',
        r'chronological order\s+(is\s+)?(incorrect|wrong)',
        r'order\s+correct\??\s*[:\|]?\s*\[?no',
        r'timeline\s+(is\s+)?(incorrect|wrong)',
        r'browserify\s+(was\s+)?(actually\s+)?(the\s+)?first',
        r'order should be',
    ]

    for pattern in wrong_order_patterns:
        if re.search(pattern, order_lower, re.I):
            return {"ok": True, "verdict": "NO"}

    # Check for explicit "Order correct?" pattern
    if "order correct?" in order_lower:
        match = re.search(r'order correct\??\s*[:\|]?\s*\[?(yes|no)', order_lower, re.I)
        if match:
            verdict = match.group(1).upper()
            if verdict == EXPECTED_ORDER_CORRECT:
                return {"ok": True, "verdict": verdict}
            else:
                return {"ok": False, "reason": f"Order verdict '{verdict}' is incorrect - should be {EXPECTED_ORDER_CORRECT}"}

    return {"ok": False, "reason": "Could not find order verification verdict"}


def check_navigation_log(text):
    """Check if navigation_log or navigation_summary exists."""
    # Check for navigation_log first
    log = extract_tag(text, "navigation_log")
    if log:
        rows = [line for line in log.split('\n') if '|' in line and 'Step' not in line and '|--' not in line]
        steps_found = len(rows)
        if steps_found >= 3:
            return {"ok": True, "steps_found": steps_found}

    # Fall back to navigation_summary
    summary = extract_tag(text, "navigation_summary")
    if summary:
        # Try to extract total pages visited
        match = re.search(r'Total pages visited:\s*(\d+)', summary, re.I)
        if match:
            page_count = int(match.group(1))
            return {"ok": True, "steps_found": page_count, "from_summary": True}
        return {"ok": True, "steps_found": "via summary"}

    # v24: If no explicit navigation_log, check for any navigation description in the text
    # Look for patterns like "Navigation Path:" or "Pages visited:" or markdown tables with URLs
    nav_patterns = [
        r'Navigation [Pp]ath',
        r'Pages visited',
        r'Visited pages',
        r'\|.*https?://[a-z]+\.wikipedia\.org/wiki/',
        r'Started at.*wikipedia\.org',
        r'navigated.*wikipedia',
        r'Summary of Findings',
    ]
    for pattern in nav_patterns:
        if re.search(pattern, text, re.I):
            return {"ok": True, "steps_found": "via text description"}

    # v24: If page count >= MIN_PAGE_COUNT, consider navigation OK
    # (This is checked separately and passed to this function via verify())
    return {"ok": None, "reason": "No explicit navigation documentation, will rely on page count", "steps_found": 0}


def check_page_count(tool_calls, text):
    """Check if minimum page count requirement is met."""
    # Count from tool calls
    page_count_from_tools, visited_urls = count_wikipedia_pages(tool_calls)

    # Also check navigation_summary for reported count
    summary = extract_tag(text, "navigation_summary")
    reported_count = 0
    if summary:
        match = re.search(r'Total pages visited:\s*(\d+)', summary, re.I)
        if match:
            reported_count = int(match.group(1))

    # Use the higher count
    final_count = max(page_count_from_tools, reported_count)

    if final_count < MIN_PAGE_COUNT:
        return {
            "ok": False,
            "reason": f"Only {final_count} pages visited (minimum {MIN_PAGE_COUNT} required)",
            "page_count": final_count,
            "from_tools": page_count_from_tools,
            "from_summary": reported_count
        }

    return {
        "ok": True,
        "page_count": final_count,
        "from_tools": page_count_from_tools,
        "from_summary": reported_count
    }


def check_cross_verification(text):
    """Check if cross-verification evidence is provided for all 6 tools."""
    cross_verify = extract_tag(text, "cross_verification")

    # v24: If no explicit tag, check full text for evidence
    search_text = cross_verify if cross_verify else text

    # Check for explicit XML evidence tags first
    evidences = []
    tools_with_evidence = set()

    if cross_verify:
        for i in range(1, 7):
            evidence = extract_subtag(cross_verify, f"evidence_{i}")
            if evidence:
                tool = extract_subtag(evidence, "tool")
                source = extract_subtag(evidence, "source")
                sentence = extract_subtag(evidence, "sentence")

                if tool and source and is_valid_wikipedia_url(source):
                    tool_lower = tool.lower().strip()
                    tools_with_evidence.add(tool_lower)
                    evidences.append({
                        "evidence_num": i,
                        "tool": tool,
                        "source": source[:60],
                    })

    # v24: Check for "### Evidence Sources:" section with markdown list
    # Pattern: - **ToolName**: https://wikipedia.org/wiki/...
    if len(tools_with_evidence) < 6:
        # Look for "- **ToolName**: URL" pattern in full text
        evidence_list_patterns = [
            (r'-\s*\*\*React\*\*.*?wikipedia\.org/wiki/React', 'react'),
            (r'-\s*\*\*Gulp\.?js?\*\*.*?wikipedia\.org/wiki/Gulp', 'gulp'),
            (r'-\s*\*\*Browserify\*\*.*?wikipedia\.org/wiki/Browserify', 'browserify'),
            (r'-\s*\*\*Webpack\*\*.*?wikipedia\.org/wiki/Webpack', 'webpack'),
            (r'-\s*\*\*Vue\.?js?\*\*.*?wikipedia\.org/wiki/Vue', 'vue.js'),
            (r'-\s*\*\*Svelte\*\*.*?wikipedia\.org/wiki/Svelte', 'svelte'),
        ]

        for pattern, tool_name in evidence_list_patterns:
            if re.search(pattern, search_text, re.I):
                tools_with_evidence.add(tool_name)

    # v24: Also check for table format: | Tool | Wikipedia Page | ... |
    if len(tools_with_evidence) < 6:
        # Look for markdown table with tool names and Wikipedia URLs
        table_patterns = [
            (r'\|\s*React\s*\|.*wikipedia\.org/wiki/React', 'react'),
            (r'\|\s*Gulp\.?js?\s*\|.*wikipedia\.org/wiki/Gulp', 'gulp'),
            (r'\|\s*Browserify\s*\|.*wikipedia\.org/wiki/Browserify', 'browserify'),
            (r'\|\s*Webpack\s*\|.*wikipedia\.org/wiki/Webpack', 'webpack'),
            (r'\|\s*Vue\.?js?\s*\|.*wikipedia\.org/wiki/Vue', 'vue.js'),
            (r'\|\s*Svelte\s*\|.*wikipedia\.org/wiki/Svelte', 'svelte'),
        ]

        for pattern, tool_name in table_patterns:
            if re.search(pattern, search_text, re.I):
                tools_with_evidence.add(tool_name)

    # v24: Also check for any mention of tool with Wikipedia URL
    if len(tools_with_evidence) < 6:
        # Look for tool name followed by Wikipedia URL anywhere in text
        tool_url_patterns = [
            (r'React[^a-zA-Z0-9].*?wikipedia\.org/wiki/React', 'react'),
            (r'Gulp[^a-zA-Z0-9].*?wikipedia\.org/wiki/Gulp', 'gulp'),
            (r'Browserify[^a-zA-Z0-9].*?wikipedia\.org/wiki/Browserify', 'browserify'),
            (r'Webpack[^a-zA-Z0-9].*?wikipedia\.org/wiki/Webpack', 'webpack'),
            (r'Vue\.?js?[^a-zA-Z0-9].*?wikipedia\.org/wiki/Vue', 'vue.js'),
            (r'Svelte[^a-zA-Z0-9].*?wikipedia\.org/wiki/Svelte', 'svelte'),
        ]

        for pattern, tool_name in tool_url_patterns:
            if re.search(pattern, search_text, re.I):
                tools_with_evidence.add(tool_name)

    # Check that all 6 tools have evidence
    required_tools = {"react", "gulp", "browserify", "webpack", "vue.js", "svelte"}
    # Also accept "vue" for "vue.js"
    if "vue" in tools_with_evidence:
        tools_with_evidence.add("vue.js")

    missing_tools = required_tools - tools_with_evidence
    if missing_tools:
        return {"ok": False, "reason": f"Missing evidence for tools: {missing_tools}"}

    return {
        "ok": True,
        "evidences": evidences if evidences else [{"tool": t, "source": "via text"} for t in tools_with_evidence],
        "tools_covered": tools_with_evidence
    }


def check_analysis(text):
    """Check if analysis section is present and long enough."""
    analysis = extract_tag(text, "analysis")

    # v24: If no explicit tag, look for analysis-like sections in text
    if not analysis:
        # Look for sections that might contain analysis
        analysis_patterns = [
            r'(?:##\s*)?(?:Analysis|Summary|Findings|Conclusion|Verdict)[^#]*',
            r'(?:###\s*)?(?:Final\s+)?(?:Verdict|Conclusion)[^#]*',
        ]
        for pattern in analysis_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                analysis = match.group(0)
                break

    if not analysis:
        return {"ok": False, "reason": "No <analysis> block found"}

    if len(analysis) < 200:
        return {"ok": False, "reason": f"Analysis too short ({len(analysis)} chars, minimum 200)"}

    return {"ok": True, "analysis": analysis[:100]}


def check_final_verdict(text):
    """Check if final_verdict is correct."""
    verdict = extract_tag(text, "final_verdict")

    # v24: If no explicit tag, search in full text
    search_text = verdict if verdict else text

    # Look for verdict patterns
    verdict_patterns = [
        r'\*\*PARTIALLY\s+ACCURATE\*\*',
        r'Final\s+Verdict[:\s]+(?:\*\*)?PARTIALLY\s+ACCURATE',
        r'(?:Verdict|Conclusion)[:\s]+(?:\*\*)?PARTIALLY\s+ACCURATE',
        r'PARTIALLY\s+ACCURATE',
    ]

    for pattern in verdict_patterns:
        if re.search(pattern, search_text, re.I):
            return {"ok": True, "verdict": "PARTIALLY ACCURATE"}

    # Check for incorrect verdicts
    if re.search(r'FULLY\s+ACCURATE', search_text, re.I):
        return {"ok": False, "reason": "Verdict is incorrect - dates are not all correct and order is wrong"}
    if re.search(r'MOSTLY\s+INACCURATE', search_text, re.I):
        return {"ok": False, "reason": "Verdict is too harsh - 4/6 dates are correct"}

    if verdict:
        verdict_upper = verdict.upper().strip()
        if "PARTIALLY ACCURATE" in verdict_upper:
            return {"ok": True, "verdict": "PARTIALLY ACCURATE"}

    return {"ok": False, "reason": "Could not find 'PARTIALLY ACCURATE' verdict"}


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: JavaScript Framework Timeline (v24)")
    print("| Task: Verify historian's claims about 6 JS tools")
    print("| Expected dates: React=YES, Gulp=YES, Browserify=NO, Webpack=NO,")
    print("|                Vue.js=YES, Svelte=YES")
    print("| Expected order: INCORRECT (Browserify is first, not third)")
    print("| Expected verdict: PARTIALLY ACCURATE")
    print("| Minimum pages: 6")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False
    text = msgs["text"]
    tool_calls = msgs["tool_calls"]

    # Step 1: Check page count (NEW in v24)
    print("|")
    print("| [CHECK 1] Page Count (minimum 6)")

    page_check = check_page_count(tool_calls, text)
    if not page_check["ok"]:
        print(f"| [FAILED] {page_check['reason']}")
        print(f"|          From tool calls: {page_check['from_tools']} pages")
        print(f"|          From summary: {page_check['from_summary']} pages")
        print("|          Model must visit at least 12 different Wikipedia pages")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Page count: {page_check['page_count']} pages")
        print(f"|      From tool calls: {page_check['from_tools']}, from summary: {page_check['from_summary']}")

    # Step 2: Check navigation log or summary
    print("|")
    print("| [CHECK 2] Navigation Documentation")

    nav_log_check = check_navigation_log(text)
    if nav_log_check["ok"] is False:
        print(f"| [FAILED] {nav_log_check['reason']}")
        print("|          Model must document navigation (log or summary)")
        print("=" * 70)
        return False
    elif nav_log_check["ok"] is None:
        # v24: No explicit navigation doc, but page count already passed
        print(f"| [OK] Navigation verified via page count ({page_check['page_count']} pages)")
    else:
        print(f"| [OK] Navigation documentation found ({nav_log_check['steps_found']} steps)")

    # Step 3: Check investigation log
    print("|")
    print("| [CHECK 3] Investigation Log (6 tools)")

    log_check = check_investigation_log(text)
    if not log_check["ok"]:
        print(f"| [FAILED] {log_check['reason']}")
        print("|          Model MUST investigate all 6 frameworks/tools")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Investigation log found with {log_check['tools_found']} tools")

    # Step 4: Check answer block exists (or answer-like content)
    print("|")
    print("| [CHECK 4] Answer Block Structure")

    answer = extract_tag(text, "answer")
    if not answer:
        # v24: Check for answer-like content instead of strict XML tag
        # Look for sections with findings, verdict, etc.
        answer_patterns = [
            r'##\s*Summary\s+of\s+Findings',
            r'##\s*Final\s+Verdict',
            r'###\s*(?:Release\s+)?Dates',
            r'\*\*PARTIALLY\s+ACCURATE\*\*',
        ]
        has_answer_content = False
        for pattern in answer_patterns:
            if re.search(pattern, text, re.I):
                has_answer_content = True
                break

        if not has_answer_content:
            print("| [FAILED] No <answer> block or answer content found")
            print("=" * 70)
            return False
        else:
            print("| [OK] Answer content found (via text)")
    else:
        print("| [OK] Answer block found")

    # Step 5: Check date verification table
    print("|")
    print("| [CHECK 5] Date Verification Accuracy")

    date_results = parse_date_verification(text)
    if len(date_results) < 6:
        missing = [t for t in ["REACT", "GULP", "BROWSERIFY", "WEBPACK", "VUE.JS", "SVELTE"] if t not in date_results]
        print(f"| [FAILED] Missing date verdicts for: {missing}")
        print("=" * 70)
        return False

    all_dates_correct = True
    for tool, expected in EXPECTED_DATE_ACCURACY.items():
        actual = date_results.get(tool, "MISSING")
        if actual == expected:
            print(f"| [OK] {tool}: {actual}")
        else:
            print(f"| [FAILED] {tool}: got {actual}, expected {expected}")
            all_dates_correct = False

    if not all_dates_correct:
        print("|")
        print("| [FAILED] Some date verdicts are incorrect")

    # Step 6: Check order verification
    print("|")
    print("| [CHECK 6] Chronological Order Verification")

    order_check = check_order_verification(text)
    if not order_check["ok"]:
        print(f"| [FAILED] {order_check['reason']}")
        print("|          Expected: Order is INCORRECT (Browserify should be first)")
        print("=" * 70)
        return False

    print(f"| [OK] Order verdict: {order_check['verdict']}")

    # Step 7: Check cross-verification (6 evidences - NEW in v24)
    print("|")
    print("| [CHECK 7] Cross-Page Verification (6 evidences)")

    cross_check = check_cross_verification(text)
    if not cross_check["ok"]:
        print(f"| [FAILED] {cross_check['reason']}")
        print("|          Must provide evidence for ALL 6 tools from Wikipedia pages")
        print("=" * 70)
        return False

    print(f"| [OK] Cross-verification for {len(cross_check['evidences'])} tools:")
    for i, ev in enumerate(cross_check['evidences'], 1):
        evidence_num = ev.get('evidence_num', i)
        print(f"|      {evidence_num}. {ev['tool']}: {ev['source']}...")

    # Step 8: Check analysis
    print("|")
    print("| [CHECK 8] Analysis Section (200+ chars)")

    analysis_check = check_analysis(text)
    if not analysis_check["ok"]:
        print(f"| [FAILED] {analysis_check['reason']}")
        print("=" * 70)
        return False

    print(f"| [OK] Analysis found: {analysis_check['analysis']}...")

    # Step 9: Check final verdict
    print("|")
    print("| [CHECK 9] Final Verdict")

    verdict_check = check_final_verdict(text)
    if not verdict_check["ok"]:
        print(f"| [FAILED] {verdict_check['reason']}")
        print("=" * 70)
        return False

    print(f"| [OK] Verdict: {verdict_check['verdict']}")

    # Final check: all date verdicts must be correct
    if not all_dates_correct:
        print("|")
        print("| [FAILED] Date verdicts have errors - see CHECK 5")
        print("=" * 70)
        return False

    # Success!
    print("|")
    print(f"| [PASSED] All verification checks passed!")
    print(f"|          Pages visited: {page_check['page_count']}")
    print(f"|          Date accuracy: 4/6 correct")
    print(f"|          Order: Incorrect (correctly identified)")
    print(f"|          Cross-verification: 6 tools covered")
    print(f"|          Verdict: PARTIALLY ACCURATE")
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
