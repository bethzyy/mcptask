# Chinese Philosophy Concept Detective: v6

## Task
Starting from https://en.wikipedia.org/wiki/Chinese_philosophy, find the philosophical concept that satisfies ALL of the following conditions by navigating Wikipedia.

---

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## The Challenge

Find a concept from Chinese philosophy that meets ALL 6 of these criteria:

| # | Criterion | Description |
|---|-----------|-------------|
| 1 | **Time period** | First appeared during the Warring States period (475-221 BCE) |
| 2 | **School** | Associated with Daoism (Taoism), NOT Confucianism |
| 3 | **Textual evidence** | Mentioned in BOTH the Zhuangzi AND the Tao Te Ching |
| 4 | **NOT about action** | NOT primarily about how to act or behave |
| 5 | **Metaphysical** | Related to the fundamental nature of reality |
| 6 | **Unique to Daoism** | Not shared with other philosophical traditions |

---

## Navigation Requirements

1. Start from the Chinese Philosophy page
2. Navigate to the Taoism/Daoism page
3. Identify at least 8 potential candidate concepts
4. For each candidate, check the Zhuangzi page and Tao Te Ching page
5. Verify each candidate against ALL 6 criteria

**Output your progress at each step:**
```
<step1>
Candidates identified: [list of concepts]
</step1>

<step2>
For [concept name]:
- Zhuangzi: found/not found
- Tao Te Ching: found/not found
- Criteria check: [list which criteria pass/fail]
</step2>
```

---

## Important Considerations

Many Daoist concepts share similar characteristics. Some common ones to investigate:

- **Wu Wei** (non-action, effortless action)
- **De** (virtue, power)
- **Qi** (vital energy)
- **Tian** (heaven)
- **Dao** (the way)
- **Yin-Yang** (complementary opposites)
- **Wu Xing** (five elements)
- **P'u** (uncarved block, simplicity)

Each of these may satisfy SOME criteria but not ALL six. Only ONE concept satisfies every criterion.

You must verify each candidate against ALL 6 criteria carefully. Pay special attention to:
- Whether the concept appears in BOTH primary texts (not just one)
- Whether the concept is unique to Daoism or shared with Confucianism
- Whether the concept is about action/behavior vs. the nature of reality

---

## CRITICAL: Final Output Format

After your investigation, output your answer in this exact format:

```
<answer>
[Concept name in Pinyin]
</answer>
```

**WARNING**: If you do not use the `<answer>` tags, your answer will be REJECTED.
