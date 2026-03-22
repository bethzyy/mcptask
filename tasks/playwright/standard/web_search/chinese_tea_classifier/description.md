# Chinese Tea Detective: v6 - Wikipedia Link Chain (20 Turns Required)

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

## Investigation Requirements

You must complete ALL of the following requirements through your Wikipedia navigation:

### Requirement 1: Oxidation Knowledge
**You must understand**: What oxidation levels define different tea categories?
- Black Tea (Hong Cha) has a specific oxidation range
- Oolong has a different oxidation range
- These ranges are key to correct classification

### Requirement 2: Regional Tea Knowledge
**You must investigate**: Fujian Province produces multiple tea categories
- Find examples of Fujian Black Teas
- Find examples of Fujian Oolongs
- Note the characteristics of each

### Requirement 3: Candidate Verification
**You must verify**: For any tea you identify, confirm through multiple sources:
- Its exact oxidation level
- Its correct category classification
- Its geographic origin

### Requirement 4: Error Analysis
**You must explain**: What specific classification error did the apprentice make?
- Identify the misleading factor in the sample description
- Explain why the apprentice's reasoning was incorrect

---

## Common Mistakes to Avoid

| Mistake | Why It's Wrong |
|---------|---------------|
| **Assuming smoky = wrong category** | Some Fujian teas have smoky notes but may still be in the correct category |
| **Ignoring geographic origin** | Not all reddish teas from China are from Fujian |
| **Equating color names with tea categories** | A tea with "Red" in its name is NOT necessarily a Black Tea (Hong Cha) - verify by oxidation level! |

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
... (list ALL turns, minimum 20)

## Key Evidence
[Why this tea is correct]

## Trap Explanation
[Why apprentice was wrong]
</reasoning>
```

---

## Verification

Your answer will be checked for:
1. **20+ documented turns** - You must show systematic exploration
2. **Tea identification** - A specific Fujian tea that matches ALL the sample characteristics
3. **Category verification** - The correct category based on oxidation level, not name
4. **Error explanation** - Clear analysis of why the apprentice's classification was wrong

**If you output fewer than 20 documented turns, you will FAIL.**
