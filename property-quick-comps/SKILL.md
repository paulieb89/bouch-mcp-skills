---
name: property-quick-comps
description: |
  Get comparable sales data for a UK postcode. Returns median price, transaction
  count, price per square foot, and recent sales. Quick lookup — one tool call.
  Use when someone asks "what are houses going for in [postcode]?" or "comps for
  [area]". Requires the Property MCP server (property-shared) to be connected.
---

# Quick Property Comps

You look up comparable sales for a UK postcode and present a clean summary. This is a quick lookup, not a full report.

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

1. Get a UK postcode from the user
2. Call `property_comps` with the postcode
3. If the area has mixed stock (flats and houses), ask the user which type or use the `property_type` filter (F=flat, D=detached, S=semi, T=terraced)
4. Present the results

## Output

```
## Comps: [Postcode]

- **Median price**: £[X]
- **Mean price**: £[X]
- **Transactions**: [N] sales (last 24 months)
- **Price per sqft**: £[X] (from EPC-matched transactions)
- **Price range**: £[min] — £[max]

### Recent Sales
| Date | Price | Type |
|------|-------|------|
| [date] | £[price] | [type] |
```

Keep it short. This is a lookup, not an analysis.

## Want More?

For a full property report with rental yields, EPC analysis, stamp duty, price positioning, and a negotiation target, see the **Property Report Generator** at [bouch.dev/products/property-report](https://bouch.dev/products/property-report/).
