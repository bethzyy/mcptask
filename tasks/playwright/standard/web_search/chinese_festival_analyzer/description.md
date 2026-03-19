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
> **Key Observation**: During the **Spring Festival period** (农历正月), our team observed families gathering to eat **sweet glutinous rice balls** (汤圆/元宵). The festival appears to have ancient origins, with historical texts referring to it as **"上元节" (Shangyuan Festival)**.
>
> **Initial Assessment**: This appears to be a perfect match - sweet food, family gathering, celebration nature. The Spring Festival period falls within our observation window.

**HOWEVER**, the director has concerns: "The scouting team has made classification errors before. They once confused a Taoist ritual day with a folk celebration, and misidentified deity offerings as family foods. I need you to verify everything systematically."

---

## Filming Criteria

The festival must meet ALL of the following:

| Criterion | Requirement | Exclusions |
|-----------|-------------|------------|
| A | Date within **January 1 - June 30, 2024** | Festivals in July-December or 2025 |
| B | Traditional **sweet food eaten by families** as meal | Deity offerings, dumplings, porridge/congee, savory dishes |
| C | **Standalone or culmination day** | First day of multi-day period |
| D | **Family gathering** as core tradition | Individual or temple-only events |
| E | **Celebration nature** | Mourning, ancestor worship, memorial ceremonies |

---

## Candidate Festivals (18 festivals)

You must systematically verify ALL of the following candidates. **Lunar dates are provided where applicable; you must convert to 2024 Gregorian dates to verify Criterion A.**

### Group A: Spring Festival Period (农历正月)
| ID | Festival | Chinese | Lunar Date | Wikipedia URL |
|----|----------|---------|------------|---------------|
| 1 | Spring Festival | 春节 | 正月初一 | /wiki/Chinese_New_Year |
| 2 | Lantern Festival | 元宵节 | 正月十五 | /wiki/Lantern_Festival |
| 3 | Kitchen God Festival | 祭灶/小年 | 腊月廿三/廿四 | /wiki/Kitchen_God_Festival |
| 4 | Renri (Human Day) | 人日 | 正月初七 | /wiki/Renri |
| 5 | Shangyuan Festival | 上元节 | 正月十五 | /wiki/Shangyuan_Festival |

### Group B: Spring-Early Summer
| ID | Festival | Chinese | Date Info | Wikipedia URL |
|----|----------|---------|-----------|---------------|
| 6 | Zhonghe Festival | 中和节 | 二月初二 | /wiki/Zhonghe_Festival |
| 7 | Tianchuan Festival | 天穿节 | 正月二十 | /wiki/Tianchuan_Festival |
| 8 | Qingming Festival | 清明节 | Solar term (Apr) | /wiki/Qingming_Festival |
| 9 | Cold Food Festival | 寒食节 | Before Qingming | /wiki/Cold_Food_Festival |
| 10 | Shangsi Festival | 上巳节 | 三月初三 | /wiki/Shangsi_Festival |

### Group C: Summer
| ID | Festival | Chinese | Lunar Date | Wikipedia URL |
|----|----------|---------|------------|---------------|
| 11 | Dragon Boat Festival | 端午节 | 五月初五 | /wiki/Dragon_Boat_Festival |
| 12 | Tianfu Festival | 天贶节 | 六月初六 | /wiki/Tianfu_Festival |

### Group D: Autumn-Winter (Verify Date Range!)
| ID | Festival | Chinese | Date Info | Wikipedia URL |
|----|----------|---------|-----------|---------------|
| 13 | Ghost Festival | 中元节 | 七月十五 | /wiki/Ghost_Festival |
| 14 | Mid-Autumn Festival | 中秋节 | 八月十五 | /wiki/Mid-Autumn_Festival |
| 15 | Double Ninth Festival | 重阳节 | 九月初九 | /wiki/Double_Ninth_Festival |
| 16 | Xiayuan Festival | 下元节 | 十月十五 | /wiki/Xiayuan_Festival |
| 17 | Dongzhi Festival | 冬至 | Solar term (Dec) | /wiki/Dongzhi_Festival |
| 18 | Laba Festival | 腊八节 | 腊月初八 | /wiki/Laba_Festival |

---

## Verification Protocol

### Step 1: Date Verification (Critical!)
For EACH candidate festival:
1. Visit the festival's Wikipedia page
2. Find the **lunar date** or **solar term date**
3. **Convert to 2024 Gregorian date** using:
   - Chinese calendar conversion tools
   - 2024 calendar references
4. Record: Does it fall within **Jan 1 - Jun 30, 2024**?

**IMPORTANT**: Lunar dates vary each year! Do not assume fixed Gregorian dates.

### Step 2: Food Classification Investigation
For each candidate that passes Step 1:
1. Find the **traditional food name** on the festival page
2. **Visit the food's DEDICATED Wikipedia page** (not just the festival page!)
3. Record:
   - Is it classified as **dessert/sweet** or **savory/vegetable**?
   - Is it eaten by **families as a meal** or primarily as **offering to deities**?
   - Is it **dumpling-like** (wrapper + filling) or **porridge/congee**?

### Step 3: Festival Nature & Position Analysis
For each candidate that passes Steps 1-2:
1. Determine the festival's **primary nature**: celebration vs. memorial/ancestor worship
2. Check if the festival involves **mourning rituals** or **tomb sweeping**
3. Verify festival **position**: first day vs. culmination/standalone

### Step 4: Cultural Context Verification
For all candidates that pass Steps 1-3:
1. Verify ancient names and aliases (e.g., 上元节 vs 元宵节)
2. Check Taoist/Buddhist origins vs. folk traditions
3. Verify on at least **TWO sources**

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
## Step 1: Date Verification
[List ALL 18 festivals with their 2024 Gregorian dates and whether they pass Criterion A]

## Step 2: Food Classification
[List festivals passing Step 1 with their traditional food, food classification, and purpose]

## Step 3: Nature and Position
[Which festivals are celebrations (not memorials)? What are their positions?]

## Step 4: Cultural Context
[Multi-source verification with specific URLs and cultural context]

## Final Determination
[Why this festival is correct and others are wrong]
</reasoning>

---

## Important Notes
- Lunar calendar dates vary each year - verify for 2024 specifically
- The scouting team's observations may contain classification errors
- "Geng" (羹) is typically a savory soup, not a sweet dessert
- "Offering to deities" does NOT count as "eaten by families"
- First day of a multi-day period FAILS Criterion C
- Ancestor worship and memorial ceremonies FAIL Criterion E
- Include URLs for all sources used
