# Chinese Tea Detective: v22

## Task
Starting from https://en.wikipedia.org/wiki/Oolong, find the Anxi oolong tea with **OSmanthus (Osmanthus fragrans)** fragrance by navigating Wikipedia.

**REQUIREMENT**: Visit at least 20 different Wikipedia pages

---

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## 5 Criteria

| # | Criterion | Requirement |
|---|-----------|-------------|
| 1 | Origin | Anxi County, Fujian |
| 2 | Category | Oolong (semi-oxidized) |
| 3 | **Fragrance** | **OSMANTHUS (Osmanthus fragrans flower)** |
| 4 | Leaf style | Rolled semi-ball |
| 5 | Name meaning | Contains "golden" or "osmanthus" |

---

## CRITICAL WARNING

**Tie Guan Yin (Iron Goddess of Mercy) has ORCHID fragrance, NOT osmanthus.**

Most famous Anxi oolong = Tie Guan Yin = **ORCHID fragrance** = **TRAP**

You need a LESS famous Anxi oolong with OSMANTHus fragrance.

---

## CRITICAL: Final Output Format

After visiting 20+ Wikipedia pages, you MUST output your answer in this exact format:

```
<answer>
[Tea name]
</answer>
```

**WARNING**: If you do not use the `<answer>` tags, your answer will be REjected.

Do NOT output:
- Explanations
- Markdown tables
- Any extra text outside the `<answer>` tag
- Any text that could "helpful" or not strictly needed

