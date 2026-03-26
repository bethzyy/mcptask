# Chinese Festival Navigator: v127 - Wikipedia Link-Chain Exploration

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## Task

Identify the Chinese traditional festival that meets ALL 6 criteria for a research project.

**Starting Point**: https://en.wikipedia.org/wiki/List_of_festivals_in_China

**EXPLORATION REQUIREMENT**: You are strongly encouraged to visit **15+ different Wikipedia pages** by following links from one page to another. This is a link-chain exploration task - each new page should be reached by clicking links from your current page, not by direct URL navigation.

---

## Navigation Rules (CRITICAL)

1. **Start**: Navigate to the List of Festivals page
2. **Explore**: Click on festival links to visit individual festival pages
3. **Deep Dive**: From each festival page, click on related links (foods, poets, history, regions)
4. **Chain**: Build a chain of page visits by following links, not by typing URLs
5. **Record**: Keep track of every unique page you visit

**Recommended**: 15+ unique Wikipedia pages before providing your final answer.

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

## CRITICAL TRAPS (DO NOT SELECT)

| Festival | Why Wrong |
|----------|-----------|
| Dragon Boat Festival | Qu Yuan **SUICIDE** by drowning |
| Cold Food Festival | Jie Zitui **NOT A POET**, died in fire, no demotion |
| Qingming Festival | Qingtuan is **SWEET** |
| Lantern Festival | Yuanxiao is **SWEET** |
| Mid-Autumn Festival | Mooncake is **SWEET** |

---

## BEFORE You Output (MANDATORY)

  Before writing `<answer>`, you MUST verify:
  1. Your selected festival is NOT in the 'CRITICAL TRAPS' list
  2. If it IS a trap → STOP, go back to the Starting Point page and start over
  3. Do NOT output `<answer>` until you find a festival that is NOT a trap

  ⚠️ WARNING: If you output a trap festival, you will FAIL immediately.

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

Trap Avoidance: [explain why you avoided each trap]
</reasoning>
```

---

## Verification

Your answer will be checked for:
1. **Correct festival** - The festival name in your `<answer>` tag must be correct
2. **Traps avoided** - Your answer must NOT be Dragon Boat, Cold Food, Qingming, Lantern, or Mid-Autumn Festival.
3. **Output format** - Your response should include `<answer>`, `<page_chain>` and `<reasoning>` sections

---

## Important Notes

- **Link-chain navigation**: Follow links from page to page, do not type URLs directly
- **Thorough exploration**: Visit multiple pages before concluding (15+ recommended)
- **Evidence required**: Quote actual Wikipedia content for each criterion
- **Poet demotion vs suicide**: Demotion means forced out of office, NOT suicide
- **Sweet vs not sweet**: Sweet foods include sugar, honey, sweet bean paste
- **Less famous festivals**: The correct answer may not be the most famous festival
