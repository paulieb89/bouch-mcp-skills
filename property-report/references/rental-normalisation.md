# Rental data normalisation — why raw aggregates mislead

Load this when rental data is central to the query, when `rental_analysis` and your own calc disagree, or when you need to explain to the user why yields vary so much.

## The problem in one line

UK rental listings mix weekly and monthly prices, professional and student lets, per-room and per-unit rates — in the same data set. A naive median of the raw list is almost always wrong.

## The normalisation script

`scripts/normalise_rents.py` does three things:

1. **Converts weekly rents to monthly** using the UK convention: `monthly = weekly × 52 / 12`.
   - So £170 per week = £737 per month, not £680.
   - Using the wrong formula (weekly × 4) undercounts rent by about 8%. That skews yield low.

2. **Separates student from professional lets** using signals:
   - Weekly pricing almost always = student
   - "student", "students", "pppw" in listing text
   - "per room" in title
   - Very low per-unit prices on multi-bed properties

3. **Flags a mixed market** when both segments are present in meaningful numbers.

## Why the `rental_analysis` MCP tool can mislead

The tool aggregates all listings in an area. In student-heavy postcodes (NG7 in Nottingham, LS6 in Leeds, M14 in Manchester, L7 in Liverpool, NE1/NE2 in Newcastle), this means:

- Median rent is dragged down by weekly student rates
- Gross yield is dragged up (lower "rent" divided into purchase price)
- The figure is meaningless for a professional-BTL investor

`compute_yield.py` uses the **professional-only median** when one is available, then flags if this differs materially from the `rental_analysis` aggregate.

## Student postcode red flags

If the comp area is any of these, student contamination is almost certain:

| Area | Postcode(s) |
|---|---|
| Nottingham (Lenton, Dunkirk, parts of Beeston) | NG7 |
| Leeds (Headingley, Hyde Park) | LS6 |
| Manchester (Fallowfield, Rusholme) | M14, M13 |
| Liverpool (Kensington, Smithdown) | L7, L15 |
| Newcastle (Jesmond, Sandyford) | NE2 |
| Sheffield (Crookes, Broomhall) | S10, S11 |
| Loughborough (town centre + north) | LE11 |

This isn't exhaustive. If a listing shows "pppw" or weekly pricing, assume student regardless of postcode.

## When to say professional vs student separately

Report both if:
- The student segment has >= 5 listings
- The student median is >15% below (weekly-normalised) the professional median
- The user asked about "rental market" (ambiguous) rather than specifically about HMO or student stock

Example output:
> 18 professional lets, median £1,050 pcm. 12 student lets, median £620 pcm per-room equivalent — meaningfully lower because of the per-room pricing model. For a standard BTL the professional figure applies.

## When NOT to split

- User asked specifically about student HMO yield
- User said they're running a student HMO
- Area is so dominated by students that splitting shows a fake "professional market" of 2 listings

In those cases, use the student median with a clear statement of the 42-week tenancy assumption.

## Common pitfalls

- **"pppw" literally means per-person-per-week.** A 4-bed at £150 pppw = £600 per week combined = £2,600 per month combined. Multiply by bed count, then convert to monthly. The scraped figure is per-person unless you do this.
- **"Rent includes all bills" on student lets** vs "tenant pays bills" on professional — the net-to-landlord position is very different. The skill can't see bills inclusion directly; flag if the listing text mentions it.
- **Shared-house versus whole-house rent.** A 4-bed HMO rented at £1,800 per whole house is a different thing from 4 rooms at £500 each = £2,000. The skill takes listings at face value; if the area is HMO-heavy, acknowledge the uncertainty.
- **Short-let listings** (Airbnb-style) occasionally pollute Rightmove. "Short-term let" or "holiday let" in the title = exclude from BTL analysis.

## If the sample is small

Below 5 professional listings, don't report a median — report the range and note the sample size. The volatility is too high to trust a single figure. Pull a wider geography if possible, or tell the user the yield read is provisional.
