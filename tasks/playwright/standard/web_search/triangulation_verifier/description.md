# JavaScript Framework Timeline Verification (v24)

## Task
A tech historian claims: **"Six major JavaScript tools appeared in this chronological order: React first released in May 2013, then Gulp in July 2013, then Browserify in March 2014, then Webpack in October 2015, then Vue.js in February 2014, then Svelte in November 2016."**

Your mission: Verify BOTH the **release dates** AND the **chronological order** of this timeline.

**IMPORTANT**: You must start from the Wikipedia page below and **navigate using page links only**. Do NOT use Wikipedia search or direct URL navigation.

**Starting point**: <https://en.wikipedia.org/wiki/Comparison_of_JavaScript-based_web_frameworks>

***

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a process or manually start the MCP process.

***

## BACKGROUND

The historian's timeline has TWO potential issues:

1. **Date Accuracy**: Each claimed release date may be correct or incorrect
2. **Chronological Order**: The claimed order may not match the actual release order

**Key concept**: The "Initial release" date in Wikipedia infoboxes represents the first public release. A claim is ACCURATE if the actual date is within 3 months of the claimed date.

***

## NAVIGATION REQUIREMENTS

**CRITICAL**: You must follow this navigation pattern:

1. **Start** from the Comparison of JavaScript-based web frameworks page
2. **Find links** to each tool's Wikipedia page within the content
3. **Click through** to navigate - do NOT use search or type URLs directly
4. **Use browser_navigate_back** to return to previous pages when needed
5. **Record each navigation step** in your investigation log

**If a tool is not linked from the starting page**, you must:
- Navigate to related pages (e.g., JavaScript libraries list, related frameworks)
- Find links from those related pages
- Document your navigation path

***

## TOOLS TO VERIFY

**CRITICAL WARNING**: You MUST investigate **ALL SIX tools** before providing your answer. If any tool is missing from your investigation_log, your answer will be **rejected**.

| # | Tool | Historian's Claimed Date | Claimed Position |
|---|------|--------------------------|------------------|
| 1 | React | May 2013 | 1st |
| 2 | Gulp | July 2013 | 2nd |
| 3 | Browserify | March 2014 | 3rd |
| 4 | Webpack | October 2015 | 4th |
| 5 | Vue.js | February 2014 | 5th |
| 6 | Svelte | November 2016 | 6th |

For each tool, find:
- The **Initial release** date from its Wikipedia infobox
- Whether the claimed date is accurate (within 3 months)
- Evidence from **at least TWO different Wikipedia pages**

**Page Requirement**: You must visit at least **6 different Wikipedia pages** during your investigation (one for each tool). Record each page visit in your navigation log.

***

## REQUIRED Output Format

**PHASE 1**: Investigation Log

```markdown
<investigation_log>
| Tool Name | Wikipedia URL | Initial Release Date | Historian's Claim | Date Accurate? |
|-----------|---------------|---------------------|-------------------|----------------|
| React | [URL] | [YYYY-MM-DD] | May 2013 | [YES/NO] |
| Gulp | [URL] | [YYYY-MM-DD] | July 2013 | [YES/NO] |
| Browserify | [URL] | [YYYY-MM-DD] | March 2014 | [YES/NO] |
| Webpack | [URL] | [YYYY-MM-DD] | October 2015 | [YES/NO] |
| Vue.js | [URL] | [YYYY-MM-DD] | February 2014 | [YES/NO] |
| Svelte | [URL] | [YYYY-MM-DD] | November 2016 | [YES/NO] |
</investigation_log>
```

**PHASE 2**: Date Verification

```markdown
<date_verification>
| Tool | Actual Release | Claimed Date | Date Accurate? |
|------|---------------|--------------|----------------|
| React | [YYYY-MM] | May 2013 | [YES/NO] |
| Gulp | [YYYY-MM] | July 2013 | [YES/NO] |
| Browserify | [YYYY-MM] | March 2014 | [YES/NO] |
| Webpack | [YYYY-MM] | October 2015 | [YES/NO] |
| Vue.js | [YYYY-MM] | February 2014 | [YES/NO] |
| Svelte | [YYYY-MM] | November 2016 | [YES/NO] |
</date_verification>
```

**PHASE 3**: Order Verification

```markdown
<order_verification>
Historian's claimed order: React → Gulp → Browserify → Webpack → Vue.js → Svelte

Actual chronological order (by release date):
1. [Tool name] - [YYYY-MM]
2. [Tool name] - [YYYY-MM]
3. [Tool name] - [YYYY-MM]
4. [Tool name] - [YYYY-MM]
5. [Tool name] - [YYYY-MM]
6. [Tool name] - [YYYY-MM]

Order correct? [YES/NO]
</order_verification>
```

**PHASE 4**: Cross-Verification (6 evidences - ONE for EACH tool)

```markdown
<cross_verification>
<evidence_1>
<tool>React</tool>
<sentence>[Direct quote from a Wikipedia page confirming React's date]</sentence>
<source>[Full Wikipedia URL - can be the tool's own page or another page]</source>
</evidence_1>
<evidence_2>
<tool>Gulp</tool>
<sentence>[Direct quote confirming Gulp's date]</sentence>
<source>[Full Wikipedia URL]</source>
</evidence_2>
<evidence_3>
<tool>Browserify</tool>
<sentence>[Direct quote confirming Browserify's date]</sentence>
<source>[Full Wikipedia URL]</source>
</evidence_3>
<evidence_4>
<tool>Webpack</tool>
<sentence>[Direct quote confirming Webpack's date]</sentence>
<source>[Full Wikipedia URL]</source>
</evidence_4>
<evidence_5>
<tool>Vue.js</tool>
<sentence>[Direct quote confirming Vue.js's date]</sentence>
<source>[Full Wikipedia URL]</source>
</evidence_5>
<evidence_6>
<tool>Svelte</tool>
<sentence>[Direct quote confirming Svelte's date]</sentence>
<source>[Full Wikipedia URL]</source>
</evidence_6>
</cross_verification>
```

**PHASE 5**: Final Answer

```markdown
<answer>
<navigation_summary>
Total pages visited: [N] (minimum 6)
Total back navigations: [N]
Tools found via direct link: [N]
Tools found via indirect navigation: [N]
</navigation_summary>

<accuracy_summary>
Date claims accurate: [X]/6
Order claim accurate: [YES/NO]
Overall timeline accurate: [YES/NO]
</accuracy_summary>

<analysis>
[Explain your findings: Which date claims were accurate/inaccurate and why. Is the chronological order correct? If not, what is the correct order? Describe your navigation strategy. Minimum 200 characters.]
</analysis>

<final_verdict>
[Provide one verdict: "FULLY ACCURATE" (all dates and order correct), "DATES ACCURATE, ORDER WRONG" (dates correct but wrong order), "PARTIALLY ACCURATE" (some dates wrong), or "MOSTLY INACCURATE" (multiple errors)]
</final_verdict>
</answer>
```

***

## CRITICAL WARNINGS

1. **ALL SIX TOOLS REQUIRED**: You MUST investigate ALL SIX tools. Missing any tool will result in failure.

2. **6+ PAGES REQUIRED**: You must visit at least 6 different Wikipedia pages (one per tool). Document each visit.

3. **Link-chain navigation ONLY**: Do NOT use Wikipedia search. Do NOT type URLs directly. Navigate only by clicking links on pages.

4. **Date tolerance**: "May 2013" means any date from February 2013 to August 2013 would be ACCURATE.

5. **Order matters**: Even if individual dates are accurate, the claimed ORDER may be wrong.

6. **Cross-verification required**: You must provide evidence for **ALL SIX tools** (6 evidences total).

***

## Success Criteria

Your answer will be considered correct if and only if:
- All 6 tools are investigated via link navigation
- At least 6 different Wikipedia pages are visited
- Navigation is documented (either log or summary)
- Date accuracy verdicts (YES/NO) are correct for all tools
- The actual chronological order is correctly determined
- Cross-verification evidence is provided for all 6 tools
- The final verdict correctly reflects the timeline's accuracy
