---
name: property-report
description: |
  UK property analysis: comparable sales, EPC ratings, rental yields,
  stamp duty, market context, and a BUY/WATCH/PASS verdict for a named
  address or postcode. Use to analyse a property, value a house, check
  what a place is worth, compare area prices, assess rental yield, or
  pull a full investment report. British spelling, UK stamp duty bands,
  real Land Registry and Rightmove data via the BOUCH property MCP.
license: Apache-2.0
compatibility: Requires the BOUCH property MCP server (property-shared) and Python 3 for post-processing scripts.
metadata:
  author: bouch
  version: "2.1"
allowed-tools:
  - mcp__claude_ai_prop__property_comps
  - mcp__claude_ai_prop__property_epc
  - mcp__claude_ai_prop__rental_analysis
  - mcp__claude_ai_prop__rightmove_search
  - mcp__claude_ai_prop__rightmove_listing
  - mcp__claude_ai_prop__property_yield
  - mcp__claude_ai_prop__stamp_duty
  - mcp__claude_ai_prop__property_report
  - mcp__claude_ai_prop__property_blocks
  - mcp__claude_ai_prop__company_search
  - mcp__claude_ai_prop__planning_search
  - mcp__claude_ai_strata__discover_server_categories_or_actions
  - mcp__claude_ai_strata__get_category_actions
  - mcp__claude_ai_strata__get_action_details
  - mcp__claude_ai_strata__execute_action
  - Bash
  - Read
  - Write
---

# Property Report Generator

Analyse a UK residential property or area and produce a grounded investment report: comps, EPC, rental, yield, stamp duty, market context, and a BUY/WATCH/PASS verdict.

You compose real data (Land Registry, EPC register, Rightmove) via the BOUCH property MCP, then hand the aggregated data to deterministic Python scripts for normalisation, yield maths, underwriting, and rendering. This keeps the numbers right and the output consistent.

## When to use

- "What's this property worth?" / "Analyse 14 Elm Street, NG1 5BT"
- "Are these comps for SW2 reasonable?"
- "Is this a good rental investment?"
- "Pull me a property report" / "Give me a property snapshot"
- Any request involving UK property valuation, comparison, or investment analysis

Do NOT use this skill for:
- Mortgage advice or affordability calculations
- Structural / surveyor work
- Legal advice on purchase
- Predicting future prices

## Setup — connect the MCP once

This skill depends on a UK property MCP server being connected. Two options, depending on how the user installed this skill.

**Option 1 — Plugin (recommended, bundles the MCP):**

```
/plugin marketplace add paulieb89/bouch-plugins
/plugin install foundations@bouch-plugins
```

Installs this skill plus nine others and pre-wires the Ledgerhall MCP gateway (`uk-business-mcp.fly.dev`), which fronts property, legal, and due-diligence data.

**Option 2 — MCP direct (standalone install):**

If the user installed this skill via `npx skills add paulieb89/bouch-mcp-skills` or git clone, they need to add the MCP manually:

```
claude mcp add --transport http property https://property-shared.fly.dev/mcp
```

For claude.ai and Claude Desktop, paste the same URL under Settings → MCP Servers. No API key. Free, hosted.

## Preflight — verify the MCP is live

Before running the workflow, call `property_comps` with a throwaway postcode (e.g. `SW1A 1AA`). If it returns a tool-not-found error or connection error:

1. Stop. Don't try to improvise.
2. Tell the user the property MCP isn't connected.
3. Show them Option 1 or Option 2 above depending on whether they're on Claude Code with plugin support.
4. Ask them to reconnect and retry.

If `property_comps` returns data (even empty results), proceed to the lane-selection step.

## Query Routing — Pick Your Lane

Before calling any tool, decide which lane the query fits. Don't chain every tool by default — pick the minimum set for what was asked.

**Lane A — Specific property** ("what's 14 Elm St worth?", "is this property overpriced?", any time the user named a specific house or gave a street address)

Tools: `property_comps` → `property_epc` → `rental_analysis` → `rightmove_search` → `property_yield` → `stamp_duty`

Output: full 8-section report rendered from `assets/report-template.md`. Offer Step 7 (save/share) after.

**Lane B — Area investment scan** ("should I buy in NG11 9HD?", "is this a good rental area?", "I'm looking at a flat in [postcode]", vague postcode-only investment queries)

Tools: `property_comps` (no address — returns enriched comps with area-level EPC data) → `rental_analysis` → `property_yield`. Only call `stamp_duty` when the user gives a budget. Skip `property_epc` — the comps already have EPC data attached to real sales.

Output: area overview in prose. Skip the "Property Overview" section. Emphasise "Market Context" and "Yield Estimate". Not the full 8-section template unless the user explicitly asks.

**Lane C — Quick area stat** ("typical prices in NG11 9HD?", "what EPC ratings are common here?", one-shot stat questions)

Tools: `property_comps` only. EPC enrichment gives ratings and floor area per transaction already. For a pure "what ratings are common?" question with no sales angle, `property_epc` (no address) returns the area summary directly — faster than comps for that narrow case.

Output: 2–3 sentence answer with inline stats. No headers, no sections, no disclaimer, no save offer.

Default to Lane B for vague postcode queries. Lane A requires a specific street address. Lane C for one-stat questions.

### Known tool behaviours to handle

- **Do NOT use `property_report` for investment analysis** — it's an aggregate convenience tool that blends all stock types, returns a sector-wide median regardless of `property_type`, and rejects postcode-only input. The blended median distorts every downstream calculation (yield, premium, comp discount). Always use the individual tools (`property_comps`, `property_yield`, `rental_analysis`) so you can filter by `property_type` and narrow `search_level`. Only use `property_report` for a quick area overview where like-for-like comparison isn't needed.
- **`property_comps` supports three `search_level` values — use the narrowest that returns ≥5 comps:**
  - `"postcode"` — exact postcode match only (e.g. NG7 1DB), tightest like-for-like, often 2–8 results
  - `"sector"` (default) — full sector (e.g. NG7 1), 20–50 results, risks blending distinct sub-areas (Radford vs University Park)
  - `"district"` — full district (e.g. NG7), broad, only use as fallback when sector is thin
  - Start at `"postcode"`, widen only if `count < 5`. If you widen, flag it in the output ("sector median used because postcode-only returned 3 comps").
- **Always pass `property_type` on `property_comps` and `property_yield` when you know it** (F=flat, D=detached, S=semi, T=terraced). Without the filter, a terrace investment gets benchmarked against detached housing in the same postcode. The premium/discount figure becomes meaningless.
- **Per-tool argument gotchas** (strict Pydantic validation — wrong arg names fail silently-looking with "missing required argument"):
  - `ppd_transactions` — uses `from_date` + `to_date` (ISO strings), **not** `months`. For a 24-month window: `from_date="2024-04-21", to_date="2026-04-21"`.
  - `rightmove_listing` — `property_id` must be the **full Rightmove URL string** (e.g. `"https://www.rightmove.co.uk/properties/165078146"`), not the bare integer ID. Prefer `listing://{id}` resource read where available.
  - `company_search` — arg name is `query` (e.g. `"nottingham city homes"`), **not** `name`.
- **`property_yield` with `property_type` filter can return null rent** if there are too few type-matched rental listings. If the filtered call returns `"median_monthly_rent": null`, retry without the type filter and use the blended sector result, noting the fallback in the output.
- **`property_epc` requires `postcode`** — `postcode` is a required argument; `address` is optional and refines the match. Calling with `address` only (e.g. `address="39 Havenwood Rise, NG11 9HD"`) throws a `missing_argument` validation error. Always pass both: `postcode="NG11 9HD", address="39 Havenwood Rise"`. If the returned certificate's floor area or property type doesn't match the listing, flag as a potential wrong-certificate match — do not treat a mismatched EPC as ground truth.
- **`rightmove_search` rent radius** — the default radius is narrow (often 0.25mi). For `property_type=rent` in suburban / low-density postcodes this routinely returns 0 listings. Start rent queries at `radius=1` (one mile) and narrow only if flooded. Sale queries can stay at default — for-sale stock is denser.
- **Blended `property_comps`** — a sector-level median without a `property_type` filter blends all stock (flats, semis, detacheds). When the listing is a specific type, always filter (`property_type=T` for terraced, etc.) so the premium/discount calculation is like-for-like. Call out the blended baseline if you could not filter.
- **Ignore `yield_assessment`** if the tool returns it as null — deprecated field.

## Workflow (Lane A — the full report)

### Step 1 — Gather

Call the MCP tools in this order, in parallel where dependencies allow:

1. `property_comps` with `postcode` + `property_type` filter + `search_level="postcode"` (tightest). If `count < 5`, retry with `search_level="sector"`; flag the widening in the output. Do NOT skip the type filter when you know the type. Extract median price — this feeds later steps.
2. `property_epc` with `postcode` (required) + `address` (optional, refines the match): `postcode="NG11 9HD", address="39 Havenwood Rise"`. Returns current + potential rating, floor area, annual costs.
3. `rental_analysis` with the postcode AND `purchase_price=<median from Step 1>` to populate gross yield.
4. `rightmove_search` with `property_type="rent"` and `radius=1` for actual listings (rental_analysis aggregates can be misleading — see `references/rental-normalisation.md`). Default radius is ~0.25mi which often returns zero in low-density postcodes — start at 1 mile and narrow only if results flood.
5. `property_yield` with the postcode (same `property_type` filter as Step 1 if used).
6. `stamp_duty` with the median price. If primary residence not specified, compute both (additional_property=true and =false).
7. `rightmove_search` with `channel=BUY` for current-market context.

Collect all responses into a single JSON object keyed by tool name. Save to `/tmp/property-report-raw.json`.

### Step 2 — Normalise

Run the rental normaliser:

```bash
python scripts/normalise_rents.py --input /tmp/property-report-raw.json --output /tmp/property-report-rental.json
```

This converts weekly rents to monthly, separates student from professional lets, and flags if the market is dominated by one segment. Read `references/rental-normalisation.md` if you need to understand why this matters.

### Step 3 — Yield

```bash
python scripts/compute_yield.py --input /tmp/property-report-raw.json --rental /tmp/property-report-rental.json --output /tmp/property-report-yield.json
```

Returns gross yield, net yield (after 30% cost allowance), and comparison against the property_yield tool's own output. If they diverge materially, both are reported.

### Step 4 — Underwrite

```bash
python scripts/underwrite.py --input /tmp/property-report-raw.json --yield /tmp/property-report-yield.json --criteria assets/underwriting-defaults.json --output /tmp/property-report-verdict.json
```

Returns `{decision: BUY|WATCH|PASS, score, reasons[]}`. The defaults in `assets/underwriting-defaults.json` are for a standard UK BTL investor. To apply a client's own criteria, copy the JSON, edit thresholds, and pass it via `--criteria`.

### Step 5 — Render

```bash
python scripts/render_report.py --raw /tmp/property-report-raw.json --rental /tmp/property-report-rental.json --yield /tmp/property-report-yield.json --verdict /tmp/property-report-verdict.json --template assets/report-template.md --output /tmp/property-report.md
```

Read the resulting markdown, sanity-check for obvious data issues (see Step 6), then present it to the user.

### Step 6 — Sanity check

Before presenting, spot-check:
- EPC floor area vs listing size (if mismatched, flag — see `references/epc-nuance.md`)
- Comp transaction count (<5 = thin market, say so)
- Rental sample — if student lets dominate, say professional-let yield may not apply
- Stamp duty — is the user a first-time buyer, primary-residence buyer, or additional-property buyer? If unspecified, show both. Flag non-UK residency if relevant (adds 2% on top).

### Step 7 — Present + offer save

Present the rendered report. The report output should include:

**5. Stamp Duty** section must show:
- SDLT as primary residence
- SDLT with 5% additional-property surcharge (BTL / second home default)
- If buyer is non-UK resident: add further 2% on top of surcharge (7% total above standard rates)
- Total acquisition cost estimate (price + SDLT + ~£2,000 conveyancing + ~£500 searches)
- If buying as primary replacement home: flag the 36-month surcharge refund entitlement

After presenting, ask:

> "Want me to save this to a Google Sheet or draft an email with the summary?"

Do not save without asking.

**Google Sheets:** Call `discover_server_categories_or_actions` with `server_names: ["google sheets"]`, then `get_category_actions` for GOOGLE_SHEETS_SPREADSHEET, then `execute_action` with server_name "google sheets", category_name "GOOGLE_SHEETS_SPREADSHEET", action_name "google_sheets_create_spreadsheet". Pass a `body_schema` with `title` and `data` (JSON mapping row numbers to {column: value}).

Layout: Row 1 = title, Rows 3–9 = comps, Rows 11–14 = rental, Rows 16–18 = yield, Rows 20–23 = stamp duty, Rows 25–28 = EPC, Row 30+ = individual comps. Column A = labels, B = values, C = source.

**Email:** Call `execute_action` with server_name "gmail", category_name "GMAIL_EMAIL", action_name "gmail_draft_email". Pass `body_schema` with `to` (ask the user), `subject` ("Property Report — [Address] — [Date]"), and `body` (key insights + summary + spreadsheet link if created).

If saving both: spreadsheet first, then email with the link.

## Workflow (Lane B — area scan)

Skip `property_epc`, `stamp_duty`, and the full render. Do Steps 1 (subset), 2, 3. Present as prose, emphasise yield and market context. Offer Step 7 save only if the user seems serious about the area.

## Workflow (Lane C — quick stat)

One MCP call, one inline answer. Example: "Median sale price in NG11 9HD over the last 24 months is £182k across 38 transactions. Mostly 3-bed semis (EPC D typical)."

## Flat-specific extras (optional)

For leasehold flats, three extra MCP tools are useful:
- `property_blocks` — other units trading in the same building. Useful for spotting block investor exits or bulk sales.
- `company_search` — freeholder / management company on Companies House. Check for adverse filings when service charges are high or management is in question.
- `planning_search` — nearby development affecting value or views. More relevant in city-centre locations.

Only call these if the property is a flat AND the context warrants it.

## Output rules

- British spelling (analyse, colour, organised)
- £245,000 not 245000; round yields to 1dp (e.g. 5.8%)
- Format `epc_match_rate` as a whole percentage (e.g. 67%, not 0.6666)
- Normalise ALL rents to monthly before any calculations
- Separate student and professional rental markets — never blend them
- Always state data source + date range for comps
- If data is missing, say so — do not guess
- Do not speculate on future prices
- Flag thin comp samples (<5 transactions)
- Always include the disclaimer: *data analysis, not professional valuation advice*

## Files in this skill

- `scripts/normalise_rents.py` — weekly→monthly, student/pro separation
- `scripts/compute_yield.py` — gross/net yield with explicit assumptions
- `scripts/underwrite.py` — BUY/WATCH/PASS against criteria JSON
- `scripts/render_report.py` — fills the template with all gathered data
- `references/epc-nuance.md` — EPC grades, MEES, retrofit context
- `references/stamp-duty-2026.md` — current SDLT bands, surcharges, FTB relief
- `references/yield-benchmarks.md` — what counts as a good yield by UK region
- `references/rental-normalisation.md` — why rental_analysis can mislead
- `assets/report-template.md` — the BOUCH-voice report shell
- `assets/underwriting-defaults.json` — default thresholds (editable per client)

## What this skill does NOT do

- Mortgage advice or affordability
- RICS-grade valuation
- Legal conveyancing advice
- Structural condition
- Future price prediction

Always include: *this is data analysis, not professional valuation advice*.
