# UK Stamp Duty Land Tax — 2026 bands

Load this reference when computing SDLT manually, sanity-checking the `stamp_duty` MCP tool's output, or when the user asks about first-time-buyer relief, additional-property surcharge, or non-resident surcharge.

Regulations differ by UK nation. These bands are **England and Northern Ireland only**. For Scotland (LBTT) and Wales (LTT), see the notes at the bottom.

## Core SDLT bands — primary residence

Rates applied in slices to the portion of the price in each band.

| Portion of price | Rate |
|---|---|
| Up to £250,000 | 0% |
| £250,001 – £925,000 | 5% |
| £925,001 – £1,500,000 | 10% |
| Over £1,500,000 | 12% |

Example — £500,000 primary residence:
- First £250,000 × 0% = £0
- Next £250,000 × 5% = £12,500
- **SDLT = £12,500**

## Additional property surcharge (5% on top)

For second homes, buy-to-let, or any additional residential property, add **5% to every band**. Applies if the buyer will own more than one residential property worth £40,000 or more after completion. This includes properties owned anywhere in the world — a flat in Spain still triggers it.

Companies purchasing residential property also pay the 5% surcharge.

| Portion of price | Additional-property rate |
|---|---|
| Up to £250,000 | 5% |
| £250,001 – £925,000 | 10% |
| £925,001 – £1,500,000 | 15% |
| Over £1,500,000 | 17% |

Example — £500,000 additional property:
- First £250,000 × 5% = £12,500
- Next £250,000 × 10% = £25,000
- **SDLT = £37,500** (vs £12,500 primary — the surcharge adds £25,000)

Rule of thumb for BTL: additional-property SDLT is roughly 3× primary SDLT on typical 2–3 bed stock.

**Main residence replacement:** if the buyer is selling their previous main home, the 5% surcharge does not apply. If they complete on the new property before selling the old one, the surcharge is charged upfront but is **refundable within 36 months** of selling the original home. Worth flagging — many buyers miss it.

## First-time buyer relief (primary residence only)

Higher nil-rate band and reduced rate for first-time buyers, but only where the purchase price is **£500,000 or less**.

| Portion of price | FTB rate |
|---|---|
| Up to £425,000 | 0% |
| £425,001 – £625,000 | 5% |

If the price exceeds £500,000, **the whole relief is lost** — standard rates apply as if not a first-time buyer.

Example — £450,000 FTB purchase:
- First £425,000 × 0% = £0
- Next £25,000 × 5% = £1,250
- **SDLT = £1,250** (vs £10,000 at standard rates — saves £8,750)

## Non-resident surcharge (2% on top)

If the buyer is non-UK resident for SDLT purposes (separate test from general UK tax residence), **add 2% to every band**. Stacks with the additional-property surcharge.

So a non-resident buying an additional property pays standard + 5% + 2% = +7% on each band.

## Total acquisition cost estimate

When reporting to a user, don't report SDLT alone. Estimate:

```
Acquisition cost = Purchase price
                 + SDLT
                 + ~£2,000 conveyancing fees
                 + ~£500 searches
                 + (if BTL) ~£500 mortgage arrangement + ~£400 valuation
```

Round up. The £2-3k band of ancillary costs is usually material to a deal and people forget it.

## Scotland and Wales (flag if relevant)

If the postcode is Scottish (EH, DD, AB, IV, PA, G, etc.) or Welsh (CF, SA, LL, NP, LD, SY — though Wales also shares SY with Shropshire, check), SDLT does NOT apply. Instead:

- **Scotland: LBTT** (Land and Buildings Transaction Tax) — different bands, different Additional Dwelling Supplement (ADS, currently 6%). Direct the user to Revenue Scotland's calculator.
- **Wales: LTT** (Land Transaction Tax) — different bands, different surcharge. Direct the user to the Welsh Revenue Authority calculator.

The `stamp_duty` MCP tool handles all three when given a postcode. If it returned an SDLT figure for a Scottish or Welsh postcode, that's a tool bug — flag it to the user and re-run with the correct country.

## Gotchas to mention

- **5% surcharge applies if you own ANY other residential property worth £40,000+ anywhere in the world**, not just in the UK. A flat in Spain still triggers it.
- **Uninhabitable property**: there's a niche argument that commercial SDLT rates apply to derelict or converted property. Uncommon — flag but don't apply without professional advice.
- **Mixed-use** (e.g. shop with flat above): commercial rates apply to the whole lot. Much lower at the top band. Worth mentioning if the property has a commercial element.
- **Main residence replacement**: if the buyer is replacing their main home, the 5% surcharge is refundable within 36 months of completion. Worth flagging — many buyers miss it.

## What to hand the user

Always present both:
1. **SDLT as primary residence** (if they didn't say)
2. **SDLT with additional-property surcharge** (if they might be a second-home or BTL buyer)

If the user specified, only show that one. Always state which you assumed.
