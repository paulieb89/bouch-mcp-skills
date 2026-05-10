---
name: property-compare
description: |
  Compare up to 3 UK properties side by side — comparable sales, EPC ratings,
  rental yields, stamp duty, and a relative ranking. Use when someone shares
  2 or 3 addresses, postcodes, or Rightmove URLs and asks "which is the better
  investment?", "compare these properties", "rank these for me", or "which
  should I buy?". Produces a structured 3-column report with a clear winner.
  Requires the Property MCP server (property-shared) to be connected.
license: Apache-2.0
compatibility: Requires the BOUCH property MCP server (property-shared) and Python 3 for post-processing scripts.
metadata:
  author: bouch
  version: "1.0"
allowed-tools:
  - mcp__claude_ai_property__rightmove_listing
  - mcp__claude_ai_property__property_comps
  - mcp__claude_ai_property__property_epc
  - mcp__claude_ai_property__rental_analysis
  - mcp__claude_ai_property__rightmove_search
  - mcp__claude_ai_property__property_yield
  - mcp__claude_ai_property__stamp_duty
  - mcp__claude_ai_property__property_blocks
  - mcp__claude_ai_property__company_search
  - Bash
  - Read
  - Write
---

# Property Comparison

You compare up to 3 UK properties side by side and produce a ranked investment report. Each property gets the same data treatment — comps, EPC, rental yield, stamp duty — and the output is a structured table with a clear relative ranking and a recommended winner.

## When to Use This Skill

- "Compare these three properties for me"
- "Which of these is the better investment?" + 2–3 addresses or URLs
- "Rank these properties" + 2–3 postcodes
- "Help me choose between these" + any mix of addresses, postcodes, Rightmove links

## Input Formats Accepted

- **Street address** — e.g. "14 Elm Street, Nottingham, NG5 1AA"
- **Postcode** — e.g. "NG5 1AA"
- **Rightmove URL** — e.g. "https://www.rightmove.co.uk/properties/12345678"
- **Mixed** — each property can be a different input type; handle each appropriately

If asking prices are not given and no Rightmove URL is provided, use the area median from comps as a proxy price and flag this explicitly.

## Query Lanes

**Lane A — Full comparison** (at least one street address or Rightmove URL per property):
Tools per property: `rightmove_listing` (if URL) → `property_comps` + `property_epc` + `rental_analysis` → `property_yield` + `stamp_duty`
Output: full 9-section comparison report.

**Lane B — Postcode-only comparison** (postcodes only, no street addresses):
Tools per property: `property_comps` + `rental_analysis` → `property_yield` + `stamp_duty`
Skip `property_epc` — no reliable individual cert match. Skip BTL scenario section.
Output: area-level comparison; note that EPC data is unavailable.

**Mixed** — use Lane A rules for any property that has an address or URL; Lane B rules for postcode-only properties. Flag the asymmetry in the output.

## Step-by-Step Workflow

### Step 1: Parse inputs

Read what the user provided. For each property, determine:
- Do you have a street address? → Can call `property_epc` with address
- Do you have a Rightmove URL? → Must call `rightmove_listing` first
- Postcode only? → Skip EPC, use comps for area data

Extract postcode from any address if not explicitly given (infer from context or ask).

### Step 2: Fetch Rightmove listings (if URLs provided)

Call `rightmove_listing` for each property that has a Rightmove URL. **Run in parallel.** This gives you asking price, floor area, tenure, council tax band, key features, and days-on-market signals before you proceed.

### Step 3: Fetch comps, EPC, and rental data

For each property, run in parallel:
- `property_comps` — with address if available; always with postcode
- `property_epc` — with address (Lane A only); skip for postcode-only
- `rental_analysis` — with postcode + `purchase_price` set to asking price (or comp median if no asking price)

**Deduplication:** if two or more properties share the same postcode sector (e.g. both in NG5), the comps results will be identical. Fetch once, reuse for both. Flag this in the output.

### Step 4: Fetch yield and stamp duty

For each property, run in parallel:
- `property_yield` — postcode; pass `property_type` filter if the property type is known
- `stamp_duty` — asking price (or comp median); calculate **both** primary-residence and additional-property scenarios

### Step 5: Consolidate raw data

Save all tool outputs to `/tmp/prop-compare-raw.json` using the consolidation script:

```bash
python3 BASE_DIR/scripts/consolidate.py \
  --props '{"p1": {...}, "p2": {...}, "p3": {...}}' \
  --out /tmp/prop-compare-raw.json
```

Where each prop dict contains the raw JSON from all tools called for that property.

### Step 6: Compute comparison metrics

Run the comparison script to derive relative metrics:

```bash
python3 BASE_DIR/scripts/compute_comparison.py \
  --raw /tmp/prop-compare-raw.json \
  --criteria BASE_DIR/assets/underwriting-defaults.json \
  --out /tmp/prop-compare-metrics.json
```

This computes per-property: price premium/discount, gross/net yield, underwriting signal scores, and the overall relative ranking.

### Step 7: Render output

```bash
python3 BASE_DIR/scripts/render_comparison.py \
  --metrics /tmp/prop-compare-metrics.json \
  --template BASE_DIR/assets/compare-template.md \
  --out /tmp/prop-compare.md
```

Read `/tmp/prop-compare.md` and present to the user.

## Output Sections

Present the report in this order. Use the `assets/compare-template.md` as the structural guide.

**1. Header**
Property labels (P1 / P2 / P3), addresses, asking prices, date.

**2. At a Glance**
3-column summary table: asking price, bedrooms, EPC rating, gross yield, ranking position.

**3. Price vs Market**
Per property: asking price vs local comp median, premium/discount %, price/sqft vs area median/sqft. Flag any property priced more than 10% above comp median.

**4. Rental Market**
Per property: median rent, listing count, rent range. Note thin markets (< 5 listings). Segment student/professional lets if mixed. Normalise all rents to monthly before any calculation.

**5. Yield**
Per property: gross yield %, net yield % (30% cost deduction), `property_yield` tool figure, data confidence (listing count). Show divergence between own-calc and tool figure if > 15%.

**6. EPC**
Per property: current rating + score, potential rating, floor area, MEES risk flag.
- F or G rating → "Cannot be let in current condition (MEES)"
- D or E rating → "Below 2028 target — budget for improvements"
- C or above → "Lettable and compliant"
Flag any floor area mismatch between EPC cert and listing (> 10%).

**7. Stamp Duty**
Per property: SDLT for primary residence and additional property. Total acquisition cost estimate (price + SDLT + £2,000 fees).

**8. Underwriting Signals**
Per property: pass/fail table against thresholds from `underwriting-defaults.json`. Score each property 0–6 (one point per signal passed). Display as a column.

| Signal | P1 | P2 | P3 |
|--------|----|----|-----|
| Gross yield ≥ 5% | ✓/✗ | ✓/✗ | ✓/✗ |
| Price ≤ 10% above median | ✓/✗ | ✓/✗ | ✓/✗ |
| EPC ≥ E (lettable) | ✓/✗ | ✓/✗ | ✓/✗ |
| Comp count ≥ 3 | ✓/⚑ | ✓/⚑ | ✓/⚑ |
| Rental listings ≥ 5 | ✓/⚑ | ✓/⚑ | ✓/⚑ |
| Lease ≥ 90 yrs (if flat) | ✓/✗/N/A | ✓/✗/N/A | ✓/✗/N/A |
| **Score** | **X/6** | **X/6** | **X/6** |

⚑ = data quality flag (not a hard fail)

**9. Ranking and Recommendation**

State the ranking clearly:
- 🥇 **1st: [Property]** — [one line reason]
- 🥈 **2nd: [Property]** — [one line reason]
- 🥉 **3rd: [Property]** — [one line reason]

Then a 2–3 sentence recommendation paragraph: which property the user should focus on, what to negotiate on, and what to verify before making an offer.

## Key Rules

- **Relative ranking, not absolute verdict** — the goal is to rank the three against each other, not to apply a single BUY/WATCH/PASS. A property that would be PASS in isolation can still rank 1st if the other two are worse.
- **Parallel tool calls** — fetch all data for all properties concurrently wherever inputs allow. Do not chain calls sequentially unless the output of one feeds the next.
- **Deduplicate same-postcode calls** — if properties share a postcode sector, one `property_comps` call covers both. Reuse the result and flag it.
- **Normalise all rents to monthly** before any yield calculation.
- **Separate student and professional rental markets** if signals are present (weekly pricing, "pppw", shared houses, university proximity).
- **Flag EPC/listing floor area mismatch > 10%** — may indicate stale cert or unmeasured extension.
- **Show both primary and additional-property SDLT** — do not assume which applies; present both.
- **BTL scenario** — only include if at least one property has a known asking price and at least 3 rental listings.
- **Flat-specific extras** — for any leasehold flat, call `property_blocks` to check building trading history and `company_search` on the freeholder if named.
- British spelling throughout (analyse, colour, organised, favour).
- Round yields to one decimal place (e.g. 5.8%).
- Format EPC match rate as a percentage (e.g. 67%, not 0.67).
- Always include the disclaimer: *data analysis only — not professional valuation or investment advice.*

## Edge Cases

- **Only 2 properties given:** Run the same workflow; produce a 2-column comparison. No need to ask for a third.
- **One property is clearly dominant:** Still present all sections; don't truncate the losing properties — the user may have a reason to prefer them.
- **All three are in the same postcode:** Note that comps and rental data are identical across all three; the comparison differentiates on asking price, EPC, size, and listing-specific data only.
- **No rental listings:** Flag yield as unreliable. Do not present a yield figure without data. State "insufficient rental data — yield not calculable" and suggest a wider search radius.
- **Rightmove listing removed:** If `rightmove_listing` returns an error for a URL, note the listing is no longer active and proceed with whatever address/postcode data is available.

## What This Skill Does NOT Do

- Provide mortgage advice or affordability calculations
- Predict future prices
- Replace a RICS valuation
- Give legal advice on purchasing
- Assess structural condition

*Always include: data analysis only — not professional valuation or investment advice.*
