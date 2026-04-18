---
name: rightmove-investment-finder
description: |
  Search Rightmove for investment properties matching your criteria, then
  analyse each for yield, comps, and stamp duty. Produces a ranked shortlist
  with BUY/WATCH/PASS ratings. Use when someone asks "find me investment
  properties in [area]" or "what's available under 200k?". Requires the
  Property MCP server. Optional: UK Legal MCP for BTL tax and leasehold checks.
---

# Rightmove Investment Finder

You search Rightmove for properties matching investment criteria, then analyse each candidate against comparable sales, yield targets, and stamp duty. You produce a ranked shortlist a property investor can act on.

This skill finds properties worth analysing. For deep analysis of a single known property, use the Property Report Generator.

## When to Use This Skill

- "Find me investment properties in [area]"
- "What's available under 200k in [postcode]?"
- "Search Rightmove for BTL opportunities"
- "Find high-yield properties near [location]"
- "What buy-to-let properties are there in [area]?"
- Any request to search for and rank investment properties

## Required Setup

### Property MCP (required)

```json
{
  "mcpServers": {
    "property": {
      "url": "https://property-shared.fly.dev/mcp"
    }
  }
}
```

API docs: https://property-shared.fly.dev/docs

### UK Legal MCP (optional — for BTL tax notes and leasehold checks)

```json
{
  "mcpServers": {
    "uk-legal": {
      "url": "https://uk-legal-mcp.fly.dev/mcp"
    }
  }
}
```

### Tools you will use (in order)

1. `rightmove_search` — find listings matching criteria (postcode, property_type, min_price, max_price, min_bedrooms, sort_by)
2. `property_comps` — comparable sales for a postcode (postcode, property_type filter: F/D/S/T)
3. `rental_analysis` — rental market data (postcode, purchase_price)
4. `property_yield` — yield calculation combining Land Registry and Rightmove data (postcode, property_type)
5. `stamp_duty` — SDLT calculation (price, additional_property)
6. `rightmove_listing` — full details on a specific property (property_id from search results)
7. (optional) `hmrc_search_guidance` — BTL income tax guidance from HMRC
8. (optional) `legislation_search` — leasehold reform legislation checks

## Workflow

### Step 1: Get Search Criteria

Gather from the user:
- **Area or postcode** (required) — `rightmove_search` needs a postcode. If the user gives a town name, ask for a postcode.
- **Budget range** (required) — "under 200k" means max_price=200000. If they give a single number, treat it as the maximum.
- **Property type** (optional) — detached, semi, terraced, flat. Default: all types.
- **Minimum bedrooms** (optional) — default: no minimum.
- **Yield target** (optional) — default: 5% gross.

If the user gives vague criteria like "somewhere cheap up north", ask them to narrow it to a specific postcode or area.

### Step 2: Search Rightmove

Call `rightmove_search` with:
- `postcode`: the user's postcode
- `property_type`: "sale"
- `min_price` / `max_price`: from their budget
- `min_bedrooms`: if specified
- `sort_by`: "price_low" (cheapest first surfaces highest potential yield)

This returns listings with: property IDs, prices, addresses, bedrooms, property types, postcodes, days on market, and Rightmove URLs.

### Step 3: First-Pass Filter

From the search results, select the **8-12 most promising candidates** based on:
- Price within budget
- Correct property type (if specified)
- Minimum bedroom count (if specified)

If all results qualify, take the top 12 by lowest price (higher yield potential). This step is pure filtering on data already returned — no additional tool calls.

### Step 4: Pull Comps

For each **unique postcode** among your candidates, call `property_comps` once. Group by postcode to minimise tool calls — one postcode's comps cover all candidates in that area.

Use the `property_type` filter to match the listing types (F for flats, D for detached, etc.). This prevents terraced house comps skewing flat analysis.

From each result, extract:
- Median sale price
- Price per square foot (where EPC-enriched)
- Transaction count (sample size)

For each candidate, calculate:
- **Price premium/discount** = (asking price - median) / median
- Flag if the asking price is more than 10% above the comp median

### Step 5: Pull Rental Data and Yield

For each unique postcode, call `rental_analysis` with `purchase_price` set to the comp median for that area. Also call `property_yield` with the same postcode and property_type filter.

Cross-reference the two results. Watch for:
- Student lets skewing average rents (common in university towns)
- HMO rents mixed in with single-let figures
- Very few rental listings (thin data)

**Normalise all rents to monthly** before any calculation. If rental_analysis returns weekly figures, multiply by 52 and divide by 12.

Extract:
- Median monthly rent
- Gross yield %
- Number of rental listings (sample size)

### Step 6: Calculate Stamp Duty

For each candidate, call `stamp_duty` with:
- `price`: the asking price
- `additional_property`: true (default for investors)

Group identical asking prices to avoid duplicate calls.

The current additional property surcharge is 5% (since October 2024). The tool handles the banding automatically.

Extract:
- Total SDLT payable
- Effective tax rate

### Step 7: Score and Rank

Score each candidate on three signals:

| Signal | 3 points | 2 points | 1 point |
|--------|----------|----------|---------|
| Yield vs target | Meets or exceeds target | Within 1% of target | Below target by more than 1% |
| Price vs comps median | Below median | Within 5% of median | Above median by more than 5% |
| Days on market | Over 60 days (motivated seller) | 30-60 days | Under 30 days |

**Maximum score: 9**

Assign ratings:
- **BUY** (score 8-9): All criteria met or exceeded. Strong candidate.
- **WATCH** (score 5-7): Close but one flag. Worth monitoring or negotiating.
- **PASS** (score 1-4): Does not stack up against your criteria.

Sort the shortlist by total score descending, then by yield descending within each rating band.

### Step 8: Enrich Top Candidates

For the **top 3 BUY-rated properties** (or top 3 overall if fewer than 3 score BUY):

Call `rightmove_listing` with each property's ID to get full details: tenure (freehold/leasehold), remaining lease term, service charge, ground rent, key features, and floorplan data.

**If the UK Legal MCP is connected:**
- For leasehold properties, call `legislation_search` with "Leasehold and Freehold Reform Act 2024" to note recent reform implications (ground rent caps, right to manage, lease extension changes).
- If the user asks about BTL tax, call `hmrc_search_guidance` with "buy to let income tax" for relevant HMRC guidance on landlord taxation.

## Output Format

```
# Investment Search: [Area/Postcode]

**Criteria**: [budget] | [property type or "all types"] | [beds] | [yield target]%
**Search date**: [today's date]
**Results**: [N] properties searched, [M] shortlisted

---

## Shortlist

### 1. [Address] — BUY
- **Price**: £[X] | **Beds**: [N] | **Type**: [terraced/flat/etc]
- **Yield**: [X]% gross ([X]% net est.)
- **Price vs comps**: [X]% [below/above] median (£[median] from [N] sales)
- **Stamp duty**: £[X] ([X]% effective, additional property rate)
- **Days on market**: [N]
- **Tenure**: [freehold/leasehold — remaining term if applicable]
- **Link**: [Rightmove URL]
> [One sentence: why this scored BUY — e.g. "Yield exceeds target, priced 8% below comps, 90 days on market suggests room to negotiate."]

### 2. [Address] — WATCH
...

---

## Area Summary

- **Median sale price**: £[X] ([N] transactions, last 24 months)
- **Median rent**: £[X] pcm ([N] active rental listings)
- **Area gross yield**: [X]%

## Notes

- [Any data quality flags: thin comps, student let mix, etc.]
- [BTL tax note if Legal MCP was used]
- [Leasehold note if applicable]

---

This is data analysis, not investment advice. Verify all figures independently before making offers. Consult a qualified adviser for tax and legal decisions.
```

## Output Rules

- British spelling throughout (analyse, colour, organised)
- Present prices as £X,000 format with commas
- Round yields to one decimal place
- Always state data sources and date ranges for comps
- Default to additional property stamp duty (additional_property=true)
- Normalise all rents to monthly before calculations
- If comp count is under 5 for a postcode, flag as "thin data — treat median with caution"
- If days on market is not available, omit from scoring (score out of 6 instead of 9, adjust thresholds: BUY >= 5, WATCH 3-4, PASS < 3)
- Do not predict future prices or rental growth
- Always include the disclaimer at the bottom
- Include Rightmove links for every shortlisted property

## What This Skill Does NOT Do

- Provide mortgage advice or affordability calculations
- Predict future property prices or rental growth
- Replace a RICS valuation or building survey
- Give personal tax advice (beyond linking to HMRC guidance)
- Assess structural condition or renovation costs
- Guarantee rental income or account for void periods
- Factor in management fees (mention that net yield estimates do not include agent fees)

## Related Skills

- **Property Report Generator** — deep analysis of a single property you have already identified
- **Property Deal Screener** — quick go/no-go from a Rightmove URL
- **Property Report to Google Sheets** — export property data to a structured spreadsheet
