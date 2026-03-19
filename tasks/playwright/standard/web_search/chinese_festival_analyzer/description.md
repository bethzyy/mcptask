# Chinese Traditional Festival Identification Challenge

## Task
Identify the Chinese traditional festival that meets all criteria for a documentary about "Family Traditions with Sweet Foods in First Half of 2024".

## CRITICAL WARNING
**YOU MUST VISIT ALL 19 REQUIRED PAGES.** The verify.py script will check your execution.log. If ANY page is missing, the task will FAIL immediately.

## Tools
IMPORTANT: The Playwright MCP server is pre-configured. Use `browser_*` tools directly.

---

## Scenario
You are a cultural consultant for a documentary about "Family Traditions with Sweet Foods in First Half of 2024".

**Scouting Team's Field Notes**:
> **Observation Period**: January 1 - June 30, 2024
> **Key Observation**: During summer months (June), families eat wrapped rice dishes with sweet fillings. The festival honors a historical figure.
> **Initial Assessment**: Appears to match criteria - sweet food, family gathering, historical significance.
> **DIRECTOR'S WARNING**: "The scouting team has made CRITICAL errors before - confusing memorial festivals with celebrations, misidentifying dumplings as desserts. Verify EVERYTHING!"

---

## Filming Criteria
The festival must meet ALL:
| Criterion | Requirement | Exclusions |
|-----------|-------------|------------|
| A | Date within **Jan 1 - Jun 30, 2024** | Jul-Dec 2024 or 2025 |
| B | **Sweet food eaten by families** | Offerings, dumplings, porridge, savory |
| C | **Standalone or culmination day** | First day of multi-day period |
| D | **Family gathering** core tradition | Temple-only events |
| E | **Celebration nature** | Mourning, ancestor worship, memorial |

**Criterion C Clarification**:
- "Culmination" = FINAL day of multi-day period (e.g., 15th day of Spring Festival)
- "First day" does NOT qualify

---

## Candidate Festivals (18)

| ID | Festival | Chinese | Date Info |
|----|----------|---------|-----------|
| 1 | Spring Festival | 春节 | 正月初一 |
| 2 | Lantern Festival | 元宵节 | 正月十五 |
| 3 | Kitchen God Festival | 祭灶 | 腊月廿三 |
| 4 | Renri | 人日 | 正月初七 |
| 5 | Shangyuan Festival | 上元节 | 正月十五 |
| 6 | Zhonghe Festival | 中和节 | 二月初二 |
| 7 | Tianchuan Festival | 天穿节 | 正月二十 |
| 8 | Qingming Festival | 清明节 | Solar term (Apr) |
| 9 | Cold Food Festival | 寒食节 | Before Qingming |
| 10 | Shangsi Festival | 上巳节 | 三月初三 |
| 11 | Dragon Boat Festival | 端午节 | 五月初五 |
| 12 | Tianfu Festival | 天贶节 | 六月初六 |
| 13 | Ghost Festival | 中元节 | 七月十五 |
| 14 | Mid-Autumn Festival | 中秋节 | 八月十五 |
| 15 | Double Ninth Festival | 重阳节 | 九月初九 |
| 16 | Xiayuan Festival | 下元节 | 十月十五 |
| 17 | Dongzhi | 冬至 | Solar term (Dec) |
| 18 | Laba Festival | 腊八节 | 腊月初八 |

**NOTE**: IDs 2 and 5 share the same lunar date (正月十五). Visit BOTH pages to determine if they are the same festival.

**SCOUTING RECOMMENDATION**: Based on field notes, Candidate #11 (Dragon Boat Festival) appears strongest. However, verify ALL criteria carefully due to past classification errors.

---

## Required Pages (19 - ALL MANDATORY)

### Festival Pages (16):
1. `/wiki/Chinese_New_Year`
2. `/wiki/Lantern_Festival`
3. `/wiki/Kitchen_God`
4. `/wiki/Renri`
5. `/wiki/Shangyuan_Festival`
6. `/wiki/Zhonghe_Festival`
7. `/wiki/Tianchuan_Festival`
8. `/wiki/Qingming_Festival`
9. `/wiki/Cold_Food_Festival`
10. `/wiki/Shangsi_Festival`
11. `/wiki/Dragon_Boat_Festival`
12. `/wiki/Ghost_Festival`
13. `/wiki/Mid-Autumn_Festival`
14. `/wiki/Double_Ninth_Festival`
15. `/wiki/Dongzhi`
16. `/wiki/Laba_Festival`

### Food Pages (2):
17. `/wiki/Tangyuan_(food)`
18. `/wiki/Zongzi`

### Cross-Verification (1):
19. `baike.baidu.com/item/元宵节`

**CRITICAL**: verify.py checks ALL 19 pages. Missing ANY page = FAIL.

---

## Common Classification Errors

| Error Type | Example | Issue |
|------------|---------|-------|
| Date Confusion | Spring Festival = FIRST day of 15-day period | FAILS Criterion C |
| Offering vs Family | Zaotang = offered to Kitchen God | FAILS Criterion B |
| Savory vs Sweet | Qicaigeng = savory soup, Zongzi = dumpling | FAILS Criterion B |
| Nature Confusion | Qingming = tomb sweeping, Dragon Boat = memorial | FAILS Criterion E |
| Calendar Type | Lunar dates vary each year | Must verify 2024 date specifically |

**Lunar Date Examples (正月十五)**:
- 2024: Feb 24
- 2025: Feb 12
- 2023: Feb 5

---

## Output Format
```
<answer>
[Festival name(s). If none, write "NONE"]
</answer>
<reasoning>
## Phase 1: Date Conversion Table
| ID | Festival | 2024 Date | In Jan-Jun? |
## Phase 2: Food Classification Table
| ID | Festival | Food | Sweet/Family? |
## Phase 3: Nature & Position Table
| ID | Festival | Celebration/Memorial? | Position? |
## Phase 4: Cross-Verification
| ID | Festival | Baidu URL |
## Final Determination
[Explanation]
</reasoning>
```

---

## Important Notes
- Complete Phase 1 before Phase 2, Phase 2 before Phase 3, etc.
- Lunar dates vary each year - verify for 2024 specifically
- "Geng" (羹) = savory soup, NOT sweet dessert
- "Offering to deities" ≠ "eaten by families"
- First day of multi-day period FAILS Criterion C
- Ancestor worship/memorial FAILS Criterion E
- Baidu Baike visit is REQUIRED
