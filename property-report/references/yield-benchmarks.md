# UK rental yield benchmarks — what counts as good

Load this when the user asks "is 5% a good yield?" or when the BUY/WATCH/PASS verdict needs context.

## Gross vs net — start here

**Gross yield** = annual rent ÷ purchase price × 100

Example: £12,000 annual rent on a £200,000 property = 6.0% gross.

**Net yield** = gross yield × (1 − cost allowance)

Industry default cost allowance is 30%, covering:
- Voids (1 month a year): ~8%
- Management (if used): ~10%
- Maintenance + repairs reserve: ~8%
- Insurance + accountancy: ~4%

So a 6.0% gross becomes 4.2% net on the 30% default. This is what most landlords actually bank before debt service.

This skill's `compute_yield.py` uses 30%. For a live-in landlord with no management, drop to 20%. For an HMO or high-maintenance stock, push to 35%.

## Regional benchmarks (gross yield)

Rough UK medians for a standard BTL flat or small house, observed over recent cycles. Not gospel — use as a sanity check.

| Region / area type | Typical gross | Signal |
|---|---|---|
| Zone 1–2 London | 2.5% – 4.0% | Capital play, not a yield play |
| Outer London / commuter belt | 4.0% – 5.5% | Balanced but thin net |
| Manchester, Leeds, Birmingham city centre flats | 5.5% – 7.0% | Healthy mainstream BTL |
| Liverpool, Bradford, Stoke, Sunderland | 7.0% – 10%+ | High yield, higher risk stock |
| Edinburgh, Glasgow | 5.0% – 7.5% | Scottish tenancy law changes the maths |
| Rural South | 3.5% – 5.0% | Holiday-let angles skew this |
| Student cities (to students) | 7% – 12% | HMO-only, different operational model |

**Interpretation:**
- **Under 4.0% gross** in a non-London area = flag it. Either the rent is low, the price is high, or the comp set is off.
- **Over 10% gross** = flag it. Almost always a data issue, a rough area, or an HMO/serviced unit being treated as standard BTL.

## The 6% rule of thumb (BTL in England outside London)

A conventional residential BTL investor targets **6%+ gross** in the North and Midlands. Anything below means:
- The purchase price is above local comp — re-check the asking vs median
- The rent is low — check for student contamination or outdated figures
- You're in a capital-growth area where cashflow isn't the play

The default in `assets/underwriting-defaults.json` is 6.0% gross. Change it if the client is a London cashflow-first buyer (absurd — push to PASS most deals) or a capital-growth investor (drop to 3.5%).

## Net yield reality check

A 6% gross = 4.2% net is barely above interest rates as of mid-2020s. A BTL investor using a 75% LTV mortgage at 5%+ may see negative cashflow on paper after debt service even with a "good" gross yield.

Always remind the user:
- The skill's yield is pre-mortgage, pre-tax
- Section 24 restricts mortgage interest relief for individuals (limited companies still get full relief — common workaround)
- Corporation tax on limited company BTL is usually lower than higher-rate income tax but adds admin

## Student lets — totally different maths

Student HMOs can show 8-12% gross on paper but come with:
- 42-week effective tenancy (10-month lets, 6-8 week summer void)
- Furnishing costs, bill-inclusive management, higher turnover
- Article 4 planning restrictions in many student areas (Nottingham, Manchester, Leeds, Sheffield, Liverpool, Newcastle)
- HMO licensing (mandatory for 5+ bed, additional licensing in many areas for 3-4 bed)

If the rental comp set shows student signals (weekly pricing, "pppw", "per room"), report the yield separately and note: *professional-let yield may be meaningfully lower than student-let yield in this area*.

The `normalise_rents.py` script segments these. Use the professional figure as headline.

## Short-let / holiday let

Same area, different operational model. A holiday let can show 12%+ gross in peak season but:
- 60-70% occupancy is typical
- Management costs run 15-25%, not 10%
- Council tax + business rates complications
- Planning restrictions rising (England 90-day rule in some local authorities)

This skill does NOT analyse short-let economics. If the user asks, point them to do a separate analysis with realistic occupancy assumptions. Don't blindly apply the BTL yield framework to a short-let.

## When to show the divergence

If `compute_yield.py` reports own-yield and tool-yield differ by >15%, present both and explain. Common causes:
- Different rent source (own calc uses professional-filtered listings; tool may use all listings)
- Different price source (own uses median comp; tool may use tool's internal price estimate)
- Student contamination on one side only

Never silently pick one. The user needs to know the figures aren't stable.
