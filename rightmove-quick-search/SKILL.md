---
name: rightmove-quick-search
description: |
  Search Rightmove and compare asking prices against recent sales data.
  Shows what is on the market and whether asking prices look fair. Use
  when someone asks "what's on Rightmove in [area]?" or "show me properties
  under [price]". Requires the Property MCP server.
---

# Quick Rightmove Search

You search Rightmove for current listings, then pull comparable sales for the same area so the user can see how asking prices compare to what properties actually sold for. This turns a raw property search into something useful.

## Required Setup

Connect the **Property MCP server**:

```json
{
  "mcpServers": {
    "property": {
      "url": "https://property-shared.fly.dev/mcp"
    }
  }
}
```

## Workflow

1. Get a UK postcode and optional filters: budget range, property type (detached, semi, terraced, flat), minimum bedrooms.

2. Call `rightmove_search` with the postcode, price range, and filters. Sort by price low.

3. Call `property_comps` for the same postcode. If the user specified a property type, use the property_type filter (F/D/S/T) to get relevant comps. This gives you the median sale price, price range, and recent transactions.

4. Now you have two datasets: what is being asked and what actually sold. Compare them:
   - Is the median asking price above or below the median sale price?
   - Which listings are priced below the comp median (potential value)?
   - Which are priced well above (overpriced or aspirational)?
   - What is the price spread like — tight market or wide range?

5. Present a market snapshot with the comparison, then list the 15 most noteworthy properties. Prioritise those priced below the comp median, recently reduced, or longest on market. Include the comp comparison for each.

## Output

```
## Rightmove: [Postcode]

### Market Context

- **On the market**: [N] properties ([type breakdown])
- **Median asking price**: £[X]
- **Median sale price** (last 24 months): £[X] from [N] transactions
- **Asking vs sold**: Asking prices are [X]% [above/below] recent sales
- **Price reductions**: [N] properties reduced (biggest cut: £[X] off)

### What This Tells You

[2-3 sentences interpreting the gap. E.g. "Asking prices are running 8% above what properties have actually sold for in this postcode over the last two years. The [N] reduced properties suggest some sellers are coming back to reality. Properties priced at or below £[comp median] are closer to where the market has actually transacted."]

---

### Listings (15 of [N])

| # | Address | Asking | Beds | Type | vs Comps | Days | Note |
|---|---------|--------|------|------|----------|------|------|
| 1 | [addr] | £[X] | [N] | [type] | -8% below | [N] | Below median |
| 2 | [addr] | £[X] | [N] | [type] | +12% above | [N] | Reduced £15k |
| 3 | [addr] | £[X] | [N] | [type] | -3% below | 90 | Long listed |
| ... | | | | | | | |

**vs Comps** = how the asking price compares to the median sale price for this postcode and property type. Negative means below what properties have sold for. Positive means above.

[N] more properties matched your filters.
```

## Output Rules

- British spelling throughout
- Prices as £X,000 with commas
- The **vs Comps** column is the key insight — always calculate it
- If comp data is thin (under 5 transactions), flag it: "Comp median based on only [N] sales — treat with caution"
- Do not estimate rental yields, calculate stamp duty, or give investment ratings
- Do not predict price movements
- Do not list more than 15 properties

## Want More?

This tells you what is on the market and whether asking prices look fair. It does not tell you which properties are worth buying as investments.

For yield calculations, stamp duty, investment scoring, and BUY/WATCH/PASS ratings, see the **Rightmove Investment Finder** at [bouch.dev/tools/rightmove-investment-finder](https://bouch.dev/tools/rightmove-investment-finder/).

For deep analysis of a single property, see the **Property Report Generator** at [bouch.dev/tools/property-report](https://bouch.dev/tools/property-report/).
