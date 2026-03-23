# Chinese Festival Navigator: v139 - Wikipedia Link-Chain Exploration

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## Task

Identify the Chinese traditional festival that meets ALL 6 criteria for a research project.

**Starting Point**: https://en.wikipedia.org/wiki/List_of_festivals_in_China

**EXPLORATION REQUIREMENT**: You must explore Wikipedia by following links from one page to another. This is a link-chain exploration task - each new page should be reached by clicking links from your current page, not by direct URL navigation.

**⚠️ NO PRIOR KNOWLEDGE**: All information must come from Wikipedia pages you visit. You cannot rely on your existing knowledge about Chinese festivals. Every claim must be backed by a quote from a Wikipedia page.

---

## Task Phases (CRITICAL - Follow in Order)

### Phase 1: Exploration
1. Navigate to the List of Festivals page
2. Follow festival links to visit individual festival pages
3. From each festival page, follow related links (foods, poets, history, regions)
4. Build a chain of page visits by following links (do not type URLs directly)
5. **Record every unique page** (title + URL) - these will be output in `<page_chain>`

**Goal**: Visit 20+ unique Wikipedia pages to discover candidate festivals.
**Output**: All visited pages will be listed in `<page_chain>` tag (need ≥20 URLs to pass verification).

---

## 🚫 CRITICAL TRAPS (DO NOT SELECT)

| Festival | Why Wrong |
|----------|-----------|
| Dragon Boat Festival | Qu Yuan **SUICIDE** by drowning |
| Cold Food Festival | Jie Zitui **NOT A POET**, died in fire, no demotion |
| Qingming Festival | Qingtuan is **SWEET** |
| Lantern Festival | Yuanxiao is **SWEET** |
| Mid-Autumn Festival | Mooncake is **SWEET** |

---

### Phase 2: Verification
For each candidate festival you discover:
1. **🚫 CHECK TRAP TABLE ABOVE**: If the festival name matches ANY festival in the TRAP table → **STOP IMMEDIATELY** → this festival is **DISQUALIFIED** → return to Phase 1
2. Check against ALL 6 criteria (Food Color, Food Taste, Symbolism, Region, Era, Poet)
3. **Collect evidence** for each criterion (quote + source URL) - these will be output in `<reasoning>`
4. If ANY criterion fails → this festival is WRONG → return to Phase 1
5. Only proceed to Phase 3 when you find a festival that passes ALL 6 criteria

**Output**: Evidence for each criterion will be listed in `<reasoning>` tag (need ≥4/6 criteria to pass verification).

### Phase 3: Output
When you have found a festival that meets ALL 6 criteria:
1. Write the festival name in `<answer>` tag
2. List all visited pages in `<page_chain>` tag
3. Provide evidence for each criterion in `<reasoning>` tag

---

## Loop Mechanism

```
Phase 1 (Explore) → Phase 2 (Verify) → Phase 3 (Output)
       ↑                   │
       └───────────────────┘
         (if TRAP or criteria fail)
```

**Loop behavior when criteria fail or TRAP found:**
1. Return to Phase 1, Step 2 (select a NEW festival link from the list)
2. Do NOT repeat Phase 1, Step 1 (you are already on the List page)
3. Keep recording ALL pages in `<page_chain>` (including failed investigations)
4. Select a DIFFERENT festival (not the one you just rejected)

**You may loop between Phase 1 and Phase 2 multiple times** until you find the correct festival.

---

## 6 Criteria (ALL must be met)

| # | Criterion | Requirement |
|---|-----------|-------------|
| 1 | Food Color | GREEN (mugwort, herbs, green vegetables) |
| 2 | Food Taste | NOT sweet (savory or bitter, no sugar/honey/sweet fillings) |
| 3 | Symbolism | Health, purification, or warding off evil |
| 4 | Region | Jiangnan OR North China Plain |
| 5 | Era | Before Tang Dynasty (618 CE) |
| 6 | Poet Connection | POLITICAL DEMOTION (exiled, forced out of office) - NOT suicide, NOT death by fire |

---

## Final Answer Format

After thorough exploration, provide your answer:

```
<answer>
[Festival name from Wikipedia]
</answer>

<page_chain>
List all Wikipedia pages you visited in order:
1. [Page title] - [URL]
2. [Page title] - [URL]
...
</page_chain>

<reasoning>
For each of the 6 criteria, provide evidence from Wikipedia pages you visited:

1. Food Color (GREEN): [quote from page] - [page URL]
2. Food Taste (NOT SWEET): [quote from page] - [page URL]
3. Symbolism: [quote from page] - [page URL]
4. Region: [quote from page] - [page URL]
5. Era (Before 618 CE): [quote from page] - [page URL]
6. Poet Connection (DEMOTION, not suicide): [quote from page] - [page URL]
</reasoning>
```

---

## Verification

Your answer will be verified against the 6 criteria listed above. A correct answer must satisfy ALL criteria while avoiding the trap festivals.

Your output will be checked for:
1. **Valid festival** in `<answer>` tag (must meet ALL 6 criteria)
2. **`<page_chain>`** contains at least 4 Wikipedia URLs
3. **`<reasoning>`** contains evidence for at least 4 of 6 criteria

**Recommended**: Visit 20+ pages and provide evidence for each criterion to ensure accuracy.

---

## Trap Detection and Backtracking

If during **Phase 2: Verification** you discover that a festival is actually a TRAP:

1. **STOP** - Do not continue with that festival
2. **DOCUMENT** - Note why it's a trap (e.g., "Dragon Boat: Qu Yuan committed SUICIDE, not demotion")
3. **RETURN** - Go back to Phase 1 (List of Festivals page)
4. **RESTART** - Begin a new investigation with a different festival

This backtracking process should be visible in your `<page_chain>` and `<reasoning>` output.

---

## Important Notes

- **Link-chain navigation**: Follow links from page to page, do not type URLs directly
- **Thorough exploration**: Visit multiple pages to gather sufficient evidence
- **Evidence required**: Quote actual Wikipedia content for each criterion
- **Poet demotion vs suicide**: Demotion means forced out of office, NOT suicide
- **Sweet vs not sweet**: Sweet foods include sugar, honey, sweet bean paste
- **Less famous festivals**: The correct answer may not be the most famous festival

---

## Exploration Tips

- Start with the List of Festivals page and explore systematically
- For each festival, verify against ALL 6 criteria before selecting
- Use the trap table to eliminate wrong answers
- Less famous festivals may be the correct answer - explore thoroughly
