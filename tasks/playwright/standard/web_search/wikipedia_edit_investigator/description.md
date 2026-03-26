# Wikipedia Edit History Investigation (v86)

## Task
You are a **Wikipedia Content Verification Analyst**. Your mission is to investigate the sources of THREE specific pieces of information on Wikipedia and assess their credibility by tracing edit history.

***

## CRITICAL: This Task Requires Wikipedia History Features

You MUST use Wikipedia's built-in history and comparison tools. Direct searches will NOT give you the answer.

### Required Actions
1. **Navigate** to the target Wikipedia page
2. **Use "View history" tab** to access edit history
3. **Use WikiBlame** or "Find addition/removal" tool to find ORIGINAL authors
4. **Investigate THREE editors** by visiting their user pages
5. **Verify each editor's reliability** (check for blocks, warnings, topic expertise)
6. **Confirm editors are DIFFERENT people** (critical!)
7. **Compare credibility** between the three editors
8. **Cross-reference** information from multiple sources

### IMPORTANT: If WikiBlame is Slow or Fails
**You MUST continue the investigation using alternative methods:**
- Browse the edit history manually using the "View history" tab
- Look for edits with summaries mentioning the target content
- Use version comparison (diff) to find when content was first added
- Check older revisions by navigating to earlier history pages
- **Do NOT give up** - you must find the original authors for ALL THREE content pieces

***

## FOUR TRAPS TO AVOID

### Trap 1: The "Recent Editor" Trap
**The Mistake**: Assuming the most recent editor who touched the content is the original author.

**Why It's Wrong**: Many editors make minor corrections (spelling, formatting) to existing content. The person who last edited a section may not be the one who originally wrote it.

**How to Avoid**: Use WikiBlame or the "Find addition/removal" tool to find the FIRST person who added the content, not the last person who touched it.

### Trap 2: The "High-Frequency Editor" Trap
**The Mistake**: Assuming the editor with the most edits on the page is the most reliable.

**Why It's Wrong**: Some users make many small, low-quality edits (fixing typos, adding categories). High edit count does NOT equal expertise in the subject matter.

**How to Avoid**: Visit the editor's user page and check their topic expertise, not just edit count. Look at the quality and depth of their contributions.

### Trap 3: The "Same Person" Trap
**The Mistake**: Assuming multiple content pieces were added by the same person.

**Why It's Wrong**: Different content sections are often written by different editors over many years. You must verify independently for EACH content piece.

**How to Avoid**: Investigate all content pieces separately using WikiBlame. Compare the usernames EXACTLY - different names mean different editors.

### Trap 4: The "Unreliable Editor" Trap
**The Mistake**: Assuming all editors who added content are equally reliable sources.

**Why It's Wrong**: Some editors may have been blocked, have warning templates on their user pages, or have a history of problematic edits. An editor who was later blocked is NOT a reliable source.

**How to Avoid**: Visit each editor's user page AND talk page. Check for:
- Block notices or ban templates
- Warning templates about problematic behavior
- Topic expertise in tea-related subjects
- Whether they are currently active or inactive

***

## MISSION BRIEFING

### Target Page
**https://en.wikipedia.org/wiki/Tea_processing**

### Target Information #1: Oxidation Process
Find the paragraph that describes **tea oxidation (fermentation)** and the chemical changes. Look for:
- Enzymatic oxidation
- Theaflavins and thearubigins
- Chlorophyll breakdown
- Tannins release

Your task: **Find out WHO ORIGINALLY ADDED this detailed oxidation chemistry content and WHEN.** You must find the ORIGINAL author, not just any editor who modified it.

### Target Information #2: Tea Roller Machines
Find the section that describes **tea roller machines** (mechanical rolling equipment). Look for:
- Traditional rolling tables
- Modern rotorvane machines
- Orthodox rolling process
- Machine descriptions

Your task: **Find out WHO ORIGINALLY ADDED this tea roller machine content and WHEN.** This is a SEPARATE investigation from the oxidation content.

### Target Information #3: Drying/Firing Methods
Find the section that describes **tea drying or firing methods**. Look for:
- Traditional drying methods
- Hot air dryers or firing equipment
- Moisture reduction techniques
- Temperature control

Your task: **Find out WHO ORIGINALLY ADDED this drying/firing content and WHEN.** This is another SEPARATE investigation.

**IMPORTANT**: These three content pieces were added by DIFFERENT editors at DIFFERENT times. You must verify this!

***

## STEP-BY-STEP INSTRUCTIONS

### Phase 1: Locate Target Information #1 - Oxidation (4-6 actions)
1. Navigate to https://en.wikipedia.org/wiki/Tea_processing
2. Read the page content using `browser_read`
3. Scroll or navigate to find the **Oxidation** section
4. Locate the paragraph describing the chemical oxidation process
5. **Record the exact text** - you'll need to find who originally added it
6. Use `browser_snapshot` to capture the page structure

### Phase 2: Find ORIGINAL Author of Oxidation Content (8-10 actions)
1. Click the **"View history"** tab (top of the page)
2. Look for **"Find addition/removal"** link or use WikiBlame externally
3. Enter keywords like "enzymatic" or "theaflavins" to search
4. **CRITICAL**: Look for the FIRST occurrence of this content, not recent edits
5. Use version comparison to see exactly what was added
6. If needed, browse through older history pages
7. **Select two versions** using checkboxes for comparison
8. Click **"Compare selected versions"** to see the diff
9. Identify the ORIGINAL editor who FIRST added the oxidation content
10. **Record the editor's username and the ORIGINAL timestamp**

### Phase 3: Investigate Oxidation Editor - Reliability Check (5-7 actions)
1. **Click on the editor's username** to visit their user page
2. Check their **registration date**
3. Check their **total edit count**
4. **NEW: Check their user talk page** for any warnings or block notices
5. Browse their **recent contributions** - look for topic patterns
6. Note their **topic expertise** - do they edit tea-related content?
7. **Record reliability status**: Are they blocked? Any warnings?

### Phase 4: Output Checkpoint #1
Before proceeding, output your findings so far:
```
<checkpoint_1>
<current_findings>
- Oxidation content found: [brief description]
- Original editor identified: [username]
- Edit date: [timestamp]
- Editor reliability: [reliable/unreliable with reason]
</current_findings>
<next_steps>
Will now investigate tea roller machine content
</next_steps>
</checkpoint_1>
```

### Phase 5: Locate Target Information #2 - Roller Machines (3-4 actions)
1. Navigate back to the Tea_processing page
2. Find the section about **Rolling** or **Tea roller machines**
3. Locate the content about mechanical rolling equipment
4. **Record the exact text**

### Phase 6: Find ORIGINAL Author of Roller Machine Content (8-10 actions)
1. Access the **"View history"** tab again
2. Use **"Find addition/removal"** or WikiBlame
3. Search for keywords like "roller" or "rotorvane" or "rolling table"
4. **CRITICAL**: This is a SEPARATE investigation - the editor is DIFFERENT
5. Browse through different time periods (this content is newer than oxidation)
6. **Compare multiple version pairs**
7. Find who FIRST added the roller machine details
8. **Record the editor's username and the ORIGINAL timestamp**

### Phase 7: Investigate Roller Machine Editor - Reliability Check (5-7 actions)
1. **Click on the editor's username**
2. Check their **registration date**
3. Check their **total edit count**
4. **Check their user talk page** for warnings or blocks
5. Browse their **contributions** - look for patterns
6. Note their **topic expertise**
7. **Record reliability status**

### Phase 8: Output Checkpoint #2
Output your findings for the second investigation:
```
<checkpoint_2>
<current_findings>
- Roller machine content found: [brief description]
- Original editor identified: [username]
- Edit date: [timestamp]
- Editor reliability: [reliable/unreliable with reason]
- Confirmed DIFFERENT from oxidation editor: [YES/NO]
</current_findings>
<next_steps>
Will now investigate drying/firing methods content
</next_steps>
</checkpoint_2>
```

### Phase 9: Locate Target Information #3 - Drying/Firing (3-4 actions)
1. Navigate back to the Tea_processing page
2. Find the section about **Drying**, **Firing**, or **Final processing**
3. Locate the content about drying methods and equipment
4. **Record the exact text**

### Phase 10: Find ORIGINAL Author of Drying Content (8-10 actions)
1. Access the **"View history"** tab again
2. Use **"Find addition/removal"** or WikiBlame
3. Search for keywords like "drying", "firing", "hot air", or "moisture"
4. **CRITICAL**: This is another SEPARATE investigation
5. Browse through different time periods
6. **Compare multiple version pairs**
7. Find who FIRST added the drying/firing content
8. **Record the editor's username and the ORIGINAL timestamp**

### Phase 11: Investigate Drying Editor - Reliability Check (5-7 actions)
1. **Click on the editor's username**
2. Check their **registration date**
3. Check their **total edit count**
4. **Check their user talk page** for warnings or blocks
5. Browse their **contributions** - look for patterns
6. Note their **topic expertise**
7. **Record reliability status**

### Phase 12: Output Checkpoint #3
Output your findings for the third investigation:
```
<checkpoint_3>
<current_findings>
- Drying/firing content found: [brief description]
- Original editor identified: [username]
- Edit date: [timestamp]
- Editor reliability: [reliable/unreliable with reason]
- Confirmed DIFFERENT from previous editors: [YES/NO]
</current_findings>
<next_steps>
Will now compare all three editors and produce final report
</next_steps>
</checkpoint_3>
```

### Phase 13: Verify Three Different Editors (2-3 actions)
1. **Compare all three usernames EXACTLY** - case-sensitive comparison
2. They should be DIFFERENT usernames (this is a key requirement)
3. If usernames appear similar, verify by checking user page details

### Phase 14: Compare and Report (3-4 actions)
1. Compare the credibility of all three editors
2. Identify which editor is most reliable (considering reliability checks)
3. Identify any editors who should be considered unreliable
4. Output your complete investigation report

***

## REQUIRED Output Format

```markdown
<investigation_report>

<checkpoint_1>
<current_findings>
[Your findings about oxidation content investigation]
</current_findings>
<next_steps>
[Your planned next steps]
</next_steps>
</checkpoint_1>

<checkpoint_2>
<current_findings>
[Your findings about roller machine investigation]
</current_findings>
<next_steps>
[Your planned next steps]
</next_steps>
</checkpoint_2>

<checkpoint_3>
<current_findings>
[Your findings about drying/firing investigation]
</current_findings>
<next_steps>
[Your planned next steps]
</next_steps>
</checkpoint_3>

<content_1_investigation>
<target_text>
[Copy the exact oxidation text you investigated - at least 50 characters]
</target_text>
<editor_username>
[Username of ORIGINAL editor who FIRST added oxidation content]
</editor_username>
<edit_timestamp>
[Date and time of ORIGINAL addition - format: YYYY-MM-DD HH:MM]
</edit_timestamp>
<editor_stats>
<total_edits>[Number]</total_edits>
<registration_date>[Date]</registration_date>
<specialty_areas>[Topics they frequently edit]</specialty_areas>
</editor_stats>
<reliability_check>
<is_blocked>[YES/NO]</is_blocked>
<has_warnings>[YES/NO]</has_warnings>
<reliability_status>[RELIABLE/UNRELIABLE with reason]</reliability_status>
</reliability_check>
</content_1_investigation>

<content_2_investigation>
<target_text>
[Copy the exact roller machine text you investigated - at least 50 characters]
</target_text>
<editor_username>
[Username of ORIGINAL editor who FIRST added roller machine content]
</editor_username>
<edit_timestamp>
[Date and time of ORIGINAL addition - format: YYYY-MM-DD HH:MM]
</edit_timestamp>
<editor_stats>
<total_edits>[Number]</total_edits>
<registration_date>[Date]</registration_date>
<specialty_areas>[Topics they frequently edit]</specialty_areas>
</editor_stats>
<reliability_check>
<is_blocked>[YES/NO]</is_blocked>
<has_warnings>[YES/NO]</has_warnings>
<reliability_status>[RELIABLE/UNRELIABLE with reason]</reliability_status>
</reliability_check>
</content_2_investigation>

<content_3_investigation>
<target_text>
[Copy the exact drying/firing text you investigated - at least 50 characters]
</target_text>
<editor_username>
[Username of ORIGINAL editor who FIRST added drying/firing content]
</editor_username>
<edit_timestamp>
[Date and time of ORIGINAL addition - format: YYYY-MM-DD HH:MM]
</edit_timestamp>
<editor_stats>
<total_edits>[Number]</total_edits>
<registration_date>[Date]</registration_date>
<specialty_areas>[Topics they frequently edit]</specialty_areas>
</editor_stats>
<reliability_check>
<is_blocked>[YES/NO]</is_blocked>
<has_warnings>[YES/NO]</has_warnings>
<reliability_status>[RELIABLE/UNRELIABLE with reason]</reliability_status>
</reliability_check>
</content_3_investigation>

<editor_comparison>
<all_different>[YES - all three editors MUST be different people]</all_different>
<verification_method>
[Explain how you verified they are different people - compare usernames, user pages, registration dates]
</verification_method>
</editor_comparison>

<credibility_comparison>
<editor_1_name>[Name of oxidation editor]</editor_1_name>
<editor_2_name>[Name of roller machine editor]</editor_2_name>
<editor_3_name>[Name of drying editor]</editor_3_name>
<most_reliable>[Name of most reliable editor]</most_reliable>
<least_reliable>[Name of least reliable editor, if any]</least_reliable>
<reasoning>
[Explain why one editor is more credible than the others in 4-5 sentences. Consider: edit count, account age, topic expertise, edit patterns, reliability check results, and any warning signs.]
</reasoning>
</credibility_comparison>

<trap_analysis>
<trap_1_avoided>
[Explain how you avoided the "Recent Editor" trap - how did you find the ORIGINAL author?]
</trap_1_avoided>
<trap_2_avoided>
[Explain how you avoided the "High-Frequency Editor" trap - how did you assess true expertise?]
</trap_2_avoided>
<trap_3_avoided>
[Explain how you avoided the "Same Person" trap - how did you verify editors are different?]
</trap_3_avoided>
<trap_4_avoided>
[Explain how you avoided the "Unreliable Editor" trap - how did you check for blocks/warnings?]
</trap_4_avoided>
</trap_analysis>

<navigation_evidence>
[List at least 15 distinct pages you visited or actions you took]
1. [Action 1]
2. [Action 2]
3. [Action 3]
4. [Action 4]
5. [Action 5]
6. [Action 6]
7. [Action 7]
8. [Action 8]
9. [Action 9]
10. [Action 10]
11. [Action 11]
12. [Action 12]
13. [Action 13]
14. [Action 14]
15. [Action 15]
</navigation_evidence>

<investigation_summary>
[Write a 2-3 sentence summary of your overall findings about the reliability of the Tea_processing page content, considering all three editors and their reliability.]
</investigation_summary>

</investigation_report>
```

***

## Success Criteria

Your answer will be verified against these requirements:

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Accessed "View history" tab | Required |
| 2 | Used WikiBlame or "Find addition/removal" tool | Required |
| 3 | Performed version comparison (diff) | Required |
| 4 | Visited ALL THREE editors' user pages | Required |
| 5 | Found ORIGINAL author of oxidation content | Required |
| 6 | Found ORIGINAL author of roller machine content | Required |
| 7 | Found ORIGINAL author of drying/firing content | Required |
| 8 | Verified all THREE editors are DIFFERENT people | Required |
| 9 | Provided ORIGINAL timestamps for all THREE edits | Required |
| 10 | Credibility comparison with reasoning | Required |
| 11 | Trap analysis explaining how ALL FOUR traps were avoided | Required |
| 12 | Checkpoints #1, #2, #3 output at appropriate stages | Required |
| 13 | Reliability check for each editor (blocks/warnings) | Required |
| 14 | Navigation evidence (15+ actions) | Required |
| 15 | Investigation summary included | Required |
| 16 | Completed in at least 20 turns | Required |

***

## CRITICAL WARNINGS

### Do NOT Do These
- **Do NOT use browser_search** to find editor names directly
- **Do NOT guess** editors based on recent edits - find the ORIGINAL author
- **Do NOT skip** the version comparison step
- **Do NOT fabricate** editor statistics
- **Do NOT investigate only ONE or TWO content pieces** - all THREE are required
- **Do NOT assume** content has the same author - they are DIFFERENT people
- **Do NOT report** recent editors as original authors
- **Do NOT report same editor for multiple** - they are DIFFERENT people
- **Do NOT skip** the reliability check (blocks/warnings) for each editor
- **Do NOT skip** the checkpoint outputs

### Common Pitfalls
1. **Wrong editor**: Most recent editor is NOT the original author - use WikiBlame!
2. **Wrong timestamp**: Record when content was ORIGINALLY ADDED, not last modified
3. **Incomplete investigation**: Must investigate ALL THREE content pieces SEPARATELY
4. **Same person assumption**: The three editors ARE different - verify this!
5. **Shallow analysis**: Must compare credibility based on expertise, not just edit count
6. **Missing trap analysis**: Must explain how you avoided ALL FOUR traps
7. **Missing checkpoints**: Must output checkpoints at phases 4, 8, and 12
8. **Missing reliability check**: Must check each editor for blocks and warnings

***

## Tools Available
The Playwright MCP server provides these tools:
- `browser_navigate` - Go to URLs
- `browser_click` - Click on elements (links, tabs, buttons)
- `browser_read` - Read page content
- `browser_snapshot` - See page structure
- `browser_scroll` - Scroll the page
- `browser_hover` - Hover over elements
- `browser_select_option` - Select from dropdown menus
- `browser_type` - Type text into input fields
- `browser_wait_for` - Wait for content to load
- `browser_tabs` - Manage browser tabs

***

## Tips for Success

1. **Use WikiBlame**: The "Find addition/removal" tool is essential for finding ORIGINAL authors
2. **Be thorough**: This task requires investigating THREE different content pieces
3. **Be patient**: Finding original editors requires comparing many versions
4. **Take notes**: Record findings for all editors as you go
5. **Verify separately**: Each content piece needs its own investigation
6. **Compare fairly**: Consider topic expertise and reliability, not just edit count
7. **Explain your process**: The trap_analysis section is required for ALL FOUR traps
8. **Complete all 14 phases**: Skipping phases will lead to incomplete answers
9. **Output checkpoints**: Don't forget to output findings at phases 4, 8, and 12
10. **Check reliability**: Visit user talk pages to check for blocks and warnings
11. **Verify different editors**: The three content pieces were added by DIFFERENT people!
