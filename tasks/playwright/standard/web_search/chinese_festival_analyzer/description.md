# Treasure Hunt Task: v105 - Wikipedia Link Chain

## CRITICAL: Follow the Chain - NO Direct Searching

**This task is different from typical web search tasks.**

You CANNOT search directly for the final answer.
You MUST follow a specific chain of links starting from a given URL.

---

## How This Task Works

1. Start at the given URL
2. Find a specific link on that page
3. Navigate to that link
4. Find another link on the new page
5. Repeat until you reach the final answer

**Each step depends on the previous step. You cannot skip steps.**

---

## Starting Point

**Navigate to:** https://en.wikipedia.org/wiki/List_of_festivals_in_China

This is your ONLY starting point. Do not search for other pages.

---

## Stage 1: Find the Festival (Follow Links)

### Task
Starting from the "List of festivals in China" page:
1. Find a festival that meets ALL conditions below
2. You MUST find this festival by following links from the starting page
3. You CANNOT search directly for "festival with green food"

### 6 Conditions
| # | Condition | Requirement |
|---|-----------|-------------|
| 1 | Appearance | Green |
| 2 | Taste | NOT sweet (savory or bitter) |
| 3 | Symbolism | Health or purification |
| 4 | Geographic | Jiangnan OR North China Plain |
| 5 | Historical | Before Tang Dynasty (618 CE) |
| 6 | Poet Connection | Associated with a famous poet |

### Link Chain Requirement
Document your navigation path:
```
<stage1>
Starting URL: https://en.wikipedia.org/wiki/List_of_festivals_in_China

Navigation Path:
1. [Page 1 URL] - [Link text you clicked]
2. [Page 2 URL] - [Link text you clicked]
3. ... continue until you find the festival

Festival Found: [Name]
Final URL: [URL where you found this festival]

Conditions Verification:
1. Appearance: Green - [Quote] - [URL]
2. Taste: NOT sweet - [Quote] - [URL]
3. Symbolism: Health/purification - [Quote] - [URL]
4. Geographic: [Quote] - [URL]
5. Historical: [Quote] - [URL]
6. Poet Connection: [Name] - [Evidence] - [URL]

Link on this page to poet information:
Poet Link URL: [URL found on the festival page]
</stage1>
```

---

## Stage 2: Find the Poem (Follow Links)

### Task
Starting from the festival page you found in Stage 1:
1. Find a link on that page to the poet's page
2. Navigate to the poet's page
3. Find a poem about the festival where the poet expresses **political frustration**

### CRITICAL
- You MUST navigate to the poet's page using a link from the festival page
- You CANNOT search directly for the poet

### Output Format
```
<stage2>
From Festival Page: [Festival URL from Stage 1]
Poet Link Found: [Link text] - [URL]
Navigated to Poet Page: [URL]

Poem Found:
Title: [Title]
Political Frustration Evidence: [Quote] - [URL]

Link on this page to biography:
Biography Link URL: [URL found on the poet page]
</stage2>
```

---

## Stage 3: Find the Event (Follow Links)

### Task
Starting from the poet's page:
1. Find a link to the poet's biography or life story
2. Navigate to that page
3. Find information about the poet's **political demotion**

### CRITICAL
- You MUST use a link from the poet's page
- You CANNOT search directly for "demotion event"

### Output Format
```
<stage3>
From Poet Page: [Poet URL from Stage 2]
Biography Link Found: [Link text] - [URL]
Navigated to Biography: [URL]

Demotion Event Found:
Description: [Quote]
Year: [YYYY]
Evidence: [Quote] - [URL]
</stage3>
```

---

## Stage 4: Verification

### Task
Verify the entire chain by checking consistency.

```
<stage4>
Complete Link Chain:
1. https://en.wikipedia.org/wiki/List_of_festivals_in_China
2. -> [Festival page URL]
3. -> [Poet page URL]
4. -> [Biography page URL]

Chain Consistency:
- Festival: [Name]
- Poet: [Name]
- Event: [Description]
- Year: [YYYY]

All links followed (not searched): [YES/NO]
</stage4>
```

---

## Final Answer

```
<answer>
Treasure Hunt Complete!

Link Chain:
1. List of festivals -> [Festival]
2. [Festival] -> [Poet]
3. [Poet] -> [Event in Year]

Total pages visited: [count]
Direct searches performed: 0 (requirement)
</answer>
```

---

## Scoring

Your answer will be evaluated on:
1. **Link chain integrity** - Did you follow links, not search directly?
2. **Correct festival** - Does it meet all 6 conditions?
3. **Chain consistency** - Does poet match festival? Does event match poet?

**IMPORTANT:** If you search directly instead of following links, you will FAIL.
