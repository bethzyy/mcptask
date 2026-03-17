# Chinese Traditional Festival Cross-Analyzer

## Task
Analyze ten major Chinese traditional festivals and identify which meet specific criteria based on their 2024 Gregorian calendar dates, traditional foods, and customs.

## Tools
IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## Festivals to Analyze
1. Chinese New Year (Spring Festival) - https://en.wikipedia.org/wiki/Chinese_New_Year
2. Lantern Festival - https://en.wikipedia.org/wiki/Lantern_Festival
3. Dragon Boat Festival - https://en.wikipedia.org/wiki/Dragon_Boat_Festival
4. Mid-Autumn Festival - https://en.wikipedia.org/wiki/Mid-Autumn_Festival
5. Double Ninth Festival - https://en.wikipedia.org/wiki/Double_Ninth_Festival
6. Qingming Festival - https://en.wikipedia.org/wiki/Qingming_Festival
7. Winter Solstice (Dongzhi Festival) - https://en.wikipedia.org/wiki/Dongzhi_Festival
8. Laba Festival - https://en.wikipedia.org/wiki/Laba_Festival
9. Hungry Ghost Festival - https://en.wikipedia.org/wiki/Hungry_Ghost_Festival
10. Kitchen God Festival - https://en.wikipedia.org/wiki/Kitchen_God_Festival

## Allowed Sources
Use only the following authoritative sources:
- Wikipedia (primary source for festival and food information)
- Baidu Baike for additional verification

Avoid: personal blogs, forums, social media posts, commercial websites.

## Task Requirements

For each festival, you must:
- Visit the Wikipedia page and extract:
  - 2024 Gregorian Date in MM/DD format
  - Traditional Sweet Foods
  - Key Customs

- For each sweet food mentioned, visit its Wikipedia page to verify if it is classified as a dessert.

## Selection Criteria

Find all festivals that meet ALL of the following conditions:
- Condition A: 2024 date falls in the first half of the year (January 1 - June 30)
- Condition B: Traditional food must be Wikipedia explicitly classify as a dessert
- Condition C: Does NOT include dragon boat racing as a custom
- Condition D: Festival name does NOT contain the word Nine (in English or Chinese)
- Condition E: The sweet food must have a dedicated Wikipedia article

## Output Format

You MUST output EXACTLY:

<answer>
<FESTIVALS>
[List each qualifying festival name, one per line]
</FESTIVALS>
<DATES>
[List corresponding 2024 dates in MM/DD format, one per line]
</DATES>
<DESSERTS>
[List corresponding sweet foods, one per line]
</DESSERTS>
</answer>

## Important Notes
- Visit all TEN Wikipedia pages to collect complete information
- Use the 2024 Gregorian calendar date
- Dumpling, congee, cake are not desserts even if they have sweet fillings
- Dragon boat racing is specifically a competitive sport
- Sweet foods must be sweet in taste, not savory dishes
- Be careful with the negative constraints
