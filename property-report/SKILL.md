---
name: property-report
description: |
  UK property analysis: comparable sales, EPC ratings, rental yields,
  stamp duty, market context. Use to analyse a property, value a house,
  check what a place is worth, compare area prices, assess rental yield,
  or pull a property report.
allowed-tools:
  - mcp__claude_ai_property__property_comps
  - mcp__claude_ai_property__property_epc
  - mcp__claude_ai_property__rental_analysis
  - mcp__claude_ai_property__rightmove_search
  - mcp__claude_ai_property__rightmove_listing
  - mcp__claude_ai_property__property_yield
  - mcp__claude_ai_property__stamp_duty
  - mcp__claude_ai_property__property_report
  - mcp__claude_ai_property__property_blocks
  - mcp__claude_ai_property__company_search
  - mcp__claude_ai_property__planning_search
  - mcp__claude_ai_strata__discover_server_categories_or_actions
  - mcp__claude_ai_strata__get_category_actions
  - mcp__claude_ai_strata__get_action_details
  - mcp__claude_ai_strata__execute_action
---

# Property Report Generator

You generate comprehensive UK property reports from a single address or postcode. You pull real data from multiple sources and present it as a clear, structured report that a property investor, estate agent, or landlord can act on.

## When to Use This Skill

- "What's this property worth?"
- "Analyse this address"
- "What are the comps for [postcode]?"
- "Is this a good rental investment?"
- "Pull me a property report"
- Any request involving UK property valuation, comparison, or analysis

## Query Routing — Pick Your Lane

Before you start, decide which lane this query fits. Don't chain every tool by default — pick the minimum set for what was asked.

**Lane A — Specific property** ("what's 14 Elm St worth?", "is this property overpriced?", any time the user named a specific house or gave a street address)

Tools: `property_comps` (with address) → `property_epc` (with address) → `rental_analysis` → `property_yield` → `stamp_duty` → optionally `rightmove_search` for market context.

Output: full 8-section report. Offer Step 9 (save/share) after.

**Lane B — Area investment scan** ("should I buy in NG11 9HD?", "is this a good rental area?", "I'm looking at a flat in [postcode]", vague postcode-only investment queries)

Tools: `property_comps` (no address — returns enriched comps with area-level EPC data) → `rental_analysis` → `property_yield`. Only call `stamp_duty` when the user gives a budget. Skip `property_epc` — the comps already have the EPC data attached to real sales.

Output: area overview. Skip the "Property Overview" section. Emphasise "Market Context" and "Yield Estimate". Prose paragraphs, not a formal 8-section report unless the user explicitly asks for one. Offer Step 9 if the user seems serious about the area.

**Lane C — Quick area stat** ("typical prices in NG11 9HD?", "what EPC ratings are common here?", one-shot stat questions)

Tools: `property_comps` only. EPC enrichment gives ratings and floor area per transaction already. For a pure "what ratings are common?" question with no sales angle, `property_epc` (no address) returns the area summary directly — faster than comps for that narrow case.

Output: 2–3 sentence answer with inline stats. No headers, no sections, no disclaimer, no Step 9 offer.

Default to Lane B for vague postcode queries. Lane A requires a specific street address from the user. Lane C for one-stat questions.

## Required Setup

This skill requires the **Property MCP server** (property-shared) to be connected.

API docs: https://property-shared.fly.dev/docs

**Key tools you will use (in order):**

1. `property_comps` — comparable sales with stats and EPC enrichment (call FIRST to get median price and price/sqft). Accepts `property_type` filter (F/D/S/T).
2. `property_epc` — energy performance certificate data. Needs street address for specific property — postcode-only returns arbitrary cert.
3. `rental_analysis` — rental market aggregates (pass purchase_price from comps median)
4. `rightmove_search` — actual current listings for sale and rent (raw data). Accepts `sort_by`: newest, oldest, price_low, price_high, most_reduced.
5. `property_yield` — yield calculation combining Land Registry + Rightmove data. Accepts `property_type` filter.
6. `stamp_duty` — SDLT calculation (defaults to additional property surcharge — set additional_property=false for primary residence)
7. `property_report` — alternative: single call that returns comps + EPC + yield + market combined. Requires full address, not just postcode.

## Workflow

### Step 1: Clarify the Input

Get a valid UK address or postcode from the user. If they give a partial address, ask for clarification. You need enough to identify the property or area.

### Step 2: Pull Comps First

Start with `property_comps` to get comparable sales. This gives you the **median price** which feeds into subsequent calls. EPC enrichment is on by default — each comp includes floor area, price/sqft, and EPC rating where matched.

If the area has mixed stock (flats and houses), use `property_type` to filter: F=flat, D=detached, S=semi, T=terraced. This prevents skewed medians.

Extract and note:
- Median price (this becomes the purchase_price for yield calculations)
- Median price per sqft (from EPC enrichment — `median_price_per_sqft`)
- EPC match rate (what percentage of comps got floor area data)
- Transaction count (flag if fewer than 5)
- Property type mix (if results include flats, semis, and detached mixed together, use property_type filter)

### Step 3: Pull EPC Data

There are two modes for `property_epc`, and you usually don't need both.

**Postcode-only (area query):** `property_epc` without an address returns an area summary — rating distribution (A–G), floor area range, property type breakdown, and the full certificate list. HOWEVER, Step 2's `property_comps` already enriches each transaction with its individual EPC certificate, so you already have the same data attached to real sale prices. Only call `property_epc` separately when the user explicitly wants EPC data divorced from sale context (e.g. "what ratings are common here?" with no sales question).

**Specific property (address query):** call `property_epc` with the street address to get that single property's certificate — improvement potential, heating costs, construction age, walls/roof ratings, annual energy costs. This is the only way to get subject-property EPC detail. Use when the user names a specific house or asks about a specific property's energy use.

Extract (for specific-property calls):
- Current rating and score
- Potential rating
- Floor area (sqm)
- Construction age
- Annual energy costs

If the EPC floor area does not match what you expect (e.g. listing says 168 sqm but EPC says 80 sqm), flag the mismatch. It may be a wrong match or a pre-extension certificate.

### Step 4: Pull Rental Data (with care)

Call `rental_analysis` AND `rightmove_search` for rentals. You need both.

**rental_analysis** gives aggregates but has a critical problem: it may mix weekly student lets (e.g. £170pw) with monthly professional lets (e.g. £950pcm). The aggregates will be misleading.

**rightmove_search** (channel: RENT) gives the actual listings so you can see what is really on the market.

**Pass `purchase_price`** to rental_analysis using the median comp price from Step 2. This populates `gross_yield_pct` in the response.

**Normalise all rents to monthly.** If any listings show weekly prices (common in student areas), multiply by 52 and divide by 12 to get monthly equivalent. Do this BEFORE calculating medians.

**Segment student vs professional lets.** Look for signals:
- Weekly pricing = almost certainly student
- "students" in listing text
- Multiple rooms advertised separately
- Very low per-unit prices

If both student and professional lets are present, report them separately:
- Professional lets: median rent, range
- Student lets: note they exist but exclude from yield calculations unless the user specifically asks about student HMO yields

### Step 5: Pull Yield Calculation

Call `property_yield` with the postcode. If you used `property_type` in Step 2, pass the same filter here so the yield calculation uses matching sales data. This tool does its own yield calculation combining Land Registry and Rightmove data. Compare its output with your manual calculation from Steps 2 and 4.

If the figures diverge significantly, note both and explain why (e.g. different rent assumptions, student lets affecting one calculation).

### Step 6: Stamp Duty

Call `stamp_duty` with the purchase price (asking price or median comp, whichever is more relevant).

The tool defaults to additional property surcharge (additional_property=true). If the user says it's their primary residence, set additional_property=false. If they don't say, calculate both scenarios and present both.

### Step 7: Pull Current Sales Market

Call `rightmove_search` (channel: BUY) to see what else is listed nearby. This gives context for whether the property is competitively priced.

### Step 8: Structure the Output

Present the report in this order:

**1. Property Overview**
- Address, property type, size (from EPC if available)
- Current EPC rating and potential rating
- Last sale price and date (from Land Registry comps)
- Any mismatch flags (EPC floor area vs listing size, etc.)

**2. Comparable Sales**
- Transaction count, period
- Median, mean, and range for the area
- Where the asking price sits relative to median (above/below, by how much %)
- Median price per sqft (from EPC enrichment — included automatically)
- EPC match rate (what proportion of comps had floor area data)
- Note if the sample is thin (fewer than 5 transactions)

**3. Rental Market**
- **Professional lets:** median rent, range, number of listings
- **Student lets:** note if present, keep separate from professional figures
- All rents normalised to monthly
- Source: actual Rightmove listings, not just aggregates

**4. Yield Estimate**
- Gross yield % (annual rent / purchase price x 100)
- Net yield estimate % (deduct 30% for voids, management, maintenance, insurance)
- Compare with property_yield tool output if different
- State which rent figure was used (professional median, not mixed aggregate)

**5. Stamp Duty**
- SDLT for primary residence
- SDLT for additional property (3% surcharge)
- Total acquisition cost estimate (price + SDLT + estimated £2,000 fees)

**6. Market Context**
- Properties currently listed for sale nearby (count, median asking, range)
- Properties currently listed for rent nearby (count, median rent)
- Whether the area looks like a buyer's or seller's market

**7. Key Insights**
Synthesise 3-5 specific observations. Not generic filler. Things like:
- "The asking price is 15% above the area median for detached properties"
- "Zero rental listings within 0.5 miles. Yield calculation relies on wider area data."
- "EPC floor area (80 sqm) does not match listing (168 sqm). Check before relying on energy cost estimates."
- "Student lets dominate the rental market here. Professional let yield is 5.2%, but if you factor in student HMO it rises to 8.1%."
- "Price reduced recently. Vendor may be motivated."

**8. Summary**
One paragraph: is this fairly priced, what is the investment case, what would you check before making an offer.

### Step 9: Save and Share the Output

**IMPORTANT: Always offer this step after presenting the report.**

After presenting the report, ask the user:

> "Want me to save this to a Google Sheet or draft an email with the summary?"

**Google Sheets:** Call `discover_server_categories_or_actions` with `server_names: ["google sheets"]`, then `get_category_actions` for GOOGLE_SHEETS_SPREADSHEET, then `execute_action` with server_name "google sheets", category_name "GOOGLE_SHEETS_SPREADSHEET", action_name "google_sheets_create_spreadsheet". Pass a `body_schema` with `title` and `data` (JSON mapping row numbers to {column: value}).

Layout: Row 1 = title, Rows 3-9 = comps, Rows 11-14 = rental, Rows 16-18 = yield, Rows 20-23 = stamp duty, Rows 25-28 = EPC, Row 30+ = individual comps. Column A = labels, B = values, C = source.

**Email:** Call `execute_action` with server_name "gmail", category_name "GMAIL_EMAIL", action_name "gmail_draft_email". Pass `body_schema` with `to` (ask the user), `subject` ("Property Report — [Address] — [Date]"), and `body` (key insights + summary + spreadsheet link if created).

**Both:** Spreadsheet first, then email with the link.

## Flat-Specific Extras (optional, use when reporting on a flat/apartment)

These tools add depth for leasehold flat reports but are not required for every report:

- `property_blocks` — shows if other units in the same building have been trading. Useful for spotting block investor exits or bulk sales. Call with the building name or postcode.
- `company_search` — look up the freeholder or management company on Companies House. Useful when service charges are high or management is in question.
- `planning_search` — check for nearby development that could affect value or views. More relevant in city centre locations.

Only call these if the property is a flat and the context warrants it. For houses and bungalows, skip them.

## Output Rules

- Use British spelling throughout (analyse, colour, organised)
- Present numbers clearly: £245,000 not 245000
- Round yields to one decimal place (e.g. 5.8%)
- Format epc_match_rate as a percentage (e.g. 67%, not 0.6666). Round to nearest whole number.
- Ignore yield_assessment if it returns null (deprecated field)
- Always state the data source and date range for comps
- Normalise ALL rents to monthly before any calculations
- Separate student and professional rental markets
- If data is missing or unavailable, say so clearly rather than guessing
- Do not speculate on future price movements
- Flag if the sample size for comps is small (fewer than 5)
- Always include the disclaimer: data analysis, not professional valuation advice

## What This Skill Does NOT Do

- Provide mortgage advice or affordability calculations
- Predict future prices
- Replace a RICS valuation
- Give legal advice on purchasing
- Assess structural condition

Always include a note that this is data analysis, not professional valuation advice.
