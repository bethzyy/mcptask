# Rare Chinese Tea Processing Challenge (v79)

## Task
You are a tea historian researching ancient Chinese tea processing methods for a documentary about the Tang Dynasty. Your mission is to discover which Chinese green tea still uses the **steaming method (蒸青)** AND has a documented history dating back to the **Tang Dynasty (618-907 CE)**.

**Starting point**: <https://en.wikipedia.org/wiki/Green_tea>

***

## BACKGROUND

Historically, Chinese green tea was processed using steaming (蒸青). However, after the early Ming dynasty, most Chinese green teas switched to pan-firing (炒青). Today, steaming is primarily associated with **Japanese** green teas like Sencha and Gyokuro.

**YOUR MISSION**:
Find the ONE **Chinese** green tea that satisfies ALL of the following conditions:

1. Uses the **steaming method (蒸青)** as the primary fixation method
2. Is produced in **mainland China** (not Japan, Taiwan, or other regions)
3. Has **documented history dating back to the Tang Dynasty (618-907 CE)**
4. Is produced in **Hubei Province (湖北省)**
5. Is **NOT** a tea that originated from Japan or was influenced by Japanese tea culture

***

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly

Do not spawn a process or manually start the MCP process

***

## CRITICAL WARNINGS - READ CAREFULLY

### Trap 1: Japanese Teas
Japanese steamed teas do NOT qualify:
- **Sencha (煎茶)** - Japanese, not Chinese
- **Gyokuro (玉露)** - Japanese, not Chinese
- **Matcha (抹茶)** - Japanese, not Chinese

### Trap 2: Gunpowder Tea
**Gunpowder tea (珠茶)** from Zhejiang Province:
- ✅ Uses steaming as part of its process
- ✅ Is Chinese, not Japanese
- ❌ Originated in the **Ming Dynasty**, not Tang Dynasty
- ❌ Is from **Zhejiang**, not Hubei Province

This is a **LOCAL OPTIMAL TRAP** - it looks correct but fails the historical constraint!

### Trap 3: Similar-Named Teas
- **Yulu (玉露)** appears in both Chinese and Japanese tea names
- The **Chinese** Enshi Yulu (恩施玉露) is the correct answer
- The **Japanese** Gyokuro (also 玉露) is NOT the answer

***

## Investigation Requirements

**PHASE 1**: Broad Exploration
- Start from the Green tea Wikipedia page
- Investigate at least **15 different teas** (Chinese, Japanese, and other regions)
- For each tea, record: name, origin, processing method, historical period, and Wikipedia URL
- You must include at least 5 Japanese teas and 10 Chinese teas in your investigation

**PHASE 2**: Historical Verification
- For any tea that uses steaming, verify its **historical origin**
- Check if it dates back to Tang Dynasty or later dynasties
- You must find historical evidence from Wikipedia

**PHASE 3**: Province Verification
- Confirm the tea is from **Hubei Province**
- Cross-reference with geographical information

**PHASE 4**: Final Verification
- Confirm the tea is NOT related to Japanese tea culture
- Verify all 5 conditions are satisfied

***

## REQUIRED Output Format

**PHASE 1**: Investigation Log (at least 10 teas)

```markdown
<investigation_log>
| Tea Name | Origin (Country/Province) | Processing Method | Historical Period | Wikipedia URL |
|----------|--------------------------|-------------------|-------------------|---------------|
| [Tea 1] | [Country/Province] | [steaming/pan-firing/other] | [Tang/Song/Ming/Qing/Modern] | [URL] |
| ... | ... | ... | ... | ... |
</investigation_log>
```

**Note**: You must investigate at least **15 different teas** (5 Japanese + 10 Chinese minimum).

**PHASE 2**: Final Answer

```markdown
<answer>
<steamed_tea>
[Name of the Chinese green tea that satisfies ALL conditions]
</steamed_tea>

<tea_province>
[Province where this tea is produced - must be Hubei]
</tea_province>

<historical_origin>
[Documented historical period - must mention Tang Dynasty connection]
</historical_origin>

<processing_description>
[Describe the steaming process - minimum 50 characters]
</processing_description>

<historical_context>
[Explain the historical significance and Tang Dynasty connection - minimum 100 characters]
</historical_context>

<verification>
<evidence_1>
<sentence>[Quote about the tea's processing method from Wikipedia - minimum 50 characters]</sentence>
<source>[Full Wikipedia URL]</source>
</evidence_1>
<evidence_2>
<sentence>[Quote about the tea's historical origin or Tang Dynasty connection - minimum 50 characters]</sentence>
<source>[Full Wikipedia URL - must be different from evidence_1]</source>
</evidence_2>
<evidence_3>
<sentence>[Quote confirming the tea's province or geographical origin - minimum 50 characters]</sentence>
<source>[Full Wikipedia URL - must be different from evidence_1 and evidence_2]</source>
</evidence_3>
<evidence_4>
<sentence>[Quote about the tea's unique characteristics or cultural significance - minimum 50 characters]</sentence>
<source>[Full Wikipedia URL - must be different from evidence_1, evidence_2, and evidence_3]</source>
</evidence_4>
</verification>

<exclusion_statement>
[Explain why Gunpowder tea does NOT qualify despite using steaming - mention both the dynasty and province differences]
</exclusion_statement>

<comparison>
[List at least 5 other Chinese green teas that use pan-firing, with their provinces]
</comparison>
</answer>
```

***

## Success Criteria

Your answer will be considered correct if and only if ALL of the following are true:

| # | Condition | Verification |
|---|-----------|--------------|
| 1 | Tea uses steaming (蒸青) | Evidence must mention "steaming" or "蒸青" |
| 2 | Tea is from mainland China | Must not be Japanese, Taiwanese, etc. |
| 3 | Tea has Tang Dynasty history | Historical evidence required |
| 4 | Tea is from Hubei Province | Province must be verified |
| 5 | Tea is not Japanese-influenced | Must be authentically Chinese |
| 6 | Four different Wikipedia sources | URLs must be from 4 different pages |
| 7 | 15 teas in investigation log | At least 5 Japanese + 10 Chinese teas |

***

## Tips

1. **Start with history**: The Green tea page discusses historical processing methods
2. **Check multiple sources**: Don't rely on a single Wikipedia page
3. **Beware of Gunpowder tea**: It's a trap - wrong dynasty AND wrong province
4. **Use Chinese Wikipedia**: zh.wikipedia.org may have more detailed historical information
5. **Verify the province**: Multiple sources should confirm Hubei Province
