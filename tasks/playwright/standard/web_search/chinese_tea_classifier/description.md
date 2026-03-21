# Chinese Tea Detective: v5 - Wikipedia Link Chain (15 Turns Required)

## Task Overview

Starting from https://en.wikipedia.org/wiki/Chinese_tea, navigate through Wikipedia's tea articles using ONLY page links to identify a mystery tea sample.

**A tea apprentice has brought you a sample with misleading characteristics.** You must trace the correct identification through systematic Wikipedia navigation.

---

## The Mystery Sample

**Apprentice's Field Notes** (may contain ERRORS):

1. **Leaf appearance**: Dark, twisted strips with reddish-brown color
2. **Liquor color**: Orange-amber to deep red
3. **Taste**: Rich, roasted character with mineral notes
4. **Origin claim**: "From Fujian Province, a famous RED tea"
5. **Name hint**: "The name contains a color reference"

**Apprentice's Conclusion**: "This is definitely a Fujian Black Tea (Hong Cha) because of the reddish color and name!"

**YOUR TASK**: Verify or refute this conclusion.

---

## Navigation Rules

### Rule 1: Start Point
Begin at: https://en.wikipedia.org/wiki/Chinese_tea

### Rule 2: Link-Only Navigation
Navigate by clicking links on Wikipedia pages ONLY.
- **FORBIDDEN**: Direct URL navigation (except start)
- **FORBIDDEN**: Wikipedia search
- **FORBIDDEN**: External websites

### Rule 3: Output Format
After each navigation, output:
```
=== TURN [N] ===
URL: [current page URL]
ACTION: Clicked on "[link text]"
FINDING: [What you learned]
DECISION: [How this helps]
```

---

## Required Navigation Phases

### Phase 1: Understand Oxidation (Turns 1-3)
Navigate from Chinese tea → Tea categories → Oxidation info
**Must understand**: What oxidation level defines Black Tea vs Oolong?

### Phase 2: Fujian Tea Investigation (Turns 4-7)
Navigate to Fujian tea pages
**Must find**: List of Fujian Black Teas AND Oolongs

### Phase 3: Compare Candidates (Turns 8-12)
Investigate at least 3 specific tea pages
**Must verify**: Oxidation level, category, origin for each

### Phase 4: Final Verification (Turns 13-15)
Confirm your answer with cross-referencing
**Must explain**: Why the apprentice was wrong

---

## TRAPS to Avoid

| Candidate | Why Wrong |
|-----------|-----------|
| **Lapsang Souchong** | IS Black Tea (100% oxidation) - correct category, but has SMOKEY flavor |
| **Dian Hong** | IS Black Tea, but from Yunnan (not Fujian) |
| **Any "Red" name = Black Tea** | FALSE! Da Hong Pao has "Red" but is Oolong |

---

## Final Answer Format

```
<answer>
Tea: [English Name] + [Chinese Name]
Category: [Correct category]
Oxidation: [Exact %]
</answer>

<reasoning>
## Navigation Log
Turn 1: [URL] - [Finding]
Turn 2: [URL] - [Finding]
... (list ALL turns, minimum 15)

## Key Evidence
[Why this tea is correct]

## Trap Explanation
[Why apprentice was wrong]
</reasoning>
```

---

## Verification

Your answer will be checked for:
1. **15+ documented turns**
2. **Correct tea**: Da Hong Pao (大红袍)
3. **Correct category**: Oolong (NOT Black Tea!)
4. **Trap explanation**: Why name "Red" ≠ Black Tea

**If you output fewer than 15 documented turns, you will FAIL.**
