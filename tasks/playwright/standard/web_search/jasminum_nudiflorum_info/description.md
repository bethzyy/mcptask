# Botanical Garden Plant Identification Challenge (v35)

## Task

Identify a yellow-flowering shrub from the East Asia collection by systematically verifying your field observations against authoritative botanical sources.

## Tools

IMPORTANT: The Playwright MCP server is pre-configured and already registered.
Use the available `browser_*` tools directly.

Do NOT spawn a subprocess or manually start the MCP process.

---

## Scenario

You are a volunteer intern at a botanical garden. During your first week, you observed a yellow-flowering shrub and took detailed notes. Now you need to confirm its identity before updating the garden database.

## Your Field Notes (Feb 20 - Mar 5, 2026)

**Observer**: Volunteer Intern
**Location**: East Asia Collection, Bed 7

### Morphological Observations

1. **Growth habit**: Deciduous shrub, approximately 1.2-1.8m tall with arching branches
2. **Branches**: Slender, distinctly **4-angled** when young, green to greenish-brown
3. **Flower characteristics**:
   - Color: Bright golden yellow
   - Arrangement: Solitary or in small clusters
   - **Petal count**: **5 to 6 petals** (counted on 8 different flowers by 3 volunteers, counts varied: 5, 5, 5, 6, 6, 6, 5, 6)
   - **Petal appearance**: Petals appear **separate and distinct**, not fused at the base
   - Corolla shape: Funnel-shaped
   - Flowers bloom **before leaves emerge**
4. **Bloom period**: Late February to early March
5. **Provenance**: Label reads "Wild-collected seeds from **Henan Province, China** (low elevation area, <500m)"

### Additional Notes from Garden Records

- Specimen planted in 2019 from wild-collected seeds
- Collection number: HNZ-2018-047
- Habitat note: "Open slopes, forest edges"

## Senior Horticulturist's Comment

> "Yellow-flowering shrubs in early spring are notoriously difficult to identify. Several genera have similar growth forms and flowering times. I'd recommend checking authoritative taxonomic descriptions carefully - particularly for corolla morphology and provincial distribution. The provenance information (Henan Province) should help narrow down the possibilities. Focus on species that occur there naturally, not just in cultivation."

## Candidate Plants (20 species)

You must investigate ALL of the following candidates systematically:

### Jasminum Genus (Yellow-flowering species)
1. Winter Jasmine (Jasminum nudiflorum)
2. Spring Jasmine (Jasminum floridum)
3. Yunnan Jasmine (Jasminum mesnyi)
4. Himalayan Jasmine (Jasminum humile)
5. Primrose Jasmine (Jasminum mesnyi f. holosericeum)
6. Italian Jasmine (Jasminum humile var. humile)

### Forsythia Genus
7. Weeping Forsythia (Forsythia suspensa)
8. Green-stem Forsythia (Forsythia viridissima)
9. Border Forsythia (Forsythia × intermedia) - HYBRID
10. Korean Forsythia (Forsythia koreana)
11. Early Forsythia (Forsythia ovata)
12. European Forsythia (Forsythia europaea)
13. Girald Forsythia (Forsythia giraldiana)

### Other Yellow-flowering Shrubs
14. Kerria (Kerria japonica)
15. Paperbush (Edgeworthia chrysantha)
16. Wintersweet (Chimonanthus praecox)
17. Chinese Witch Hazel (Hamamelis mollis)
18. Cornelian Cherry (Cornus mas)
19. Spike Hazel (Corylopsis spicata)
20. White Forsythia (Abeliophyllum distichum)

## Verification Requirements

### Step 1: Flora of China Investigation
Navigate to efloras.org and search for BOTH genera:
- **Forsythia**: Record corolla structure (how many lobes? fused or separate?), and provincial distribution for each species
- **Jasminum**: Record corolla lobe count, corolla tube characteristics, and distribution for yellow-flowering species

### Step 2: Provincial Distribution Analysis
For each candidate, determine if **Henan Province** appears in its **native/wild distribution** (not cultivation records).
- Cross-reference with Kew POWO for distribution accuracy
- Hybrids (marked ×) do NOT occur naturally in the wild

### Step 3: Multi-Source Verification
For all species with Henan distribution, verify the following on at least TWO sources:
- Exact corolla lobe/petal count
- Corolla tube characteristics (fused or separate)
- Altitude/habitat preferences

### Step 4: Reconcile Observations
Your field notes indicate "5-6 separate petals." Taxonomic descriptions may use different terminology. Explain:
- How your observation relates to the actual floral morphology
- What feature distinguishes the correct species from similar alternatives
- Why some candidates that seem to match your observations are actually incorrect

---

## Output Format

<answer>
Plant name (Latin binomial)
</answer>

<reasoning>
## Step 1: Flora of China Data
[List ALL species with corolla structure and distribution]

## Step 2: Provincial Distribution
[Which species have Henan in their NATIVE range?]

## Step 3: Cross-Verification
[Multi-source verification with specific URLs]

## Step 4: Observation Reconciliation
[Explain how your observations relate to actual morphology, and how you determined the correct species]

## Final Determination
[Why this species is correct and others are wrong]
</reasoning>

---

## Allowed Sources

- Wikipedia
- Baidu Baike (百度百科)
- Kew POWO (powo.science.kew.org)
- Missouri Botanical Garden (missouribotanicalgarden.org)
- RHS (rhs.org.uk)
- Flora of China (efloras.org)

---

## Important Notes

- Field observations may contain errors or use non-technical terminology
- "Separate petals" might actually be "corolla lobes" of a fused tube
- "Native distribution" excludes cultivation records
- Hybrid species (×) do NOT occur naturally in the wild
- Include URLs for all sources used
