# JavaScript Framework History Investigator (v59)

## Task

You are a **Wikipedia Edit History Analyst**. Your mission is to investigate the edit history of JavaScript frameworks on Wikipedia to find the ORIGINAL authors who first added "Initial release" information, and determine which framework's "Initial release" was added FIRST chronologically.

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

## Requirements

- You MUST investigate Wikipedia's edit history for each framework
- You MUST find the ORIGINAL authors who FIRST added the information (not recent editors)
- You MUST view diff pages to confirm who actually added the content
- You MUST compare dates across all frameworks to determine which was added first

**Key Tools**: Wikipedia's "View history" feature, "Find addition/removal" tool, or external tools like WikiBlame can help you find when content was first added.

.

### IMPORTANT: Original Authors vs Recent Editors

**The Trap**: Recent editors often make minor corrections (spelling, formatting) to existing content. The ORIGINAL author is the person who FIRST added the information.

- Be careful of edits by bots or IP addresses - these are not real authors
- Check if the username looks like a regular Wikipedia username (not an IP address or bot name)

***

## FRAMEWORKS TO INVESTIGATE

**CRITICAL**: You must investigate ALL FOUR frameworks before providing your answer.

| # | Framework | Find: Initial Release Author |
|---|-----------|------------------------------|
| 1 | React | Who FIRST added "Initial release"? |
| 2 | Vue.js | Who FIRST added "Initial release"? |
| 3 | Angular | Who FIRST added "Initial release"? |
| 4 | Svelte | Who FIRST added "Initial release"? |

**Starting point**: <https://en.wikipedia.org/wiki/Comparison_of_JavaScript-based_web_frameworks>

From this page, click on each framework's link to navigate to its Wikipedia page.

***

## What You Need to Find

For each framework, find:
1. **Author**: Who FIRST added the "Initial release" information (username only, not IP address or bot)
2. **Date**: When was this information first added (YYYY-MM-DD)

Then compare dates to determine:
- **Which framework's "Initial release" was added FIRST chronologically?**
- **What was the date?**

**CRITICAL**: The first_framework must have the EARLIEST date among all four frameworks. If React was added on 2015-01-02, Vue on 2017-03-11, Angular on 2017-03-05, and Svelte on 2019-12-19, then React is the first (2015-01-02 is earliest).

***

## REQUIRED Output Format

**CRITICAL**: You MUST output your final answer using EXACTLY these XML tags. Do NOT use Markdown, JSON, or any other format.

```xml
<answer>
<react_author>username</react_author>
<react_date>YYYY-MM-DD</react_date>

<vue_author>username</vue_author>
<vue_date>YYYY-MM-DD</vue_date>

<angular_author>username</angular_author>
<angular_date>YYYY-MM-DD</angular_date>

<svelte_author>username</svelte_author>
<svelte_date>YYYY-MM-DD</svelte_date>

<first_framework>FrameworkName</first_framework>
<first_date>YYYY-MM-DD</first_date>
</answer>
```

### Example (format only - usernames/dates are fictional placeholders)

```xml
<answer>
<react_author>ExampleUser123</react_author>
<react_date>2015-01-15</react_date>

<vue_author>DemoContributor</vue_author>
<vue_date>2017-03-20</vue_date>

<angular_author>SampleEditor99</angular_author>
<angular_date>2017-03-10</angular_date>

<svelte_author>TestWriter2020</svelte_author>
<svelte_date>2019-12-25</svelte_date>

<first_framework>ExampleFramework</first_framework>
<first_date>2015-01-15</first_date>
</answer>
```

***

## CRITICAL WARNINGS

- **Do NOT** just read the current page - you MUST use View history
- **Do NOT** assume recent editors are original authors
- **Do NOT** include bot usernames or IP addresses as authors
- **Do NOT** use company names or framework creators as authors (e.g., "Facebook", "Evan You")
- **Do NOT** use Markdown, JSON, or any format other than the required XML format above
- **Do NOT** fabricate editor information
- **Do NOT** skip any framework - you must investigate ALL FOUR
- **Do NOT** guess the first framework - you MUST compare all dates and pick the EARLIEST one
