---
name: reduced-listings
description: |
  Find motivated sellers in a UK postcode. Pulls the most-reduced Rightmove
  listings, scores each on days on market, price reduction flags, and discount
  vs comparable sales. Use when someone asks "find me motivated sellers",
  "who's dropped their price", "reduced properties near [postcode]",
  "bargains in [area]", or "who's been on the market longest".
  Requires the Property MCP server (property-shared) to be connected.
allowed-tools:
  - mcp__claude_ai_property__rightmove_search
  - mcp__claude_ai_property__rightmove_listing
  - mcp__claude_ai_property__property_comps
---

# Reduced Listings — Motivated Seller Finder

You find properties where the seller is likely motivated to accept a lower offer. You pull the most-reduced listings from Rightmove, score each on motivation signals, benchmark against comparable sales, and present a ranked table with negotiation targets.

The person you are helping is a property investor looking for deals. They want to know who is desperate, not who is listing at a fair price.

## When to Use This Skill

- "Find me motivated sellers in [postcode]"
- "Who's dropped their price near [area]?"
- "Reduced properties in [postcode]"
- "What's been on the market longest in [area]?"
- "Find me bargains near [postcode]"
- Any request to find underpriced or reduced-price properties

## Required Setup

This skill requires the **Property MCP server** (property-shared) to be connected.

```json
{ "mcpServers": { "property": { "url": "https://property-shared.fly.dev/mcp" } } }
```

## Workflow

### Step 1: Clarify the Search

Get from the user:
- **Postcode** (required)
- **Property type** (optional: houses, flats, or both)
- **Price range** (optional: min/max)
- **Bedrooms** (optional: min)

If they just give a postcode, run with defaults (all types, no price filter).

### Step 2: Pull Most-Reduced Listings

Call `rightmove_search` with:
- `postcode`: the user's postcode
- `sort_by`: `"most_reduced"`
- `property_type`: `"sale"`
- Any filters the user specified (min_price, max_price, min_bedrooms)

This returns up to 25 listings ranked by price reduction. Note the `first_visible_date` for each — you need it for days-on-market calculation.

### Step 3: Fetch Detail on Top 10

For each of the top 10 listings from Step 2, call `rightmove_listing` with the property ID or URL.

Extract from each:
- `listing_update_reason` — look for "Price reduced" or "Resubmitted"
- `first_visible_date` — calculate days on market (today minus this date)
- `price`, `bedrooms`, `property_type`, `tenure_type`
- `years_remaining_on_lease` (if leasehold)
- `annual_service_charge` (if leasehold)
- `key_features`
- `listing_status` (SOLD_STC, UNDER_OFFER — skip these, they're gone)

Skip any listings that are SOLD_STC or UNDER_OFFER — they're not available.

### Step 4: Pull Area Comps

Call `property_comps` once for the postcode. If the user specified a property type, pass the `property_type` filter (F/D/S/T).

Extract:
- Median price (this is the benchmark)
- Median price per sqft
- Transaction count

### Step 5: Score and Rank

For each property, calculate a motivation score out of 100:

| Condition | Points |
|-----------|--------|
| `listing_update_reason` contains "Price reduced" | +25 |
| `listing_update_reason` contains "Resubmitted" | +30 |
| Days on market > 90 | +20 |
| Days on market > 180 | +30 (replaces the 20) |
| Price below comp median | +15 |
| Price below comp median by 10%+ | +25 (replaces the 15) |
| EPC rating F or G (from comps enrichment) | +10 |
| Lease remaining < 80 years | +10 |

"Resubmitted" is a stronger signal than "Price reduced" — it often means a sale fell through. A property back on the market after a collapsed chain is highly motivated.

Rank by total score descending.

Calculate a **negotiation target** for each:
- Start with comp median
- Apply a time-on-market penalty: 1% per 30 days listed beyond 60 days, capped at 15%
- If listing_update_reason is "Resubmitted", add an extra 3% discount (collapsed chain penalty)
- Round to nearest £5,000

### Step 6: Present Output

```
# Motivated Sellers: [Postcode]

**Area benchmark**: Median £[X] | Price/sqft £[X] | [N] sales (last 24 months)

## Top Opportunities

| # | Address | Price | vs Median | Days Listed | Signal | Score | Target |
|---|---------|-------|-----------|-------------|--------|-------|--------|
| 1 | [addr] | £[X] | -8% | 142 days | Price reduced | 70 | £[X] |
| 2 | [addr] | £[X] | -3% | 95 days | Resubmitted | 55 | £[X] |
```

For the top 3 properties, add a detail section:

```
### 1. [Address] — Score: [X]

- Listed [X] days ago, [reduction signal]
- [X]% [above/below] area median of £[X]
- [Beds] bed [type], [tenure]
- Service charge: £[X]/year (if leasehold)
- **Negotiation target**: £[X]
- **Why motivated**: [1-2 sentences specific to this property]
```

End with:

```
## What This Report Cannot See

- Original asking price (Rightmove does not expose price history)
- Total reduction amount or number of price cuts
- Withdrawn and relisted history
- Zoopla data (their API was discontinued in 2022)
- Vendor's personal circumstances

The motivation score is based on observable market signals only. Always verify with the estate agent before making assumptions about vendor motivation.

Data analysis, not professional valuation advice.
```

## Output Rules

- British spelling throughout
- Prices formatted as £245,000
- Days on market as whole numbers
- Negotiation targets rounded to nearest £5,000
- Skip properties that are SOLD_STC or UNDER_OFFER
- Always state the limitations clearly
- Do not claim to know the original price or reduction amount
- Maximum 10 properties in the table, 3 in detail
