# JavaScript Framework History Investigator (v41)

## Task

You are a **Wikipedia Edit History Analyst**. Your mission is to investigate the sources of "Initial release" information for JavaScript frameworks by tracing their edit history to find ORIGINAL authors.

***

## CRITICAL: This Task Requires Wikipedia History Features

You MUST use Wikipedia's built-in history and comparison tools. Simply reading the current page will NOT give you the answer.

### Required Actions
1. **Navigate** to each framework's Wikipedia page
2. **Click "View history" tab** to access edit history
3. **Use "Find addition/removal" tool** to find ORIGINAL authors (NOT just browse history)
4. **View diff pages** to confirm who FIRST added the content
5. **Visit editor user pages** to verify credibility
6. **Record findings** in the investigation log

### IMPORTANT: How to Find Original Authors Efficiently

**Do NOT just click "older 50" repeatedly** - this is inefficient and will waste time.

Instead, use the **"Find addition/removal"** tool (external tool link on the history page):
1. Go to the framework's Wikipedia page
2. Click **"View history"** tab at the top
3. Look for a link like **"Find addition/removal"** or use the external tool
4. Enter search terms like "Initial release" or "released"
5. Select **"From earliest"** to search from the oldest edits
6. Click **"Start"** to search
7. The tool will show you when the content was FIRST added and by whom

***

## THREE TRAPS TO AVOID

### Trap 1: The "Recent Editor" Trap
**The Mistake**: Assuming the most recent editor who touched the content is the original author.

**Why It's Wrong**: Many editors make minor corrections (spelling, formatting) to existing content.

**How to Avoid**: Use the "Find addition/removal" tool to find the FIRST person who added the content.

### Trap 2: The "High-Frequency Editor" Trap
**The Mistake**: Assuming the editor with the most edits is the most reliable.

**Why It's Wrong**: Some users make many small, low-quality edits (fixing typos). High edit count does NOT equal expertise.

**How to Avoid**: Visit the editor's user page and check their topic expertise, not just edit count.

### Trap 3: The "Admin User" Trap
**The Mistake**: Assuming administrators or experienced users are the original authors.

**Why It's Wrong**: An administrator may have reverted vandalism or made maintenance edits, not added original content.

**How to Avoid**: Use the "Find addition/removal" tool to find who ACTUALLY added the content, regardless of their user status.

***

## FRAMEWORKS TO INVESTIGATE

**CRITICAL**: You must investigate ALL THREE frameworks before providing your answer.

| # | Framework | What to Find |
|---|-----------|--------------|
| 1 | React | Who originally added the "Initial release" date? |
| 2 | Vue.js | Who originally added the "Initial release" date? |
| 3 | Angular | Who originally added the "Initial release" date? |

**Starting point**: <https://en.wikipedia.org/wiki/Comparison_of_JavaScript-based_web_frameworks>

From this page, click on each framework's link to navigate to its Wikipedia page.

***

## What You Need to Find

For each framework, determine:
- **Original Author**: Who FIRST added the "Initial release" information (not recent editors!)
- **Date Added**: When the information was first added
- **Author Credibility**: Is the editor a reliable source?

## How to Investigate

Wikipedia provides tools to investigate edit history:
- The **"View history"** tab shows all past revisions of a page
- The **"Find addition/removal"** tool can locate when specific content was added
- **User pages** show information about each editor

You must use these tools to trace back to the ORIGINAL author who first added the "Initial release" information.

**Record your investigation process** - which pages you visited and what you found

***

## REQUIRED Output Format

```xml
<framework_investigation>

<framework name="React">
  <original_author>[Username of ORIGINAL editor who FIRST added Initial release]</original_author>
  <date_added>[Date when content was FIRST added - format: YYYY-MM-DD]</date_added>
  <edit_summary>[Edit summary from the revision, or "N/A" if none]</edit_summary>
  <user_page_checked>YES/NO</user_page_checked>
  <credibility_notes>[Brief note about user's credibility based on their user page]</credibility_notes>
</framework>

<framework name="Vue.js">
  <original_author>[Username]</original_author>
  <date_added>[YYYY-MM-DD]</date_added>
  <edit_summary>[Edit summary or N/A]</edit_summary>
  <user_page_checked>YES/NO</user_page_checked>
  <credibility_notes>[Brief note]</credibility_notes>
</framework>

<framework name="Angular">
  <original_author>[Username]</original_author>
  <date_added>[YYYY-MM-DD]</date_added>
  <edit_summary>[Edit summary or N/A]</edit_summary>
  <user_page_checked>YES/NO</user_page_checked>
  <credibility_notes>[Brief note]</credibility_notes>
</framework>

<investigation_log>
- [Record each page you visited]
- [Example: "Visited React Wikipedia page via link from comparison page"]
- [Example: "Clicked View history tab"]
- [Example: "Used Find addition/removal tool to search 'Initial release'"]
- [Example: "Found edit by [username] on [date] adding initial release info"]
- [Continue for all frameworks...]
</investigation_log>

<final_answer>
Which framework's "Initial release" information was added FIRST chronologically (by edit date)?
[Framework name]
</final_answer>

</framework_investigation>
```

***

## Success Criteria

Your answer will be verified against these requirements:

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Accessed "View history" tab for each framework | Required |
| 2 | Used "Find addition/removal" tool | Required |
| 3 | Viewed diff pages to see actual changes | Required |
| 4 | Visited editor user pages | Required |
| 5 | Found ORIGINAL authors for all 3 frameworks | Required |
| 6 | Investigation log with entries | Required |
| 7 | Final answer present | Required |

***

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

- `browser_navigate` - Go to URLs
- `browser_click` - Click on elements (links, tabs, buttons)
- `browser_read` - Read page content
- `browser_snapshot` - See page structure
- `browser_type` - Type text into input fields
- `browser_wait_for` - Wait for content to load

Do NOT spawn a process or manually start the MCP process.

***

## CRITICAL WARNINGS

- **Do NOT** just read the current page - you MUST use View history
- **Do NOT** just click "older 50" repeatedly - use the "Find addition/removal" tool
- **Do NOT** assume recent editors are original authors
- **Do NOT** skip the diff viewing step
- **Do NOT** skip visiting user pages
- **Do NOT** fabricate editor information

***

## Tips for Success

1. **Use "Find addition/removal" tool** - This is the most efficient way to find original authors
2. **Be thorough** - Investigate all 3 frameworks completely
3. **Take notes** - Record findings in your investigation log as you go
4. **Verify credibility** - Visit user pages to assess editor reliability
5. **Record original dates** - When was the content FIRST added, not last modified
