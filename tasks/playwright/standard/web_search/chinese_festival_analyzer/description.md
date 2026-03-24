# Chinese Festival Navigator: v127 - Wikipedia Link-Chain Exploration

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## Task

Identify the Chinese traditional festival that meets ALL 6 criteria for a research project.

**Starting Point**: https://en.wikipedia.org/wiki/List_of_festivals_in_China

**EXPLORATION REQUIREMENT**: You must visit at least **15 different Wikipedia pages** by following links from one page to another. This is a link-chain exploration task - each new page should be reached by clicking links from your current page, not by direct URL navigation.

---

## Navigation Rules (CRITICAL)

1. **Start**: Navigate to the List of Festivals page
2. **Explore**: Click on festival links to visit individual festival pages
3. **Deep Dive**: From each festival page, click on related links (foods, poets, history, regions)
4. **Chain**: Build a chain of page visits by following links, not by typing URLs
5. **Record**: Keep track of every unique page you visit

**Minimum**: 15 unique Wikipedia pages before providing your final answer.

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

## Final Answer Format

After visiting 15+ Wikipedia pages, provide your answer:

```
<answer>
[Festival name from Wikipedia]
</answer>

<page_chain>
List all 15+ Wikipedia pages you visited in order:
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
1. **Correct festival** meeting all 6 conditions
2. **Traps avoided** (Dragon Boat, Cold Food, Qingming, Lantern, Mid-Autumn)
3. **Page chain** with 15+ unique Wikipedia pages

---

## Important Notes

- **Link-chain navigation**: Follow links from page to page, do not type URLs directly
- **Thorough exploration**: Visit at least 15 pages before concluding
- **Evidence required**: Quote actual Wikipedia content for each criterion
- **Poet demotion vs suicide**: Demotion means forced out of office, NOT suicide
- **Sweet vs not sweet**: Sweet foods include sugar, honey, sweet bean paste
- **Less famous festivals**: The correct answer may not be the most famous festival

---

## Hint

The correct festival has connections to:
- A famous Chinese poet who was **demoted** (forced out of office) but did NOT commit suicide
- Traditional food that is **green** but **not sweet**
- Origins **before the Tang Dynasty** (618 CE)

Consider exploring less well-known festivals on the List of Festivals page.
