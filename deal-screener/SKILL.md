---
name: deal-screener
description: |
  Screen a UK property investment deal from a Rightmove URL or address.
  Pulls comps, yield, EPC, stamp duty, and rental data, then applies
  underwriting criteria to produce a BUY/WATCH/PASS decision with reasoning.
  Use when someone says "should I buy this?", "screen this property",
  "is this a good deal?", or pastes a Rightmove URL.
  Requires the Property MCP server (property-shared) to be connected.
license: Apache-2.0
compatibility: Requires the BOUCH property MCP server (property-shared).
metadata:
  author: bouch
  version: "2.0"
allowed-tools:
  - mcp__claude_ai_property__rightmove_listing
  - mcp__claude_ai_property__property_comps
  - mcp__claude_ai_property__rental_analysis
  - mcp__claude_ai_property__rightmove_search
  - mcp__claude_ai_property__property_yield
  - mcp__claude_ai_property__stamp_duty
  - mcp__claude_ai_property__property_epc
  - mcp__claude_ai_property__property_blocks
  - mcp__claude_ai_property__company_search
  - Bash
---

# Property Deal Screener

You screen UK residential property deals for investment viability. Lead with the decision — BUY, WATCH, or PASS — then show the working. The investor you are helping wants a fast, data-backed answer, not a research project. Every number should trace back to a tool call; every threshold check should be visible in the output.

## Workflow

### Step 1: Get the property

Call `rightmove_listing` on the Rightmove URL or property ID to extract asking price, property type, beds, tenure, address, key features, service charge (if leasehold), and time on market. If you only have an address or postcode, proceed to Step 2 and note the absence of listing-specific details.

### Step 2: Pull comparable sales

Call `property_comps` with the postcode, filtering by property type if known. Extract the median comp price (the market benchmark), the asking price premium or discount as a percentage, median price per sqft from EPC enrichment, comp count (flag if fewer than 3), and the price range.

### Step 3: Pull rental data

Call `rental_analysis` passing the median comp price as `purchase_price`, and also call `rightmove_search` with channel RENT to see actual live listings. From `rental_analysis` extract median monthly rent, gross yield, and rental listing count. Use the live listings to sense-check the estimate and identify whether the market is dominated by student lets (weekly pricing) or professional lets. If the two are mixed, weight towards the professional let comparables for this property type.

### Step 4: Calculate yield and stamp duty

Call `property_yield` for the formal yield figure. Call `stamp_duty` with the asking price, defaulting `additional_property=true` — most investors already own a property. Extract total SDLT and the effective rate.

### Step 5: Check EPC

If a street address is available (not just postcode), call `property_epc`. Extract the current rating and score, potential rating, floor area in sqm, and construction age. Flag an F or G rating as below the minimum rental standard, and flag a floor area that does not match the listing as a potential wrong-certificate match.

### Step 6: Flat-specific checks

If the property is a flat or apartment, call `property_blocks` to check building-level sales history — unit volume, price trends, and any signs of bulk sales or investor exits. Also call `company_search` on the management company or freeholder name from the listing to confirm the entity is active and has no adverse filings.

### Step 7: Apply underwriting criteria

Score each signal against the thresholds in `assets/underwriting-criteria.json`. See `references/underwriting-logic.md` for decision rules, flat-specific checks, and the rationale behind conservative defaults.

You can score manually (walk through each threshold in your output) or use `scripts/compute_verdict.py` for a deterministic run. The script takes a JSON file of raw MCP data, not command-line flags.

**Exact invocation:**
```bash
# Write the collected data to a temp file (field names must match exactly)
cat > /tmp/deal-raw.json <<'EOF'
{
  "user_inputs": {"asking_price": 135000},
  "property_yield": {"gross_yield_pct": 7.56},
  "property_comps": {"median": 155000, "count": 8},
  "rightmove_search_rent": {"count": 25},
  "rightmove_listing": {"tenure": "freehold"},
  "property_epc": {"rating": "D"}
}
EOF

python3 scripts/compute_verdict.py \
  --input /tmp/deal-raw.json \
  --criteria assets/underwriting-criteria.json
```

**Required JSON field paths** (use these exact names or the script silently gets nulls):
- `user_inputs.asking_price` — integer, asking price in £
- `property_yield.gross_yield_pct` — float, e.g. 7.56 for 7.56%
- `property_comps.median` — integer, median comp price in £
- `property_comps.count` — integer, number of comp transactions
- `rightmove_search_rent.count` — integer, live rental listings found
- `rightmove_listing.tenure` — "freehold" or "leasehold"
- `rightmove_listing.annual_service_charge` — integer (leasehold only)
- `rightmove_listing.lease_remaining_years` — integer (leasehold only)
- `property_epc.rating` — string, "A" through "G"

### Step 8: Write the output

Use the template in `assets/screener-template.md`. State the decision first. Every figure in the output must come from a tool call made in this session. For BUY and WATCH decisions, include the full BTL investment scenario.

## Key Principles

- **Lead with the decision.** BUY, WATCH, or PASS — before the detail.
- **Show the working.** Every number should trace back to a data source.
- **Flag thin data.** If there are only 2 comps, say so. The decision still stands but with lower confidence.
- **Rental reality check.** Always cross-reference `rental_analysis` with actual `rightmove_search` listings. The aggregates can be misleading when student and professional lets are mixed.
- **Conservative defaults.** Additional property stamp duty, 5.5% mortgage rate, £1,500 legal fees. Better to underestimate returns than overestimate.

## Files in this skill

- `assets/underwriting-criteria.json` — thresholds for the six screening signals, editable per investor profile
- `assets/screener-template.md` — full output format with all sections
- `references/underwriting-logic.md` — decision rules, flat-specific checks, conservative defaults rationale
- `scripts/compute_verdict.py` — applies underwriting criteria to raw MCP data, returns BUY/WATCH/PASS with score (exit 0=success, 1=input error, 2=criteria missing)
