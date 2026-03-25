# Triangulation Verifier: v1

## Task
Verify the following historical claim from THREE independent angles:

**CLAIM**: "The Great Wall of China was built by Qin Shi Huang to defend against the Mongols."

**REQUIREMENT**: Visit at least 10 different Wikipedia pages to gather evidence.

---

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

---

## Three Verification Angles

You must investigate this claim from three INDEPENDENT angles:

### ANGLE 1: Construction History
- Who actually built the Great Wall?
- Was Qin Shi Huang the only builder?
- What did he actually do?

**Starting pages**: Great Wall of China, Qin Shi Huang, History of the Great Wall

### ANGLE 2: Timeline Analysis
- When was the Great Wall built?
- What were the different construction periods?
- When did Qin Shi Huang live?

**Starting pages**: Qin Dynasty, Timeline of Chinese history

### ANGLE 3: Purpose Analysis
- Who were the enemies of Qin Dynasty?
- When did the Mongols emerge as a unified group?
- Was "Mongols" the correct term for Qin's enemies?

**Starting pages**: Xiongnu, Mongols, History of Mongolia

---

## CRITICAL WARNING

**COMMON MISCONCEPTIONS**:

| Misconception | Why It's Wrong |
|---------------|----------------|
| "Qin Shi Huang built the Great Wall" | He CONNECTED existing walls, not built from scratch |
| "It was to defend against Mongols" | Qin's enemies were XIONGNU, not Mongols |
| "The Wall is a single structure" | Built by MANY dynasties over centuries |
| "Current Wall is Qin's Wall" | Most existing sections are from MING Dynasty |

---

## Final Output Format

After visiting 10+ Wikipedia pages, output:

<verification>
=== ANGLE 1: Construction History ===
Verdict: [FULLY TRUE / PARTIALLY TRUE / FALSE]
Evidence 1: [Quote] - [URL]
Evidence 2: [Quote] - [URL]
Analysis: [1-2 sentences]

=== ANGLE 2: Timeline Analysis ===
Verdict: [FULLY TRUE / PARTIALLY TRUE / FALSE]
Evidence 1: [Quote] - [URL]
Evidence 2: [Quote] - [URL]
Analysis: [1-2 sentences]

=== ANGLE 3: Purpose Analysis ===
Verdict: [FULLY TRUE / PARTIALLY TRUE / FALSE]
Evidence 1: [Quote] - [URL]
Evidence 2: [Quote] - [URL]
Analysis: [1-2 sentences]
</verification>

<conclusion>
OVERALL VERDICT: [FULLY ACCURATE / PARTIALLY ACCURATE / MOSTLY INACCURATE / COMPLETELY INACCURATE]

Summary: [3-4 sentences explaining why the claim is accurate or not, citing evidence from all three angles]
</conclusion>

---

## Verification Checklist

Before submitting, ensure:
- [ ] Visited 10+ unique Wikipedia pages
- [ ] Investigated all THREE angles
- [ ] Provided 2+ evidence for each angle
- [ ] Included URLs for all evidence
- [ ] Provided overall verdict with reasoning
