#!/usr/bin/env python3
"""
Verification script for Playwright web search task.
Checks if the AI agent found the correct information about MCPMark.
"""

import sys
import json
import os
import re
from pathlib import Path
from typing import Dict, Any

# =============================================================================
# CONFIGURATION - Expected ground truth answers
# =============================================================================

EXPECTED_ANSWERS = {
    "ARXIV_ID": "2509.24002",
    "FIRST_AUTHOR": "Wu",
    "LICENSE": "Apache",
}

# =============================================================================
# MCP RESULT PARSING
# =============================================================================


def get_working_directory() -> Path:
    """Get the working directory where messages.json should be."""
    # Priority 1: Use MCP_MESSAGES path if available (most reliable)
    messages_path = os.getenv("MCP_MESSAGES")
    if messages_path and Path(messages_path).exists():
        return Path(messages_path).parent.resolve()

    # Priority 2: Use PLAYWRIGHT_WORK_DIR environment variable
    work_dir = os.getenv("PLAYWRIGHT_WORK_DIR")
    if work_dir:
        work_path = Path(work_dir).resolve()
        if (work_path / "messages.json").exists():
            return work_path

    # Priority 3: Check current directory (fallback)
    current_dir = Path.cwd()
    if (current_dir / "messages.json").exists():
        return current_dir

    # Priority 4: Default fallback
    return Path(".").resolve()


def extract_answer_block(content: str) -> Dict[str, str]:
    """Extract the answer block from AI response content."""
    # Look for <answer>...</answer> block
    answer_pattern = r"<answer>\s*(.*?)\s*</answer>"
    match = re.search(answer_pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        return {}

    answer_content = match.group(1).strip()

    # Parse key-value pairs from the answer block
    results = {}
    for line in answer_content.split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            results[key.strip().upper()] = value.strip()

    return results


def parse_ai_results(work_dir: Path) -> Dict[str, Any]:
    """Parse the AI agent's results from messages.json"""
    messages_file = work_dir / "messages.json"
    if not messages_file.exists():
        return {"success": False, "error": "No messages.json found"}

    try:
        with open(messages_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {"success": False, "error": f"Failed to read messages.json: {e}"}

    # Look for answer block in AI's responses
    found_answers = {}

    for message in messages:
        if message.get("role") == "assistant":
            content = str(message.get("content", ""))

            # Handle both string and list content formats
            if isinstance(message.get("content"), list):
                content = " ".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in message.get("content", [])
                )

            # Extract answer block
            answers = extract_answer_block(content)
            if answers:
                found_answers = answers

    return {
        "success": True,
        "found_answers": found_answers,
    }


# =============================================================================
# VERIFICATION LOGIC
# =============================================================================


def verify_task() -> bool:
    """Verify the AI agent found the correct answers"""

    # Parse AI agent results
    work_dir = get_working_directory()
    print(f"| Working directory: {work_dir}")

    ai_results = parse_ai_results(work_dir)

    if not ai_results["success"]:
        print(f"| [FAILED] Could not parse AI results: {ai_results.get('error')}")
        return False

    found_answers = ai_results.get("found_answers", {})

    if not found_answers:
        print(f"| [FAILED] No answer block found in AI response")
        print(f"| Expected format: <answer>ARXIV_ID: ... FIRST_AUTHOR: ... LICENSE: ...</answer>")
        return False

    # Check each expected answer
    all_correct = True
    for key, expected_value in EXPECTED_ANSWERS.items():
        found_value = found_answers.get(key, "")
        if found_value.lower() == expected_value.lower():
            print(f"| [OK] {key}: {found_value}")
        else:
            print(f"| [WRONG] {key}: found '{found_value}', expected '{expected_value}'")
            all_correct = False

    if all_correct:
        print(f"| [SUCCESS] All answers are correct!")
        return True
    else:
        print(f"| [FAILED] Some answers are incorrect")
        return False


def main():
    """Main verification function."""
    try:
        success = verify_task()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Verification error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
