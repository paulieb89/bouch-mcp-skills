---
name: investment-summary
description: |
  Generate a property investment summary from a Rightmove URL. Pulls the
  listing details, area comparables, rental market, and key financials
  into a structured investment brief. Use when someone shares a Rightmove
  link and wants to know if it's worth buying, what the yield would be,
  or how it compares to the area. Requires the Property MCP server.
---

# Investment Summary Generator

You take a Rightmove property URL and produce a structured investment summary that a property investor, landlord, or developer can use to make a decision.

## When to Use This Skill

- Someone shares a Rightmove URL
- "Is this property worth buying?"
- "What's the yield on this?"
- "Pull me an investment summary"
- "How does this compare to the area?"
- "Should I make an offer?"

## Required Setup

This skill requires the **Property MCP server** (property-shared) to be connected, and web access to fetch the Rightmove listing page.

## Workflow

### Step 1: Get the Listing Details

Try `rightmove_listing` with the full URL first. If it errors (some property IDs, especially newer or commercial listings, can fail), fall back to WebFetch on the same URL.

Extract: address, postcode, asking price, property type, bedrooms/size, tenure, EPC, key features, service charge/ground rent, council tax band.

**Important:** Rightmove listings often hide the exact house number. Ask the user to confirm the full address (including house number) before pulling EPC or area data in Step 2. Getting the address wrong means the comps and EPC will be off.

### Step 2: Pull Area Data

**Call sequence matters. Pull data in this order:**

1. `property_comps` with the address and postcode (ppd_months=24, search_radius=0.25 for city centre or 0.5 for suburbs, property_type to match listing: F/D/S/T). Extract the **median price** for yield calculations.
2. `property_epc` for the specific address. Flag if floor area mismatches the listing.
3. `rental_analysis` with the address AND `purchase_price` set to the median comp price from step 1. This populates gross_yield_pct and yield_assessment.
4. `rightmove_search` (channel: RENT) for actual rental listings. This is essential because rental_analysis aggregates can mix weekly student lets with monthly professional lets, producing misleading medians.
5. `property_yield` with the address for a second yield calculation to cross-check.
6. `stamp_duty` with the asking price.
7. `rightmove_search` (channel: BUY) for current sales market context.

### Step 3: Normalise Rental Data

**Critical:** Before calculating any yields, normalise all rents to monthly. Weekly prices (common in student areas like Nottingham) must be converted: weekly x 52 / 12 = monthly.

Segment the rental market:
- **Professional lets:** monthly pricing, standard tenancies. Use these for BTL yield calculations.
- **Student lets:** weekly pricing, HMO-style. Report separately. Only use for yield if the user asks about student HMO.

If rental_analysis aggregates look wrong (e.g. median rent is suspiciously low), check the raw rightmove_search listings to see if student lets are skewing the data.

### Step 4: Calculate Financials

**For residential buy-to-let:**
- Gross yield = (annual professional rent / purchase price) x 100
- Use the **professional let median** from normalised rightmove_search data, NOT the mixed rental_analysis aggregate
- Compare with property_yield tool output. If they differ, explain why.
- Net yield estimate: deduct 30% for management, voids, maintenance, insurance
- Stamp duty from stamp_duty tool (calculate both primary and additional property scenarios)
- Total acquisition cost = price + SDLT + estimated £2,000 legal/survey fees

**For commercial:**
- Gross yield from estimated commercial rent (note: Property MCP rental data is residential only)
- Note business rates liability
- Flag different lending requirements

### Step 4: Write the Summary

Structure the output as:

```
## Investment Summary: [Address]

**Asking Price:** £X | **Tenure:** X | **EPC:** X | **Type:** X

### Property
[2-3 sentences: what it is, size, key features, condition notes]

### Area Comparables ([postcode sector], last 24 months)
- Transaction count, median, mean, range
- Where the asking price sits relative to median (above/below, by how much %)

### Current Sales Market ([radius])
- Properties listed, median asking, range
- How this property compares to what else is available

### Rental Market ([radius])
- Listings, median rent, range
- Flag if data is residential but property is commercial

### Yield Estimate
- Gross yield %
- Net yield estimate %
- Stamp duty amount
- Total acquisition cost

### Key Considerations
- 3-5 bullet points: risks, opportunities, things to investigate
- Be specific: "vacant for X months suggests negotiation room" not "consider market conditions"

### Summary
- One paragraph: is this fairly priced, what's the investment case, what would you want to check before making an offer
```

## Output Rules

- British spelling throughout
- Present prices as £X,000 format
- Round yields to one decimal place
- Always state data sources and date ranges
- If data is thin (fewer than 5 comps), flag it explicitly
- Do not predict future prices
- Do not give mortgage or tax advice
- Flag if residential rental data is being used for a commercial property
- Note the disclaimer: data analysis, not professional valuation

## What This Skill Does NOT Do

- Provide mortgage affordability calculations
- Give tax advice (beyond basic SDLT)
- Predict price movements
- Replace a RICS survey or valuation
- Assess structural condition
- Advise on planning permission or listed building consent
