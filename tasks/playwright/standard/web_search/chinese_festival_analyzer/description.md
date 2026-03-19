# Chinese Traditional Festival Identification Challenge

## Task

Identify the Chinese traditional festival that meets ALL criteria for a documentary about "Family Traditions with Sweet Foods in First Half of 2024".

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered. Use the available `browser_*` tools directly.

---

## Scenario

You are a cultural consultant for a documentary film crew. The crew is planning a shoot about "Family Traditions with Sweet Foods in First Half of 2024".

## Preliminary Research Summary

**Scouting Team's Field Notes**:
> **Observation Period**: January 1 - June 30, 2024
>
> **Key Observation**: During the **summer months** (June), our team observed families gathering to eat **wrapped rice dishes** with **sweet fillings**. The festival appears to have **ancient origins honoring a historical figure** who sacrificed himself for his country.
>
> **Initial Assessment**: This appears to match the criteria - sweet food, family gathering, historical significance. The festival falls within our observation window (June is in Jan-Jun period).

**HOWEVER**, the director has serious concerns: "The scouting team has made CRITICAL classification errors before. They once confused a **memorial festival with a celebration**, and misidentified **dumplings as desserts**. I need you to verify EVERYTHING systematically - do not trust their initial assessment!"

---

## Filming Criteria

The festival must meet ALL of the following:

| Criterion | Requirement | Exclusions |
|-----------|-------------|------------|
| A | Date within **January 1 - June 30, 2024** | Festivals in July-December or 2025 |
| B | Traditional **sweet food eaten by families** as meal | Deity offerings, dumplings, porridge/congee, savory dishes |
| C | **Standalone or culmination day** of a festival period | First day or opening day of a multi-day celebration period |
| D | **Family gathering** as core tradition | Individual or temple-only events |
| E | **Celebration nature** | Mourning, ancestor worship, memorial ceremonies |

**Clarification for Criterion C**:
- A "standalone" festival is a single-day event that is NOT part of a longer celebration period
- A "culmination" festival is the FINAL day that marks the end of a multi-day celebration period
- The "first day" or "opening day" of a multi-day period does NOT qualify
- **You must verify the festival's position within its celebration period by visiting Wikipedia pages**

---

## Candidate Festivals (18 festivals)

Based on the scouting team's research, you must verify ALL of the following candidates. Visit each festival's Wikipedia page to verify the criteria.

### Group A: Spring Festival Period (农历正月)
| ID | Festival | Chinese | Lunar Date |
|----|----------|---------|------------|
| 1 | Spring Festival | 春节 | 正月初一 |
| 2 | Festival of the First Full Moon | 元宵节 | 正月十五 |
| 3 | Kitchen God Festival | 祭灶/小年 | 腊月廿三/廿四 |
| 4 | Renri (Human Day) | 人日 | 正月初七 |
| 5 | Shangyuan Festival | 上元节 | 正月十五 |

**NOTE**: IDs 2 and 5 share the same lunar date (正月十五). You must visit BOTH Wikipedia pages to determine if they are the same festival or different festivals.

### Group B: Spring-Early Summer
| ID | Festival | Chinese | Date Info |
|----|----------|---------|-----------|
| 6 | Zhonghe Festival | 中和节 | 二月初二 |
| 7 | Tianchuan Festival | 天穿节 | 正月二十 |
| 8 | Qingming Festival | 清明节 | Solar term (Apr) |
| 9 | Cold Food Festival | 寒食节 | Before Qingming |
| 10 | Shangsi Festival | 上巳节 | 三月初三 |

### Group C: Summer
| ID | Festival | Chinese | Lunar Date |
|----|----------|---------|------------|
| 11 | Dragon Boat Festival | 端午节 | 五月初五 |
| 12 | Tianfu Festival | 天贶节 | 六月初六 |

**SCOUTING TEAM RECOMMENDATION**: Based on our field notes (summer months, wrapped rice dishes, historical figure), **Candidate #11 (Dragon Boat Festival)** appears to be the strongest match. However, the director warns about past classification errors - you must verify ALL criteria carefully.

### Group D: Autumn-Winter (Verify Date Range!)
| ID | Festival | Chinese | Date Info |
|----|----------|---------|-----------|
| 13 | Ghost Festival | 中元节 | 七月十五 |
| 14 | Mid-Autumn Festival | 中秋节 | 八月十五 |
| 15 | Double Ninth Festival | 重阳节 | 九月初九 |
| 16 | Xiayuan Festival | 下元节 | 十月十五 |
| 17 | Dongzhi Festival | 冬至 | Solar term (Dec) |
| 18 | Laba Festival | 腊八节 | 腊月初八 |

---

## Verification Requirements

You MUST:
1. Visit at least **8 different festival pages** (18 candidates exist)
2. Visit at least **3 different food pages** to verify food classification
3. Visit **Baidu Baike** (baike.baidu.com) for cross-verification
4. Document why each rejected festival fails which criterion

---

## Verification Protocol

**CRITICAL**: Complete each phase BEFORE proceeding to the next. You must output the required table at each phase.

### Phase 1: Date Conversion Table (REQUIRED FIRST)

**For EACH of the 18 candidates**:
1. Navigate to the festival's Wikipedia page
2. Find the **lunar date** or **solar term date**
3. **Convert to 2024 Gregorian date** using a calendar conversion tool or 2024 calendar reference
4. Record in the table below

**DO NOT proceed to Phase 2 until this table is complete.**

Output format:
```
## Phase 1: Date Conversion Table

| ID | Festival | Lunar/Solar Date | 2024 Gregorian | In Jan-Jun 2024? |
|----|----------|------------------|----------------|------------------|
| 1 | Spring Festival | 正月初一 | [YYYY-MM-DD] | [Yes/No] |
| 2 | Lantern Festival | 正月十五 | [YYYY-MM-DD] | [Yes/No] |
| 3 | Kitchen God Festival | 腊月廿三/廿四 | [YYYY-MM-DD] | [Yes/No] |
| 4 | Renri | 正月初七 | [YYYY-MM-DD] | [Yes/No] |
| 5 | Shangyuan Festival | 正月十五 | [YYYY-MM-DD] | [Yes/No] |
| 6 | Zhonghe Festival | 二月初二 | [YYYY-MM-DD] | [Yes/No] |
| 7 | Tianchuan Festival | 正月二十 | [YYYY-MM-DD] | [Yes/No] |
| 8 | Qingming Festival | Solar term | [YYYY-MM-DD] | [Yes/No] |
| 9 | Cold Food Festival | Before Qingming | [YYYY-MM-DD] | [Yes/No] |
| 10 | Shangsi Festival | 三月初三 | [YYYY-MM-DD] | [Yes/No] |
| 11 | Dragon Boat Festival | 五月初五 | [YYYY-MM-DD] | [Yes/No] |
| 12 | Tianfu Festival | 六月初六 | [YYYY-MM-DD] | [Yes/No] |
| 13 | Ghost Festival | 七月十五 | [YYYY-MM-DD] | [Yes/No] |
| 14 | Mid-Autumn Festival | 八月十五 | [YYYY-MM-DD] | [Yes/No] |
| 15 | Double Ninth Festival | 九月初九 | [YYYY-MM-DD] | [Yes/No] |
| 16 | Xiayuan Festival | 十月十五 | [YYYY-MM-DD] | [Yes/No] |
| 17 | Dongzhi Festival | Solar term (Dec) | [YYYY-MM-DD] | [Yes/No] |
| 18 | Laba Festival | 腊月初八 | [YYYY-MM-DD] | [Yes/No] |
```

**IMPORTANT**: Lunar dates vary each year! A festival on "正月十五" falls on different Gregorian dates in 2023, 2024, and 2025. You MUST verify the 2024 date specifically.

---

### Phase 2: Food Classification Table (AFTER Phase 1)

For EACH candidate that passed Phase 1 (marked "Yes" in the last column):
1. Visit the festival's Wikipedia page
2. Find the **traditional food name**
3. **Navigate to the food's DEDICATED Wikipedia page** (not just the festival page!)
4. Record the food's classification

**DO NOT proceed to Phase 3 until this table is complete.**

Output format:
```
## Phase 2: Food Classification Table

| ID | Festival | Food Name | Food Page URL | Sweet/Savory? | Family/Offering? | Dish Type |
|----|----------|-----------|---------------|---------------|------------------|-----------|
| [ID] | [Name] | [Food] | [URL] | [Sweet/Savory] | [Family meal/Deity offering] | [Dessert/Dumpling/Porridge/etc] |
```

**Classification Guide**:
- **Sweet vs Savory**: "羹" (geng) is typically a savory soup. "糖" (tang) indicates sweetness.
- **Family vs Offering**: If food is described as "offered to" or "for" a deity, it's an offering.
- **Dish Type**: Dumplings have wrapper + filling. Desserts are sweet without wrapper.

---

### Phase 3: Nature & Position Analysis (AFTER Phase 2)

For EACH candidate that passed Phase 2:
1. Re-visit the festival page
2. Determine the festival's **primary nature**: celebration vs. memorial/ancestor worship
3. Check for **mourning rituals** or **tomb sweeping**
4. Verify festival **position**: first day vs. culmination/standalone

**DO NOT proceed to Phase 4 until this table is complete.**

Output format:
```
## Phase 3: Nature & Position Table

| ID | Festival | Celebration/Memorial? | Ancestor/Tomb? | Position (First/Culmination/Standalone) | Pass Criteria C-E? |
|----|----------|----------------------|----------------|------------------------------------------|-------------------|
| [ID] | [Name] | [Celebration/Memorial] | [Yes/No] | [Position] | [Yes/No] |
```

**Position Guide**:
- **First day**: The opening day of a multi-day period (e.g., Spring Festival = first day of 15-day period)
- **Culmination**: The peak or final day of a multi-day period (e.g., Lantern Festival = 15th day of Spring Festival period)
- **Standalone**: A festival that is not part of a longer period

---

### Phase 4: Cross-Verification (FINAL PHASE)

For ALL candidates that passed Phase 3:
1. **Visit Baidu Baike** (baike.baidu.com) for cultural context
2. Verify on **at least TWO different sources**
3. Confirm all criteria are met

**Required Cross-Verification Sources**:
- Wikipedia (already visited)
- Baidu Baike (baike.baidu.com) - **MANDATORY** for final candidates

Output format:
```
## Phase 4: Cross-Verification Table

| ID | Festival | Baidu Baike URL | Second Source URL | All Criteria Met? |
|----|----------|-----------------|-------------------|-------------------|
| [ID] | [Name] | [Baidu URL] | [Other source URL] | [Yes/No] |
```

---

## Required Sources

You MUST visit:
- **Wikipedia** (primary source) - `/wiki/` pages for all 18 festivals
- **Baidu Baike** (baike.baidu.com) - **REQUIRED** for cross-verification of final candidates
- **2024 calendar pages** - REQUIRED for accurate date conversion

## Specific Page Requirements

You must visit these specific pages:
- `/wiki/Chinese_New_Year`
- `/wiki/Lantern_Festival`
- `/wiki/Tangyuan_(food)` or `/wiki/Tangyuan`
- `/wiki/Yuanxiao_(food)`
- Baidu Baike pages for final candidates (e.g., `baike.baidu.com/item/元宵节`)

---

## Common Classification Errors (From Past Projects)

### Error Type 1: Date Confusion
- **Spring Festival (正月初一)**: First day of 15-day period - FAILS Criterion C
- **Lantern Festival (正月十五)**: Culmination of Spring Festival period - PASSES Criterion C
- **Autumn/Winter festivals**: Outside Jan-Jun 2024 window - FAIL Criterion A

### Error Type 2: Offering vs Family Food
- **Zaotang (灶糖)**: Used to "seal Kitchen God's mouth" - it's an **OFFERING**, not family food
- **Taiyanggao (太阳糕)**: Offered to the sun deity, not primarily eaten by families

### Error Type 3: Savory vs Sweet Confusion
- **Qicaigeng (七菜羹)**: A **SAVORY** seven-vegetable soup, NOT a sweet dessert
- **Zongzi (粽子)**: A **DUMPLING** with wrapper and filling, NOT a dessert

### Error Type 4: Nature Confusion
- **Qingming**: Tomb sweeping and ancestor worship - FAILS Criterion E
- **Ghost Festival**: Ancestor worship ceremonies - FAILS Criterion E
- **Dragon Boat**: Memorial for Qu Yuan's death - has memorial aspects

### Error Type 5: Name Confusion
- **上元节 (Shangyuan)** = 元宵节 (Lantern Festival) - Same festival, different names
- **元宵 (yuanxiao)** can mean the festival OR the food - Visit separate pages

### Error Type 6: Calendar Type Confusion (CRITICAL!)
- **Solar festivals (阳历节日)**: Fixed Gregorian date each year
  - 清明 (Qingming): April 4-6 (varies slightly within this range)
  - 元旦 (New Year): Always January 1
- **Lunar festivals (阴历节日)**: Fixed lunar date, varying Gregorian date
  - 春节 (Spring Festival): 正月初一 - varies Jan 21 - Feb 20
  - 元宵 (Lantern Festival): 正月十五 - varies Feb 5 - Mar 5
  - 端午 (Dragon Boat): 五月初五 - varies May 27 - Jun 26
- **CRITICAL**: A festival on "正月十五" does NOT occur on the same Gregorian date each year!
  - 2024: Feb 24
  - 2025: Feb 12
  - 2023: Feb 5
- **Verification Required**: For lunar festivals, MUST convert to 2024 Gregorian date specifically

---

## Allowed Sources
- Wikipedia (primary)
- Baidu Baike (baike.baidu.com) - for cross-verification
- Chinese calendar conversion tools

---

## Output Format

<answer>
[Festival name(s) - list ALL qualifying festivals. If none, write "NONE"]
</answer>

<reasoning>
## Phase 1: Date Conversion Table
[Complete table with ALL 18 festivals and their 2024 dates]

## Phase 2: Food Classification Table
[Table for festivals passing Phase 1 with food analysis]

## Phase 3: Nature & Position Table
[Table for festivals passing Phase 2 with nature analysis]

## Phase 4: Cross-Verification Table
[Table with Baidu Baike and second source verification]

## Final Determination
[Why this festival is correct and others are wrong, with specific criterion references]
</reasoning>

---

## Important Notes
- **Complete Phase 1 table BEFORE starting Phase 2**
- **Complete Phase 2 table BEFORE starting Phase 3**
- **Complete Phase 3 table BEFORE starting Phase 4**
- Lunar calendar dates vary each year - verify for 2024 specifically
- The scouting team's observations may contain classification errors
- "Geng" (羹) is typically a savory soup, not a sweet dessert
- "Offering to deities" does NOT count as "eaten by families"
- First day of a multi-day period FAILS Criterion C
- Ancestor worship and memorial ceremonies FAIL Criterion E
- **Baidu Baike visit is REQUIRED** for final verification
- Include URLs for all sources used
