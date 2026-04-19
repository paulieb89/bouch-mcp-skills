# Property report — {{meta.address}}

**Postcode:** {{meta.postcode}}
**Report date:** {{meta.date}}
**Asking price (if supplied):** {{meta.asking_price_fmt}}

---

## Verdict

**{{verdict.decision}}** — {{verdict.score_pct}}% match against supplied criteria.

{{verdict.reasons_md}}

> Criteria-based scan, not a recommendation. Always verify with your own diligence before acting.

---

## Comparable sales

- **Transactions in sample:** {{comps.count}}
- **Median sale price:** {{comps.median_fmt}}
- **Mean sale price:** {{comps.mean_fmt}}
- **Range:** {{comps.min_fmt}} – {{comps.max_fmt}}
- **Median £/sqft:** {{comps.median_price_per_sqft_fmt}}
- **EPC match rate:** {{comps.epc_match_rate_pct}}%

## Energy performance (subject property)

- **Current rating:** {{epc.current_rating}}
- **Potential rating:** {{epc.potential_rating}}
- **Floor area:** {{epc.floor_area_sqm}} sqm
- **Construction age band:** {{epc.construction_age}}
- **Annual energy cost:** {{epc.annual_energy_cost_fmt}}

## Rental market (half-mile radius)

**Professional lets:** {{rental.pro_count}} listings · median {{rental.pro_median_fmt}} pcm · range {{rental.pro_min_fmt}} – {{rental.pro_max_fmt}}
**Student lets:** {{rental.student_count}} listings · median {{rental.student_median_fmt}} pcm equivalent
**Mixed market:** {{rental.mixed}}

Normalisation notes:
{{rental.notes}}

## Yield

- **Own calculation** (professional-let median, 30% cost allowance): {{yield.gross_own_pct}}% gross · {{yield.net_own_pct}}% net
- **`property_yield` tool output:** {{yield.gross_tool_pct}}% gross
- **Divergence:** {{yield.divergence_pct}}%

Yield notes:
{{yield.notes}}

## Stamp duty (England / NI)

- **As primary residence:** {{sdlt.primary_fmt}}
- **As additional property (+3% surcharge):** {{sdlt.additional_fmt}}

Scotland uses LBTT, Wales uses LTT — these figures do not apply if the postcode is SCO/WAL.

---

## What to check before offering

- Verify asking price against the median and EPC-adjusted £/sqft
- Confirm EPC floor area matches the listing size (mismatch = stale certificate, usually)
- If yield is the driver, check the professional-let segment depth, not the mixed aggregate
- Budget the 3% additional-property SDLT surcharge if BTL
- Factor an MEES reserve if EPC is D or worse — rental floor rising to C by 2028/2030

## What this report does not cover

- Mortgage affordability or interest cover
- Structural condition (survey job)
- Legal or lease review (solicitor job)
- Future price prediction

*Data analysis, not professional valuation advice. Sources: Land Registry Price Paid Data, EPC Register, Rightmove. Figures as of report date.*
