# Chinese Tea Classification - Professional Multi-Source Taxonomic Verification

## Task

Identify the correct Chinese tea from 20 candidates by conducting comprehensive research using multiple authoritative sources.

## Tools

IMPORTANT: The Playwright MCP server is pre-configured. Use the available `browser_*` tools directly.

---

## Scenario

You are a tea sommelier at a high-end Chinese tea house. A customer has brought in a mysterious tea sample and wants to know exactly which famous Chinese tea it is. Your apprentice has made some initial observations, but you need to verify these against authoritative sources before making a definitive identification.

## Your Apprentice's Field Notes (Research Phase 1)

**Observer**: Tea Apprentice (2 years experience)
**Source**: Visual inspection and basic tasting
**Date**: March 2025

### Initial Observations

1. **Dry leaf color**: Dark reddish-brown with some green undertones
2. **Leaf shape**: Tightly twisted, strip-like form (not ball-rolled)
3. **Aroma**: Roasted, woody notes with hints of orchid
4. **Liquor color**: Orange-red to amber when brewed
5. **Taste profile**: Rich, mellow, with a lingering sweetness (hui gan)
6. **Finish**: Distinct mineral quality with rocky character
7. **Steeping durability**: Can be brewed 7-8 times

### Apprentice's Initial Assessment

> "Based on the reddish-brown color and amber liquor, I believe this is a Black Tea (Hong Cha). The customer mentioned it's a famous tea from Fujian. My best guess is Lapsang Souchong or perhaps a Fujian Black Tea."

**YOUR TASK**: Verify or refute this assessment using authoritative sources. The apprentice may have made errors in classification!

---

## Candidate Teas (20) - ALL MUST BE INVESTIGATED

You must systematically investigate ALL 20 candidates. For each tea, you must determine:
- The tea category (Green, White, Oolong, Black, Dark)
- The oxidation level (exact percentage)
- The processing method
- The origin (province, mountain)
- The sensory characteristics

### Fujian Black Teas (Hong Cha)
1. **Lapsang Souchong** (正山小种) - Wuyi Mountains
2. **Jin Jun Mei** (金骏眉) - Wuyi Mountains
3. **Tanyang Gongfu** (坦洋工夫) - Fuan
4. **Zhenghe Gongfu** (政和工夫) - Zhenghe

### Wuyi Rock Teas (Yancha)
5. **Da Hong Pao** (大红袍) - Wuyi Mountains
6. **Tie Luo Han** (铁罗汉) - Wuyi Mountains
7. **Bai Ji Guan** (白鸡冠) - Wuyi Mountains
8. **Shui Jin Gui** (水金龟) - Wuyi Mountains
9. **Rou Gui** (肉桂) - Wuyi Mountains

### Anxi Oolong Teas
10. **Tie Guan Yin** (铁观音) - Anxi
11. **Huang Jin Gui** (黄金桂) - Anxi
12. **Ben Shan** (本山) - Anxi

### Phoenix Oolong Teas (Guangdong)
13. **Fenghuang Dancong** (凤凰单丛) - Chaozhou

### Taiwanese Oolong Teas
14. **Dong Ding** (冻顶) - Nantou
15. **Alishan** (阿里山) - Chiayi

### Other Categories
16. **Pu'er Sheng** (普洱生茶) - Yunnan
17. **Pu'er Shou** (普洱熟茶) - Yunnan
18. **Dian Hong** (滇红) - Yunnan
19. **Keemun** (祁门红茶) - Anhui
20. **Tai Ping Hou Kui** (太平猴魁) - Anhui

---

## CRITICAL TAXONOMIC DISTINCTIONS

### Distinction 1: "Black Tea" vs "Dark Tea" vs "Oolong"

In Chinese tea classification:
- **Hong Cha (红茶)** = Black Tea in English = FULLY OXIDIZED (100%)
- **Hei Cha (黑茶)** = Dark Tea in English = POST-FERMENTED
- **Oolong (乌龙茶)** = Semi-oxidized tea (10-85% oxidation)

**IMPORTANT**: The term "Red Tea" (红茶) in Chinese refers to what English calls "Black Tea"!

### Distinction 2: Color Can Be Deceptive

**WARNING**: Tea leaf color does NOT always indicate tea category!
- Some teas have "Red" (红) in their name but are NOT Black Tea
- **Oxidation level**, not color, determines classification
- You MUST verify the **oxidation percentage** from authoritative sources

### Distinction 3: Processing Method Matters

Different tea categories have different processing:
- **Green tea**: Kill-green (杀青) → no oxidation
- **Oolong**: Withering → oxidation (10-85%) → kill-green
- **Black tea**: Full oxidation (100%) → drying
- **Dark tea**: Post-fermentation (microbial)

---

## MANDATORY MULTI-SOURCE INVESTIGATION

**You MUST use BOTH sources for verification:**

### Source 1: Wikipedia (en.wikipedia.org)

For each tea, visit Wikipedia to verify:
- Tea category
- Oxidation level
- Processing method
- Origin

### Source 2: Baidu Baike (baike.baidu.com)

**CRITICAL**: Wikipedia may have incomplete information about:
- Exact oxidation percentages
- Regional sensory characteristics
- Chinese-specific terminology

For each tea, visit Baidu Baike to cross-verify:
- Oxidation percentage (exact number)
- Sensory characteristics (leaf shape, liquor color, taste)
- Regional characteristics

### Source 3: Specialty Tea Sources (Optional)

For additional verification, you may use:
- Teapedia (teapedia.org)
- Chinese tea association websites

---

## Investigation Protocol

### Step 1: Category Verification (MANDATORY)

For ALL 20 candidates, you must:
1. Visit Wikipedia to find the tea category
2. Visit Baidu Baike to verify oxidation percentage
3. Record the exact oxidation level (not a range)

**Do NOT rely on tea names!** Some teas have misleading names.

### Step 2: Origin Verification (MANDATORY)

For candidates matching the category:
1. Verify the origin province and mountain
2. Determine if the origin matches the field notes
3. Record any regional characteristics

### Step 3: Sensory Profile Verification (MANDATORY)

For remaining candidates, verify ALL sensory characteristics:
1. Dry leaf color and shape
2. Liquor color
3. Taste profile
4. Steeping durability

**Match against ALL 7 field observations.**

### Step 4: Cross-Source Verification (MANDATORY)

For final candidates:
- Verify from at least 2 sources
- Document any discrepancies between sources
- Explain which source you trust and why

---

## Output Format

<answer>
[Tea Name in English] + [Tea Name in Chinese]
</answer>

<reasoning>
## Step 1: Category Verification Table
| Tea | Category | Oxidation % | Source URL | Eliminated? |
|-----|----------|-------------|------------|-------------|
| T1 | ... | ...% | ... | Yes/No |
... (ALL 20 teas MUST be investigated)

## Step 2: Origin Verification Table
| Tea | Province | Mountain | Source URL | Eliminated? |
|-----|----------|----------|------------|-------------|
| ... | ... | ... | ... | Yes/No |

## Step 3: Sensory Verification Table
| Tea | Leaf Shape | Liquor | Taste | Durability | Match? |
|-----|------------|--------|-------|------------|--------|
| ... | ... | ... | ... | ... | Yes/No |

## Step 4: Cross-Source Verification
[Verify top candidates from multiple sources with URLs]

## Final Determination
[Why this tea is correct]
[Explain the taxonomic trap that led to the apprentice's error]
[Include ALL source URLs used]
</reasoning>

---

## Allowed Sources

- Wikipedia (en.wikipedia.org)
- Baidu Baike (baike.baidu.com) - **MANDATORY for oxidation verification**
- Teapedia (teapedia.org)
- Chinese tea association websites

---

## Important Notes

1. **The apprentice's assessment may be WRONG** - verify independently!
2. **Tea names can be misleading** - some teas have "Red" in the name but are not Black Tea
3. **Oxidation level determines category**, not leaf color
4. **Cross-source verification is mandatory** - do not rely on a single source
5. **Include ALL source URLs** in your reasoning
6. **Verify ALL 20 candidates** before finalizing your answer
