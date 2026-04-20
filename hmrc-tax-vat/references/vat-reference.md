# VAT Quick Reference

## Standard Rates (2025/26)

| Rate | % | Applies to |
|------|---|-----------|
| Standard | 20% | Most goods and services |
| Reduced | 5% | Domestic fuel, mobility aids, children's car seats, some energy-saving materials |
| Zero | 0% | Food (most), children's clothing, books/newspapers, public transport, new homes |
| Exempt | N/A | No VAT charged, no input tax recovery | Insurance, finance, education, health, postal services |

**Key distinction:** Zero-rated businesses can reclaim input VAT. Exempt businesses cannot.

## Registration Thresholds (2025/26)

| Threshold | Amount |
|-----------|--------|
| Compulsory registration | £90,000 taxable turnover (rolling 12 months) |
| Deregistration | Below £88,000 |
| Voluntary registration | Any level |

## Common Zero-Rated Supplies

- Most food and drink (exceptions: hot food, catering, crisps/confectionery, alcohol)
- Children's clothing and footwear (up to age ~14, not school uniforms with logos)
- Books, newspapers, magazines (not e-books until April 2020 — now zero-rated)
- Prescription drugs and aids for disabled people
- New build residential properties (first grant of major interest)
- Public transport (trains, buses, aircraft)
- Exported goods

## Common Reduced-Rate (5%) Supplies

- Domestic electricity and gas — confirmed by [HMRC VAT Notice 701/19](https://www.gov.uk/guidance/vat-on-fuel-and-power-notice-70119) (updated Feb 2025). **Note:** `hmrc_get_vat_rate` has no commodity mapping for domestic fuel/power and returns 20% by default. Use `hmrc_search_guidance` with "domestic fuel power VAT notice 701/19" to retrieve the authoritative guidance instead.
- Energy-saving materials (insulation, solar panels) — rules changed post-Brexit
- Children's car seats
- Contraceptive products
- Nicotine patches (stop-smoking aids)
- Renovation of properties empty 2+ years

## Common Exempt Supplies

- Insurance
- Financial services (lending, credit, shares)
- Education and vocational training
- Healthcare (by registered professionals)
- Burial and cremation
- Letting of land and buildings (unless opted to tax)

## Partial Exemption

If a business makes both taxable and exempt supplies it is "partially exempt" and can only recover a proportion of input VAT. Standard method or special method must be applied. Flag this — do not attempt to calculate it from guidance search alone.

## Option to Tax

Landlords and property owners can opt to tax commercial property, making the supply standard-rated and allowing input VAT recovery on construction/refurbishment costs. Residential property cannot be opted to tax.

## Reverse Charge

From March 2021: construction services between VAT-registered businesses use domestic reverse charge — the customer accounts for VAT, not the supplier. Affects builders, subcontractors.

## Making Tax Digital (MTD) for VAT

Mandatory for all VAT-registered businesses (above and below threshold if voluntarily registered). MTD for Income Tax Self Assessment (ITSA) — phased from April 2026 for income over £50k, April 2027 for £30k+.
