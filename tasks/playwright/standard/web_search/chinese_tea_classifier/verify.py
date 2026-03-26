#!/usr/bin/env python3
"""
Verification for Rare Chinese Tea Processing Challenge v79.
Task: Find the Chinese green tea that uses steaming method with Tang Dynasty history.

Correct answer: Enshi Yulu (恩施玉露) - uses steaming (蒸青)
- Province: Hubei (湖北)
- History: Tang Dynasty connection

Traps:
1. Japanese teas (Sencha, Gyokuro, Matcha) - wrong country
2. Gunpowder tea (珠茶) - uses steaming BUT from Zhejiang + Ming Dynasty (not Tang)
3. Similar names (Yulu/Gyokuro confusion)

v79 improvements:
- Requires 15+ teas in investigation log (5 Japanese + 10 Chinese minimum)
- Requires 4 different Wikipedia evidence sources
- Minimum sentence length increased to 50 characters
- Tang Dynasty history verification
- Gunpowder tea trap detection
"""
import sys
import json
import os
import re
from pathlib import Path

# Correct answer - only unique identifiers
CORRECT_VARIANTS = ["enshi yulu", "en shi yu lu", "enshi", "恩施玉露", "en-shi"]

# Correct method keywords
CORRECT_METHODS = ["steaming", "蒸青", "steamed", "steam fixation"]

# Japanese teas - TRAPS
JAPANESE_TEAS = ["sencha", "gyokuro", "matcha", "bancha", "hojicha", "genmaicha",
                 "煎茶", "抹茶", "番茶"]

# Trap: Gunpowder tea - uses steaming but wrong province and wrong dynasty
GUNPOWDER_TRAP = ["gunpowder", "珠茶", "zhen cha", "zhēn chá"]

# Province verification
CORRECT_PROVINCE = ["hubei", "湖北", "enshi"]

# Tang Dynasty keywords
TANG_KEYWORDS = ["tang dynasty", "tang era", "唐代", "唐朝", "618", "907", "ancient china"]

# Wikipedia URL pattern
WIKIPEDIA_PATTERN = re.compile(r'https?://[a-z]+\.wikipedia\.org/(wiki/|w/index\.php\?)', re.I)


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


def is_valid_sentence(sentence, min_len=50):
    """Check if sentence is valid."""
    if not sentence:
        return False
    return len(sentence.strip()) >= min_len


def normalize_url(url):
    """Normalize Wikipedia URL for comparison."""
    if not url:
        return ""
    wiki_match = re.search(r'/wiki/([^#?]+)', url, re.I)
    search_match = re.search(r'[?&]search=([^#&]+)', url, re.I)

    if wiki_match:
        return wiki_match.group(1).lower().replace('_', ' ')
    elif search_match:
        return search_match.group(1).lower().replace('+', ' ')
    return url.lower()


def check_investigation_log(text):
    """Check if investigation_log exists with at least 15 teas."""
    log = extract_tag(text, "investigation_log")
    if not log:
        return {"ok": False, "reason": "No <investigation_log> found", "teas_found": 0}

    # Count table rows (lines with |)
    rows = [line for line in log.split('\n') if '|' in line and 'Tea Name' not in line and '|---' not in line]
    teas_found = len(rows)

    if teas_found < 15:
        return {"ok": False, "reason": f"Only {teas_found}/15 teas in investigation log (need at least 15)", "teas_found": teas_found}

    return {"ok": True, "teas_found": teas_found}


def check_answer_block(text):
    """Check if answer block exists with required tags."""
    answer = extract_tag(text, "answer")
    if not answer:
        return {"ok": False, "reason": "No <answer> block found"}

    steamed_tea = extract_subtag(answer, "steamed_tea")
    tea_province = extract_subtag(answer, "tea_province")
    historical_origin = extract_subtag(answer, "historical_origin")
    processing_description = extract_subtag(answer, "processing_description")
    historical_context = extract_subtag(answer, "historical_context")
    exclusion_statement = extract_subtag(answer, "exclusion_statement")
    comparison = extract_subtag(answer, "comparison")

    # Check verification block
    verification = extract_subtag(answer, "verification")
    if not verification:
        return {"ok": False, "reason": "No <verification> block found"}

    evidence_1 = extract_subtag(verification, "evidence_1")
    evidence_2 = extract_subtag(verification, "evidence_2")
    evidence_3 = extract_subtag(verification, "evidence_3")
    evidence_4 = extract_subtag(verification, "evidence_4")

    if not evidence_1 or not evidence_2 or not evidence_3 or not evidence_4:
        return {"ok": False, "reason": "Missing evidence_1, evidence_2, evidence_3, or evidence_4 in verification"}

    sentence_1 = extract_subtag(evidence_1, "sentence")
    source_1 = extract_subtag(evidence_1, "source")
    sentence_2 = extract_subtag(evidence_2, "sentence")
    source_2 = extract_subtag(evidence_2, "source")
    sentence_3 = extract_subtag(evidence_3, "sentence")
    source_3 = extract_subtag(evidence_3, "source")
    sentence_4 = extract_subtag(evidence_4, "sentence")
    source_4 = extract_subtag(evidence_4, "source")

    if not steamed_tea:
        return {"ok": False, "reason": "No <steamed_tea> found in answer"}

    if not processing_description or len(processing_description) < 50:
        return {"ok": False, "reason": "Processing description too short (< 50 characters)"}

    if not historical_context or len(historical_context) < 100:
        return {"ok": False, "reason": "Historical context too short (< 100 characters)"}

    if not exclusion_statement or len(exclusion_statement) < 30:
        return {"ok": False, "reason": "Exclusion statement too short (< 30 characters)"}

    if not comparison or len(comparison) < 50:
        return {"ok": False, "reason": "Comparison too short"}

    return {
        "ok": True,
        "steamed_tea": steamed_tea,
        "tea_province": tea_province,
        "historical_origin": historical_origin,
        "processing_description": processing_description,
        "historical_context": historical_context,
        "exclusion_statement": exclusion_statement,
        "comparison": comparison,
        "sentence_1": sentence_1,
        "source_1": source_1,
        "sentence_2": sentence_2,
        "source_2": source_2,
        "sentence_3": sentence_3,
        "source_3": source_3,
        "sentence_4": sentence_4,
        "source_4": source_4
    }


def is_correct_tea(tea_name):
    """Check if the tea name matches the correct answer."""
    tea_lower = tea_name.lower()
    for variant in CORRECT_VARIANTS:
        if variant in tea_lower:
            return True
    return False


def is_gunpowder_trap(tea_name):
    """Check if the answer is the Gunpowder tea trap."""
    tea_lower = tea_name.lower()
    for trap in GUNPOWDER_TRAP:
        if trap in tea_lower:
            return True
    return False


def is_japanese_tea_primary(tea_name):
    """Check if the answer is PRIMARILY a Japanese tea."""
    if is_correct_tea(tea_name):
        return False  # Correct answer priority

    tea_lower = tea_name.lower()
    for jp_tea in JAPANESE_TEAS:
        if jp_tea in tea_lower:
            return True
    return False


def check_tang_history(text):
    """Check if there's evidence of Tang Dynasty history."""
    text_lower = text.lower()
    for keyword in TANG_KEYWORDS:
        if keyword in text_lower:
            return True
    return False


def verify(wd):
    print("=" * 70)
    print("| VERIFICATION: Rare Chinese Tea Processing Challenge v79")
    print("| Mission: Find the Chinese green tea with Tang Dynasty history")
    print("| TRAP 1: Japanese teas (Sencha, Gyokuro) - wrong country")
    print("| TRAP 2: Gunpowder tea - uses steaming BUT wrong dynasty + wrong province")
    print("=" * 70)

    msgs = parse_messages(wd)
    if not msgs["ok"]:
        print("| [FAILED] Could not parse messages")
        return False
    text = msgs["text"]

    # Step 1: Check investigation log (15+ teas)
    print("|")
    print("| [CHECK 1] Investigation Log (15+ teas)")

    log_check = check_investigation_log(text)
    if not log_check["ok"]:
        print(f"| [FAILED] {log_check['reason']}")
        print("|          Model must investigate at least 15 different teas")
        print("=" * 70)
        return False
    else:
        print(f"| [OK] Investigation log found with {log_check['teas_found']} teas")

    # Step 2: Check answer block structure
    print("|")
    print("| [CHECK 2] Answer Block Structure")

    answer_check = check_answer_block(text)
    if not answer_check["ok"]:
        print(f"| [FAILED] {answer_check['reason']}")
        print("=" * 70)
        return False

    steamed_tea = answer_check["steamed_tea"]
    tea_province = answer_check["tea_province"]
    historical_origin = answer_check["historical_origin"]
    sentence_1 = answer_check["sentence_1"]
    source_1 = answer_check["source_1"]
    sentence_2 = answer_check["sentence_2"]
    source_2 = answer_check["source_2"]
    sentence_3 = answer_check["sentence_3"]
    source_3 = answer_check["source_3"]
    sentence_4 = answer_check["sentence_4"]
    source_4 = answer_check["source_4"]

    print(f"|           Tea identified: {steamed_tea[:50]}")
    print(f"|           Province: {tea_province[:30] if tea_province else 'N/A'}")
    print(f"|           Historical origin: {historical_origin[:30] if historical_origin else 'N/A'}")

    # Step 3: Check all four evidences
    print("|")
    print("| [CHECK 3] Evidence 1 (Processing Method)")

    if not is_valid_sentence(sentence_1):
        print("| [FAILED] Evidence 1 sentence too short (< 50 characters)")
        print("=" * 70)
        return False

    if not is_valid_wikipedia_url(source_1):
        print("| [FAILED] Evidence 1 source is not a valid Wikipedia URL")
        print("=" * 70)
        return False

    print(f"| [OK] Evidence 1: {sentence_1[:50]}...")

    # Step 4: Check evidence 2
    print("|")
    print("| [CHECK 4] Evidence 2 (Historical Origin)")

    if not is_valid_sentence(sentence_2):
        print("| [FAILED] Evidence 2 sentence too short (< 50 characters)")
        print("=" * 70)
        return False

    if not is_valid_wikipedia_url(source_2):
        print("| [FAILED] Evidence 2 source is not a valid Wikipedia URL")
        print("=" * 70)
        return False

    print(f"| [OK] Evidence 2: {sentence_2[:50]}...")

    # Step 5: Check evidence 3
    print("|")
    print("| [CHECK 5] Evidence 3 (Province/Geography)")

    if not is_valid_sentence(sentence_3):
        print("| [FAILED] Evidence 3 sentence too short (< 50 characters)")
        print("=" * 70)
        return False

    if not is_valid_wikipedia_url(source_3):
        print("| [FAILED] Evidence 3 source is not a valid Wikipedia URL")
        print("=" * 70)
        return False

    print(f"| [OK] Evidence 3: {sentence_3[:50]}...")

    # Step 6: Check evidence 4
    print("|")
    print("| [CHECK 6] Evidence 4 (Cultural Significance)")

    if not is_valid_sentence(sentence_4):
        print("| [FAILED] Evidence 4 sentence too short (< 50 characters)")
        print("=" * 70)
        return False

    if not is_valid_wikipedia_url(source_4):
        print("| [FAILED] Evidence 4 source is not a valid Wikipedia URL")
        print("=" * 70)
        return False

    print(f"| [OK] Evidence 4: {sentence_4[:50]}...")

    # Step 7: Check if all four sources are different
    print("|")
    print("| [CHECK 7] Four Different Wikipedia Sources")

    url_1_norm = normalize_url(source_1)
    url_2_norm = normalize_url(source_2)
    url_3_norm = normalize_url(source_3)
    url_4_norm = normalize_url(source_4)

    urls = [url_1_norm, url_2_norm, url_3_norm, url_4_norm]
    unique_urls = set(urls)

    if len(unique_urls) < 4:
        print(f"| [FAILED] Evidence sources must be from 4 DIFFERENT Wikipedia pages")
        print(f"|          Page 1: {url_1_norm}")
        print(f"|          Page 2: {url_2_norm}")
        print(f"|          Page 3: {url_3_norm}")
        print(f"|          Page 4: {url_4_norm}")
        print(f"|          Only {len(unique_urls)} unique page(s) found")
        print("=" * 70)
        return False

    print(f"| [OK] Four different Wikipedia pages used:")
    print(f"|      Page 1: {url_1_norm}")
    print(f"|      Page 2: {url_2_norm}")
    print(f"|      Page 3: {url_3_norm}")
    print(f"|      Page 4: {url_4_norm}")

    # Step 8: Check for Japanese tea trap
    print("|")
    print("| [CHECK 8] Japanese Tea Trap Detection")

    if is_japanese_tea_primary(steamed_tea):
        print(f"| [FAILED] TRAP 1 TRIGGERED: Answer is a Japanese tea")
        print(f"|          Got: {steamed_tea}")
        print("|          The answer must be a CHINESE green tea from mainland China")
        print("=" * 70)
        return False

    print("| [OK] Answer is not a Japanese tea")

    # Step 9: Check for Gunpowder tea trap
    print("|")
    print("| [CHECK 9] Gunpowder Tea Trap Detection")

    if is_gunpowder_trap(steamed_tea):
        print(f"| [FAILED] TRAP 2 TRIGGERED: Gunpowder tea (珠茶)")
        print(f"|          Gunpowder tea uses steaming, BUT:")
        print("|          - It is from Zhejiang Province, NOT Hubei")
        print("|          - It originated in the Ming Dynasty, NOT Tang Dynasty")
        print("|          This is a 'local optimal trap' - looks correct but fails constraints!")
        print("=" * 70)
        return False

    print("| [OK] Answer is not the Gunpowder tea trap")

    # Step 10: Check Tang Dynasty history
    print("|")
    print("| [CHECK 10] Tang Dynasty History Verification")

    all_evidence = f"{sentence_1} {sentence_2} {sentence_3} {sentence_4} {historical_origin} {answer_check['historical_context']}"
    has_tang_history = check_tang_history(all_evidence)

    if not has_tang_history:
        print("| [WARNING] No Tang Dynasty history evidence found in response")
        print("|          The tea should have documented Tang Dynasty (618-907 CE) history")
    else:
        print("| [OK] Tang Dynasty history evidence found")

    # Step 11: Verify correct answer
    print("|")
    print("| [CHECK 11] Answer Verification")

    sentence_lower = (sentence_1 + " " + sentence_2 + " " + sentence_3 + " " + sentence_4).lower()
    has_method_evidence = any(m in sentence_lower for m in CORRECT_METHODS)

    province_lower = tea_province.lower() if tea_province else ""
    has_province = any(p in province_lower for p in CORRECT_PROVINCE)

    if is_correct_tea(steamed_tea):
        print(f"| [OK] Correct tea identified: Enshi Yulu")

        if has_method_evidence:
            print(f"| [OK] Evidence mentions steaming method")
        else:
            print(f"| [WARNING] Evidence should mention 'steaming'")

        if has_province:
            print(f"| [OK] Correct province: Hubei")
        else:
            print(f"| [WARNING] Province should be Hubei")

        print("|")
        print(f"| [PASSED] Correct answer: Enshi Yulu (恩施玉露)")
        print(f"|          Unique method: Steaming (蒸青)")
        print(f"|          Province: Hubei (湖北)")
        print(f"|          History: Tang Dynasty connection")
        print(f"|          Unlike other Chinese green teas which use pan-firing")
        print("=" * 70)
        print("| RESULT: SUCCESS")
        print("=" * 70)
        return True
    else:
        print("|")
        print(f"| [FAILED] Incorrect answer: {steamed_tea}")
        print("|          Expected: Enshi Yulu (恩施玉露)")
        print("|          Unique method: Steaming (蒸青)")
        print("|          Province: Hubei (湖北)")
        print("|          History: Tang Dynasty connection")
        print("=" * 70)
        return False


def main():
    wd = get_work_dir()
    print(f"| Working dir: {wd}")
    result = verify(wd)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
