# Underwriting Logic

## Underwriting Criteria

| Signal | Threshold | Fail Means |
|--------|-----------|------------|
| Gross yield | >= 5.0% | Insufficient return for BTL outside prime London |
| Price premium vs comps | <= 10.0% | Overpaying relative to comparable sales |
| Annual service charge | <= £5,000 | Running costs too high, materially erodes net yield |
| Remaining lease | >= 90 years | Lease risk affecting mortgage-ability and resale |
| Comp count | >= 3 | Thin market — median unreliable (flag, do not auto-fail) |
| Rental listing count | >= 5 | Thin rental market — flag yield confidence as low (do not auto-fail) |

## Decision Logic

- **BUY**: All thresholds met, no red flags
- **WATCH**: One threshold marginal (within 10% of limit) OR thin market data on comp count or rental listings OR one threshold failed but with a credible explanation
- **PASS**: Two or more thresholds failed

Comp count and rental listing count are data quality flags, not investment fails. A property can receive a BUY with fewer than 3 comps if all other signals are strong — but note the confidence caveat explicitly in the Recommendation section.

## Flat-Specific Checks

Leasehold properties need additional checks beyond the standard six signals. These are where deals go wrong most often and where buyers with less experience get caught.

**When to call `property_blocks`:** Always for flats and apartments. Look at:
- How many units have sold in the building in the last 3 years — a high rate of turnover can signal problems
- Price trends within the building — if the building is consistently discounted vs the postcode, find out why
- Any signs of bulk sales (many units selling in a short window) — can indicate an investor exit or major issue

**When to call `company_search`:** When the listing names a management company or freeholder. Look for:
- Is the company active and in good standing? A dormant or recently struck-off management company is a serious red flag
- When was it incorporated? A very recently formed management company can mean a right-to-manage transition (positive) or a rushed setup after problems (investigate further)
- Adverse filings — winding-up petitions, late accounts, director resignations

If the listing does not name a freeholder or management company, note the gap and flag to the investor to request this before proceeding.

## Rental Reality Check

Always cross-reference `rental_analysis` with actual `rightmove_search` listings. The aggregate figures can be misleading when student lets and professional lets are mixed in the same postcode.

Student lets typically price weekly (e.g. £120/week = £520/month) and are targeted at full-time students in HMOs. Professional lets price monthly and target working tenants. If a postcode has a large student population (university towns, city-centre postcodes near campus), `rental_analysis` may blend these groups and overstate the yield for a property that will attract professional tenants.

To separate them: look at the rightmove_search results and check whether listings are described as "student only", have per-room pricing, or are in large shared houses. Filter those out and recalculate the realistic rent for this property type.

## Conservative Defaults Rationale

The screening uses conservative defaults throughout to protect the investor from overestimating returns:

- **Additional property stamp duty** — most BTL investors already own a home, so the 3% surcharge applies. If the investor confirms this is their first property, recalculate.
- **5.5% mortgage rate** — a realistic current-market rate for a BTL mortgage at 75% LTV. Actual rates vary by lender and applicant profile.
- **£1,500 legal fees** — a reasonable estimate for a straightforward conveyance. Leasehold properties, title disputes, or shared ownership structures will cost more.
- **£500 survey** — a homebuyer's report. For older properties or those with visible defects, a full structural survey (£800-£1,200) is appropriate.

Better to underestimate returns and be pleasantly surprised than to overestimate and find the deal does not stack up post-completion.
