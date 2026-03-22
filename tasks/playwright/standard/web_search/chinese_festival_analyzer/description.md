# Chinese Festival Navigator: v114 - Open Exploration

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## Task Overview

Starting from https://en.wikipedia.org/wiki/List_of_festivals_in_China, find a traditional Chinese festival meeting ALL 6 conditions:

| # | Condition | Requirement |
|---|-----------|-------------|
| 1 | Food Color | Green |
| 2 | Food Taste | NOT sweet (savory or bitter) |
| 3 | Symbolism | Health, purification, or warding off evil |
| 4 | Region | Jiangnan OR North China Plain |
| 5 | Era | Before Tang Dynasty (618 CE) |
| 6 | Poet Connection | POLITICAL DEMOTION (not suicide) |

---

## TRAPS (DO NOT SELECT)

| Festival | Why Wrong |
|----------|-----------|
| Dragon Boat Festival | Qu Yuan SUICIDE by drowning |
| Qingming Festival | Qingtuan is SWEET |
| Lantern Festival | Yuanxiao is SWEET |
| Mid-Autumn Festival | Mooncake is SWEET |

---

## CRITICAL: Step-by-Step Navigation with IMMEDIATE Output

**After EVERY browser action, you MUST output what you found before proceeding.**

You CANNOT execute multiple browser actions in one turn. Each turn must contain:
1. ONE browser action (navigate or click)
2. IMMEDIATE output of what you found on that page
3. Your next decision

---

## Navigation Requirements

1. **Start** at the List of Festivals in China page
2. **Explore** festival pages by clicking links
3. **Verify** each festival against ALL 6 conditions
4. **Continue** until you find one that meets ALL conditions
5. **Document** at least 20 turns

**Exploration Strategy:**
- Focus on spring festivals (they often involve green plants)
- Look for festivals with purification rituals
- Verify poet connections carefully - demotion ≠ suicide

---

## When to Output Your Answer

**DO NOT output `<answer>` until you find a festival that meets ALL 6 conditions.**

If your current best candidate fails ANY of the 6 conditions:
1. Do NOT output `<answer>`
2. Go back to search for more festivals
3. Continue exploring until you find one that meets ALL conditions

Remember: An answer that doesn't meet all 6 conditions will be marked as FAILED.
It is better to continue searching than to give an incorrect answer.

---

## Final Answer Format

**CRITICAL: Your answer MUST use the EXACT format below or verification will FAIL.**

```
<answer>
[Festival name from Wikipedia]
</answer>

<reasoning>
## Turn-by-Turn Navigation Log
Turn 1: [URL] - [Finding]
Turn 2: [URL] - [Finding]
Turn 3: [URL] - [Finding]
... (MUST have 20+ documented turns)

## Verification of 6 Conditions
1. Food Color: [Evidence that food is GREEN]
2. Food Taste: [Evidence that food is NOT SWEET]
3. Symbolism: [Evidence of health/purification/warding off evil]
4. Region: [Evidence of Jiangnan or North China Plain]
5. Era: [Evidence of pre-Tang Dynasty origin]
6. Demotion Event: [Evidence of POLITICAL DEMOTION, not suicide]

## Trap Avoidance
- Dragon Boat: [Why rejected - Qu Yuan SUICIDE by drowning]
- Qingming: [Why rejected - Qingtuan is SWEET]
- Lantern: [Why rejected - Yuanxiao is SWEET]
- Mid-Autumn: [Why rejected - Mooncake is SWEET]

## Final Determination
[Why this festival meets ALL 6 conditions]
</reasoning>
```

**NOTE:** ALL 6 conditions MUST be verified. Conditions 1-5 require 5/5 keyword verification. Condition 6 (Demotion) is validated separately.

---

## Verification

Your answer will be checked for:
1. **20+ turns** with step-by-step documentation
2. **Correct festival** meeting all 6 conditions
3. **Traps avoided** (Dragon Boat, Qingming, Lantern, Mid-Autumn)
4. **Valid demotion event** (not suicide)

**If you output fewer than 20 documented turns, you will FAIL.**
