# Chinese Traditional Festival Cross-Analyzer

## Task
Identify the Chinese traditional festival that meets ALL criteria for a documentary about "Family Traditions with Sweet Foods in First Half of 2024".

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered. Use the available `browser_*` tools directly.

---

## Scenario
A documentary researcher needs to identify Chinese festivals for a film about "Family Traditions with Sweet Foods in First Half of 2024".

**Filming Requirements:**
1. Festival must occur within **First Half of 2024 (January 1 - June 30, 2024)** (filming window)
2. Festival must feature a traditional sweet food **eaten by families as a meal** (not just candy/snack, not just offering to deities)
3. Festival must be a **standalone celebration or culmination day** (not the first day of a longer period)
4. Festival must have **family gathering** as a core tradition

**CRITICAL NEGATIVE CONSTRAINTS:**
- **Food CANNOT be**: dumpling/dumpling-like food, porridge/congee, or food primarily used as offering to deities
- **Festival CANNOT involve**: mourning rituals, ancestor worship ceremonies, or memorial activities

**CRITICAL**: Chinese festivals follow the **lunar calendar**, which means their Gregorian dates shift each year. You must verify the EXACT 2024 Gregorian date for each festival by consulting a lunar calendar conversion resource.

---

## Initial Observation (from location scouting team)

"Our preliminary research identified several promising candidates for the documentary:

1. **Qingming Festival** - April 4, 2024
   - Has qingtuan (green glutinous rice balls)
   - Families gather together
   - Date falls nicely in the first half of 2024
   - CONCERN: Need to verify if qingtuan is classified as sweet food or dumpling

2. **Dragon Boat Festival** - June 10, 2024
   - Has zongzi (sticky rice wrapped in bamboo leaves)
   - Strong family reunion traditions
   - Date is right at the end of our filming window
   - CONCERN: Need to verify food classification and fillings

3. **Chinese New Year** - February 10, 2024
   - The most important family reunion festival
   - Features sweet niangao (rice cake)
   - CONCERN: Need to verify if this is a standalone day or first day of longer period

Based on initial screening, Qingming and Dragon Boat appear most promising since their dates fall clearly in the first half. However, our team has made serious classification errors before - you must verify each criterion yourself."

---

## CRITICAL WARNING

Our location scouting team has made **systematic errors** in past projects:

1. **Food Classification Errors**:
   - Called zongzi 'sweet food' when it's actually a **dumpling** (dumpling-like food does NOT qualify)
   - Called qingtuan 'sweet dessert' when it's a **dumpling** (glutinous rice wrapper)
   - Called zaotang 'family food' when it's primarily an **offering to deities**
   - Called laba porridge 'dessert' when it's primarily a **porridge/congee**

2. **Festival Position Misunderstanding**:
   - They confuse 'first day of multi-day period' with 'standalone day'
   - The **first day** of a multi-day celebration FAILS Criterion C
   - The **culmination/final day** of a multi-day celebration PASSES Criterion C

3. **Mourning Ritual Oversight**:
   - They have included festivals that involve **ancestor worship** or **memorial ceremonies**
   - Any festival with mourning/remembrance of deceased does NOT qualify

4. **Date Boundary Errors**:
   - They sometimes forget that "first half of year" means **January 1 to June 30**
   - Festivals in July or later FAIL Criterion A

**DO NOT TRUST the initial observations without verification!**

---

## MANDATORY VERIFICATION PROTOCOL (4-Phase Process)

**CRITICAL**: You must complete ALL four phases sequentially. Skipping phases will result in incomplete analysis.

### Phase 1: Date Screening
For EACH festival, you MUST:
1. Visit the festival's Wikipedia page
2. Find the lunar calendar date (e.g., "15th day of 1st lunar month")
3. Convert to 2024 Gregorian date using a lunar calendar resource
4. Determine if date falls within January 1 - June 30, 2024

**CROSS-VERIFICATION REQUIRED**: You must verify the 2024 date using at least TWO different sources:
- Wikipedia festival page
- A lunar calendar conversion page (e.g., Wikipedia's Chinese calendar article, or a dedicated lunar calendar site)

### Phase 2: Food Classification
For each festival that passes Phase 1, you MUST:
1. Identify the traditional food from the festival page
2. Visit the food's dedicated Wikipedia page
3. Find EXPLICIT classification (dessert/dumpling/porridge/offering)
4. Determine if it's "eaten by families as a meal" or "primarily an offering"

**CROSS-VERIFICATION REQUIRED**: For borderline cases, check BOTH Wikipedia and Baidu Baike

### Phase 3: Festival Nature Analysis
For each festival that passes Phase 2, you MUST:
1. Determine if festival is "first day", "standalone day", or "culmination day"
2. Check for ANY mention of mourning, ancestor worship, or memorial activities
3. Verify family gathering is a CORE tradition (not just mentioned)

### Phase 4: Final Validation
For each remaining candidate, you MUST:
1. Re-verify ALL criteria with a second source
2. Document the specific exclusion reason for each rejected candidate
3. Confirm the final answer meets ALL five criteria

---

## Candidate Festivals (15 festivals)

You must verify ALL of the following candidates systematically:

### Spring Festival Period (January - February)
| ID | Festival | Wikipedia URL |
|----|----------|---------------|
| 1 | Laba Festival | /wiki/Laba_Festival |
| 2 | Kitchen God Festival | /wiki/Kitchen_God_Festival |
| 3 | Chinese New Year | /wiki/Chinese_New_Year |
| 4 | Lantern Festival | /wiki/Lantern_Festival |
| 5 | Renri (Human Day) | /wiki/Renri |
| 6 | Tianchuan Festival | /wiki/Tianchuan_Festival |

### Spring Season (March - May)
| ID | Festival | Wikipedia URL |
|----|----------|---------------|
| 7 | Zhonghe Festival | /wiki/Zhonghe_Festival |
| 8 | Qingming Festival | /wiki/Qingming_Festival |
| 9 | Cold Food Festival | /wiki/Cold_Food_Festival |

### Summer Season (June)
| ID | Festival | Wikipedia URL |
|----|----------|---------------|
| 10 | Dragon Boat Festival | /wiki/Dragon_Boat_Festival |

### Autumn-Winter Season (July - December)
| ID | Festival | Wikipedia URL |
|----|----------|---------------|
| 11 | Qixi Festival | /wiki/Qixi_Festival |
| 12 | Ghost Festival | /wiki/Ghost_Festival |
| 13 | Mid-Autumn Festival | /wiki/Mid-Autumn_Festival |
| 14 | Double Ninth Festival | /wiki/Double_Ninth_Festival |
| 15 | Dongzhi Festival | /wiki/Dongzhi_Festival |

---

## Allowed Sources
- Wikipedia (primary)
- Baidu Baike (baike.baidu.com) - for cross-verification of food classification
- Lunar calendar resources (for date verification)

---

## Selection Criteria

Find the festival that meets **ALL** conditions:

- **A**: Date falls within **First Half of 2024 (January 1 - June 30, 2024)**
- **B**: Has traditional sweet food **eaten by families as a meal** (NOT dumpling, NOT porridge, NOT offering to deities)
- **C**: Festival must be a **standalone day or culmination day** (NOT the first day of a multi-day celebration period)
- **D**: Must have **family eating together** as a core tradition
- **E**: Festival must NOT involve **mourning, ancestor worship, or memorial ceremonies**

---

## Food Classification Requirements

**CRITICAL**: For each festival's food, you MUST:

1. **Visit the food's Wikipedia page** (e.g., /wiki/Tangyuan, /wiki/Zongzi, etc.)
2. **Determine the food's classification**:
   - Is it explicitly classified as a **dessert** or **sweet dish** in the article?
   - Is it classified as a **dumpling**, **porridge**, or **savory dish**?
   - Is it primarily described as an **offering** to deities?
3. **Only foods explicitly classified as desserts/sweet dishes eaten by families** qualify under Criterion B

**Key Classification Rules**:
- **Dumplings** (zongzi, qingtuan, jiaozi, etc.) = Do NOT qualify (dumpling-like)
  - A "dumpling" has a distinct wrapper/skin and filling structure
  - Zongzi: sticky rice WRAPPED in bamboo/reed leaves = dumpling-like
  - Qingtuan: glutinous rice WRAPPER with filling = dumpling-like
- **Porridge/Congee** (laba porridge, etc.) = Do NOT qualify (not dessert)
- **Offerings** (zaotang, etc.) = Do NOT qualify (not family meal)
- **Sweet rice balls** (tangyuan, yuanxiao) = **May qualify** - these are NOT dumplings
  - Tangyuan/yuanxiao are made from glutinous rice flour mixed with water to form a dough, NOT a wrapper + filling structure
  - They are solid spheres, not wrapped items

**What counts as "eaten by families as a meal"**:
- The food must be traditionally consumed by families together during the festival
- It does NOT need to be a "main course" - traditional festival foods eaten together count
- Families gathering to share the traditional food is sufficient
- What does NOT count: foods primarily used as offerings to deities/ancestors

---

## Festival Nature Verification

**CRITICAL**: For each festival, you MUST verify:

1. **Does the festival involve mourning or ancestor worship?**
   - Check if the festival involves tomb sweeping, ancestor memorials, or remembrance of deceased
   - Festivals with mourning components FAIL Criterion E

2. **Is the festival the first day or culmination of a period?**
   - First day of multi-day celebration FAILS Criterion C
   - Culmination/final day PASSES Criterion C
   - Standalone day PASSES Criterion C

---

## Verification Checklist

For EACH of the 15 festivals, complete this verification:

1. [ ] **Lunar Date**: What is the lunar calendar date?
2. [ ] **Gregorian Date 2024**: What is the 2024 Gregorian date? Is it within Jan 1 - Jun 30, 2024?
3. [ ] **Date Cross-Check**: Did you verify with a second source?
4. [ ] **Food Identification**: What is the traditional food? Visit its Wikipedia page.
5. [ ] **Food Classification**: Is the food dessert/sweet dish, dumpling, porridge, or offering?
6. [ ] **Food Purpose**: Is it eaten by families as a meal, or primarily used as offering?
7. [ ] **Festival Position**: Is this the first day of a multi-day period, or a standalone/culmination day?
8. [ ] **Festival Nature**: Does this festival involve mourning, ancestor worship, or memorial ceremonies?
9. [ ] **Family Tradition**: Is family gathering a core tradition?
10. [ ] **Exclusion Reason**: If rejected, what is the SPECIFIC reason?

---

## Output Format

**CRITICAL**: You MUST output BOTH sections in the exact order below:

<answer>
<FESTIVALS>
[List ALL qualifying festival names, one per line - if none, write "NONE"]
</FESTIVALS>
<DATES>
[List 2024 dates in YYYY-MM-DD format for each qualifying festival]
</DATES>
<FOODS>
[List the sweet food for each qualifying festival]
</FOODS>
</answer>

<verification>
## Phase 1: Date Screening Results
[For each of the 15 festivals:
- Festival name
- Lunar calendar date
- 2024 Gregorian date
- Source 1 (festival page)
- Source 2 (lunar calendar resource)
- Within H1 2024? (Y/N)]

## Phase 2: Food Classification Results
[For each festival passing Phase 1:
- Festival name
- Food name
- Food Wikipedia page URL
- Classification from Wikipedia (dessert/dumpling/porridge/offering)
- Cross-check from Baidu Baike (if applicable)
- Purpose: family meal/offering to deities
- PASSES Criterion B? (Y/N)]

## Phase 3: Festival Nature Analysis
[For each festival passing Phase 2:
- Festival name
- Position: first day/standalone/culmination
- Mourning/ancestor worship? (Y/N)
- Family gathering core? (Y/N)
- PASSES Criteria C, D, E? (Y/N)]

## Phase 4: Exclusion Summary
[For ALL 15 festivals, document the SPECIFIC exclusion reason:]

| Festival | Date | In H1? | Food | Food OK? | Position OK? | Nature OK? | Family OK? | EXCLUSION REASON |
|----------|------|--------|------|----------|--------------|------------|------------|------------------|
| ... | YYYY-MM-DD | Y/N | food name | Y/N | Y/N | Y/N | Y/N | [Specific criterion failed] |

## Final Determination
[List the qualifying festival(s) and explain why they meet ALL criteria]
</verification>

**IMPORTANT**: The `<verification>` section MUST appear AFTER the `</answer>` tag. Do NOT place analysis before the answer.

---

## Important Notes
- **Mandatory 4-phase verification**: You MUST complete ALL four phases sequentially
- **Minimum page visits**: You must visit at least 7 festival pages, at least 3 food pages, and at least 1 lunar calendar resource
- **Cross-verification required**: Dates must be verified with 2 sources; borderline foods must be cross-checked with Baidu Baike
- **Date verification**: "First Half 2024" means January 1 - June 30
- **Dumpling exclusion**: Dumpling-like foods (zongzi, qingtuan, jiaozi) do NOT qualify as sweet food
- **Porridge exclusion**: Porridge/congee (laba porridge) do NOT qualify as dessert
- **Offering exclusion**: Foods primarily offered to deities do NOT qualify as family meal
- **Mourning exclusion**: Festivals involving ancestor worship or memorial ceremonies do NOT qualify
- **Festival position**: Distinguish between "first day of period" vs "standalone/culmination day"
- **Exclusion documentation**: You MUST provide a specific exclusion reason for each rejected candidate
- **Trap awareness**: The initial observation contains ERRORS - verify everything yourself!
