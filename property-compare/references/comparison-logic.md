# Comparison Logic

## Relative Ranking vs Absolute Verdict

This skill ranks properties against each other — it does **not** produce an absolute BUY/WATCH/PASS verdict for each one in isolation. A property that would PASS on a deal-screener can still rank 1st if the other two are weaker. Always frame the output as "P1 is the strongest of these three" not "P1 is a good deal".

The distinction matters because:
- The user has already chosen a short-list; they want differentiation, not a rejection of their choices
- Relative ranking surfaces the *why* — yield gap, EPC difference, price positioning
- It remains honest: if all three are weak, say "none of these are strong BTL investments but P1 is the least bad"

## Scoring (0–6 per property)

Each signal from `underwriting-defaults.json` contributes 1 point if passed:

| Signal | Pass condition |
|---|---|
| Gross yield | ≥ `min_gross_yield_pct` (default 5.0%) |
| Price vs median | Asking price ≤ comp median × (1 + `max_price_premium_pct`/100) |
| EPC lettable | Rating ≥ `min_epc_rating` (default E; if no EPC data, score as N/A — do not penalise) |
| Comp count | ≥ `min_comp_count` (default 3) — data quality flag only, treated as soft |
| Rental listings | ≥ `min_rental_listing_count` (default 5) — data quality flag only, treated as soft |
| Lease (flats only) | Years remaining ≥ `min_lease_remaining_years` (default 90); N/A for freehold |

Comp count and rental listing count are **data quality flags** — a fail here does not reduce the score in the same way. Weight them as 0.5 each. Round total score to nearest integer.

## Tie-breaking

When two properties share the same score, apply `ranking_tiebreak_priority` from the defaults JSON in order:
1. Higher gross yield wins
2. Lower price premium (or higher discount) wins
3. Higher EPC score wins
4. Higher comp count wins (more data confidence)

## When to Weight EPC More Heavily

EPC rating is a **blocking issue** for BTL investors when the rating is F or G:
- Properties cannot be legally let under MEES without an exemption
- Improvement costs can run £10,000–£30,000+
- Properties on oil heating with no gas connection face higher improvement costs

In the ranking recommendation, explicitly call this out: "P1 cannot be let in its current state and requires EPC work before generating income — this materially changes the investment timeline."

## When to Weight Yield More Heavily

Yield is the primary BTL signal when the user has expressed a cashflow goal. If the user mentions "monthly income", "cashflow", or "BTL", treat yield failures as hard fails and use the yield gap between properties as the primary ranking differentiator.

## Capital Growth vs Income Properties

Some properties will score low on yield but high on price positioning (below comp median in a desirable area). These are capital-growth cases, not yield plays. Call this out explicitly rather than ranking them last purely on yield — note: "P2 has the weakest yield but is priced 8% below comp median in a low-turnover village — better suited to a capital appreciation strategy than monthly income."

## Postcode Overlap

When two properties share the same postcode sector (first 4 characters of postcode), their `property_comps` and `rental_analysis` results will be nearly identical. In this case:
- Fetch once and reuse
- Note in the comparison: "P1 and P2 share a postcode sector — comparable sales data is the same for both; differentiation rests on asking price, EPC, and listing-specific features"

## Data Gaps

Handle missing data gracefully. Do not fail silently:
- No EPC cert found → show "No cert" in EPC column; do not score the signal; note in EPC section
- Rightmove listing removed → note listing is no longer active; proceed with address/postcode data
- No rental listings → state "insufficient rental data — yield unreliable"; do not show a yield figure
- Fewer than 3 comps → show median with a ⚑ flag; note confidence is low

## Presenting the Comparison to a Non-Investor

When the user is buying a home (not for investment), re-weight the ranking:
- Drop yield and rental signals
- Emphasise price vs market (am I overpaying?)
- Emphasise EPC running costs (annual energy cost, improvement potential)
- Emphasise stamp duty total cost difference
- Note any days-on-market signals (long listing = negotiating room)

Offer both framings if the user's intent is ambiguous.
