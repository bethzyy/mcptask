# Wikipedia Framework Release Investigator (v71)

## Task

You are a **Wikipedia Edit History Analyst**. Your mission is to investigate the edit history of JavaScript framework articles on Wikipedia, find the **original editor** who first added "Initial release" information for each framework, and determine which framework's "Initial release" entry was added **first chronologically**.

**CRITICAL**: You must conduct a thorough investigation of ALL FOUR frameworks. Superficial research or guessing will be detected.

***

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

- `browser_navigate` - Go to URLs
- `browser_click` - Click on elements (links, tabs, buttons, checkboxes)
- `browser_read` - Read page content
- `browser_snapshot` - See page structure
- `browser_type` - Type text into input fields
- `browser_wait_for` - Wait for content to load

Do NOT spawn a process or manually start the MCP process.

***

## Requirements

### What to Investigate

For each framework listed below, you must find:

1. **Username** of the Wikipedia editor who **FIRST** added "Initial release" information to that framework's **own Wikipedia article** (e.g., the Vue.js article for Vue.js — NOT the comparison page)
2. **Date** when this information was first added to that framework's own article (YYYY-MM-DD format)

Then compare dates across all four frameworks to determine which framework's "Initial release" was added **earliest**.

### Frameworks to Investigate

You MUST investigate **all four** frameworks before providing your answer.

| # | Framework |
|---|-----------|
| 1 | React |
| 2 | Vue.js |
| 3 | Angular |
| 4 | Svelte |

**Starting point**: <https://en.wikipedia.org/wiki/Comparison_of_JavaScript-based_web_frameworks>

### Key Distinction: Original Editor vs Recent Editor

**The Trap**: Recent editors often make minor corrections (spelling, formatting) to existing content. The **original editor** is the person who **first added** the "Initial release" information.

- Do NOT confuse the framework's creator (e.g., "Jordan Walke" for React) with the Wikipedia editor who added the info
- Do NOT accept bot usernames or IP addresses as valid editors
- You must verify that the identified editor genuinely added the "Initial release" information, not just made corrections to existing content

### Wikipedia Page Interactions

Wikipedia's edit history pages provide built-in tools for investigation, including:

- **Filter revisions** — the filter panel allows filtering by date range, user, or tags
- **Search within history** — the history search box finds edits matching specific terms
- **Sort revisions** — sort by date, author, or edit size
- **View diffs** — click on revision links to see exactly what content was added or changed

***

## REQUIRED Output Format

**CRITICAL**: You MUST output your final answer using EXACTLY these XML tags. Do NOT use Markdown, JSON, or any other format.

```xml
<answer>
<first_framework>FrameworkName</first_framework>
<first_author>username</first_author>
<first_date>YYYY-MM-DD</first_date>
<all_dates>
<framework name="React" author="username">YYYY-MM-DD</framework>
<framework name="Vue.js" author="username">YYYY-MM-DD</framework>
<framework name="Angular" author="username">YYYY-MM-DD</framework>
<framework name="Svelte" author="username">YYYY-MM-DD</framework>
</all_dates>
</answer>
```

### Example (format only — all values below are fictional placeholders)

```xml
<answer>
<first_framework>SomeFramework</first_framework>
<first_author>SomeWikipediaEditor</first_author>
<first_date>2016-06-15</first_date>
<all_dates>
<framework name="React" author="SomeEditor1">2014-05-29</framework>
<framework name="Vue.js" author="SomeEditor2">2016-09-18</framework>
<framework name="Angular" author="SomeEditor3">2016-11-14</framework>
<framework name="Svelte" author="SomeEditor4">2018-07-23</framework>
</all_dates>
</answer>
```

The `first_framework` must be the framework whose "Initial release" was added earliest among all four. The `first_author` must be the Wikipedia username (not a framework creator's name), and `first_date` must be in YYYY-MM-DD format. The `all_dates` section must include the date and the Wikipedia editor's username for **each** framework.

***

## CRITICAL WARNINGS

- **Do NOT** use framework creators' names as Wikipedia editors (e.g., "Jordan Walke", "Evan You")
- **Do NOT** include bot usernames or IP addresses as authors
- **Do NOT** guess — verify your findings against actual Wikipedia edit history
