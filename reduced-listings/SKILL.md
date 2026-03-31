---
name: reduced-listings
description: |
  Find motivated sellers in a UK postcode. Pulls reduced Rightmove listings,
  benchmarks against Land Registry comps, and assesses motivation signals.
  Use when someone asks about reduced properties, motivated sellers, price
  drops, bargains, or who has been on the market longest.
  Requires the Property MCP server (property-shared) to be connected.
allowed-tools:
  - mcp__claude_ai_property__rightmove_search
  - mcp__claude_ai_property__rightmove_listing
  - mcp__claude_ai_property__property_comps
---

# Motivated Seller Finder

Find properties where the seller is likely to accept less than asking. Combine Rightmove listing data with Land Registry comparable sales to separate genuine opportunities from noise.

## Thinking Like an Investor

The user is hunting, not browsing. Every property you present should answer three questions:

1. **Is the seller under pressure?** Time on market, price cuts, resubmissions after collapsed chains, and restricted buyer pools all point to motivation.
2. **What is it actually worth?** The asking price is a wish. Comparable sales are the benchmark.
3. **What should I offer?** A number that reflects the seller's position, adjusted for how long they've been waiting.

Data that doesn't help the investor decide is noise. Cut it.

## What Motivation Looks Like

Not all reduced listings are motivated. A £1M house reduced by £5k is a rounding error. A £180k terrace relisted after 400 days with a collapsed chain — that's motivation.

**Strong signals:**
- **Resubmitted** — a sale fell through. The vendor has already mentally spent the money. Strongest single signal.
- **180+ days on market** — the property has been rejected at the current price. The vendor knows.
- **10%+ below comp median** — pricing to shift, or a problem property. Both worth investigating.

**Moderate signals:**
- Price reduced with 90+ days on market — tried, waited, capitulated.
- EPC F or G — below minimum rental standard. A landlord may want out.
- Lease under 80 years — below the informal mortgage threshold. Buyer pool shrinks.

**Weak signals (note but don't overweight):**
- Recently listed with "Price reduced" — could be strategic, not desperation.
- Above median but reduced — still overpriced, just less so.

## What You Have and Don't Have

**Available:** `rightmove_search` with `sort_by="most_reduced"`, `rightmove_listing` for detail (listing_update_reason, first_visible_date, tenure, lease, service charge), `property_comps` for Land Registry benchmarks.

**Not available:** Original asking price, total reduction amount, number of price cuts, withdrawn/relisted history, Zoopla data (API discontinued 2022), vendor circumstances.

Never imply you know the original price or the reduction size.

## How to Work

**Gather:** Search Rightmove with `sort_by="most_reduced"` and `max_pages=1` (25 listings is enough — quality over quantity). Fetch detail on the most promising candidates — prioritise by oldest `first_visible_date`. Pull comps once for the area benchmark. If comps return fewer than 5 transactions or `escalated_from` is set, the median is unreliable — use the Rightmove listings median as a secondary benchmark and say so.

**Analyse:** For each property, assess pressure (signals stacking), value (price vs comps as %), and offer (comp median adjusted for time and circumstances). A reasonable framework: 1% per 30 days beyond 60, capped at 15%, plus 3% for resubmissions. This is a starting point, not a valuation.

**Present:** Lead with a ranked summary table. Go deeper on the top 3 with a paragraph each connecting the signals into a narrative — not "this seller appears motivated" but "listed 491 days, resubmitted after a collapsed chain, 23% below median." End with what you can't see.

## When Things Go Wrong

- **Zero reduced listings:** The area may not have enough stock. Widen the radius or suggest adjacent postcodes.
- **Zero comps:** Use Rightmove asking prices as the benchmark and state clearly that no Land Registry data was available.
- **Thin market (under 5 comps):** Flag it. Don't pretend 2 transactions make a reliable median.
- **All listings are above median:** The "most reduced" sort returns the biggest reductions, not the cheapest properties. A £500k house in a £230k area is a different market segment — note it, don't dismiss it.

## Good vs Bad Output

**Good:** Ranks by combined signal strength. States the benchmark up front. Negotiation targets are grounded in comps and time. Detail paragraphs connect multiple signals. Limitations stated plainly. Does not reproduce raw API data.

**Bad:** Lists every property with equal weight. Claims to know the original price. Gives targets without reasoning. Generic statements. Dumps JSON in the output.

## Formatting

British spelling. Prices as £245,000. Days as whole numbers. Targets rounded to £5,000. Maximum 10 in summary, 3 in detail. Always include limitations. Always include: data analysis, not professional valuation advice.
