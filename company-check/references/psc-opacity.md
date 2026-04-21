# PSC and opacity patterns — who really controls this company

PSC (Person with Significant Control) is the UK's beneficial ownership register. Every company incorporated since 2016 must declare anyone with:
- >25% of shares, OR
- >25% of voting rights, OR
- Power to appoint/remove a majority of directors, OR
- "Significant influence or control" (a catch-all)

The register should tell you who actually owns and controls the company. In practice, it often doesn't.

## What a clean PSC record looks like

- One or two named individuals
- UK country of residence
- Full date of birth (month/year only is public, full DOB is private — that's fine)
- Notified within 14 days of incorporation or change
- Natures of control stated clearly ("ownership of shares 25-50%", "ownership of voting rights 25-50%")

A company with this profile has transparent UK ownership.

## Opacity patterns — what to flag

### 1. Nominee director (individual PSC who isn't the real owner)

Signals:
- PSC is named but is also a director of 20+ unrelated companies (check via `appointment_count` in `company_officers`)
- PSC's address is a formation-agent address shared with hundreds of other filings
- PSC's occupation is "director" (not a real job)
- PSC was "notified" on the same day as incorporation at a company-formation package

Nominees are legal in the UK (unlike some jurisdictions) but they defeat the point of the PSC register. When you see one, you're being told "someone else is the real owner, but we don't have to tell you who".

### 2. Overseas corporate PSC (a company controls a company)

Signals:
- PSC is of kind `corporate-entity-person-with-significant-control`
- `country_of_residence` or `registered_office` is overseas (Jersey, BVI, Cayman, Delaware, Hong Kong, UAE)
- Company registration numbers in opaque jurisdictions don't resolve publicly

This is where beneficial ownership actually hides. The UK PSC chain stops at the overseas entity. The MCP flag `overseas_corporate_psc_flag > 0` is a direct count of this.

### 3. Layered UK PSCs

Signals:
- PSC is a UK company (kind `corporate-entity-person-with-significant-control`)
- That UK company has its OWN PSC which is ALSO a UK company
- That company's PSC is an overseas entity

Each layer adds friction. Regulators / Financial Action Task Force (FATF) standards push for ultimate beneficial owner (UBO) disclosure. UK law only requires disclosure of the immediate layer.

### 4. "No PSC identifiable"

A legitimate filing option when nobody meets the 25% threshold. But:
- Check the shareholding. If a single individual owns >25%, the statement is false.
- Small companies sometimes use this wrongly to avoid disclosure. Cross-check with share allotment history (SH01).

### 5. Relevant Legal Entity (RLE)

A UK-registered company that itself has transparent PSC disclosure can be listed as an RLE instead of the ultimate beneficial owner. This is legitimate chain-shortening — you follow the RLE's own PSC register to find the UBO.

Not opaque if the chain terminates in identifiable UK-resident individuals within 1-2 hops. Opaque if it terminates at an offshore entity.

## How to trace a PSC chain

1. Start at the company. Run `company_psc` — get the first layer.
2. If the PSC is a UK company, note its registration number. Run `company_psc` on THAT company. Repeat.
3. If the PSC is an overseas corporate, you hit a wall. Document and stop.
4. If the PSC is an individual, you have the beneficial owner (possibly via nominee).

The MCP's `company_psc` tool exposes:
- `kind`: individual / corporate-entity / legal-person / super-secure (rare)
- `name`: full name or registered corporate name
- `notified_on`: when they were declared
- `ceased_on`: when they stopped being a PSC (if relevant)
- `natures_of_control[]`: list like `["ownership-of-shares-25-to-50-percent", "voting-rights-25-to-50-percent"]`
- `country_of_residence` (individual) or `country_registered_in` (corporate)
- `address`: correspondence address

## Specific jurisdictions and what they tell you

| Jurisdiction | Transparency | Common use |
|---|---|---|
| **Jersey** | Medium — PSC-like register since 2017, private | Holding companies, trusts, investment vehicles |
| **Guernsey** | Medium — private beneficial ownership register | Similar to Jersey |
| **Isle of Man** | Medium — central register for Manx entities | Property holding, IP licensing |
| **BVI (British Virgin Islands)** | Low — beneficial ownership search limited to regulators | Asset protection, tax-neutral holding |
| **Cayman Islands** | Low to Medium — economic substance register since 2019 | Fund structures, investment vehicles |
| **Delaware (US)** | Very low — no beneficial ownership disclosure | Tax-neutral US holding |
| **Hong Kong** | Medium — Significant Controllers Register since 2018 | Asia-Pacific holding |
| **UAE (DIFC/ADGM/mainland)** | Low to Medium — UBO register since 2021 but private | Holding, regional HQ |
| **Singapore** | Medium — register of registrable controllers since 2017 | Fintech, SE Asia HQ |

An offshore corporate PSC is not automatically suspicious. Global businesses have legitimate reasons to hold UK subsidiaries through overseas vehicles. It becomes suspicious when:

- The offshore entity is in a jurisdiction with opaque disclosure
- There's no evident business reason (no overseas trade, no international footprint)
- Layered through multiple jurisdictions
- Combined with other signals (nominee directors, mail-forward address, no employees)

## Connected people

When a PSC's name matches a director's name OR a PSC appears across multiple unrelated UK companies, you have a network. Map it by running `disqualified_search` on names and cross-referencing appointment histories. The due-diligence value is in the pattern, not any single filing.

## Scope

PSC register is a UK government record. This reference focuses on reading UK PSC filings and flagging opacity. Identifying ultimate beneficial owners in opaque offshore jurisdictions is outside scope — that requires specialist services (ICIJ Offshore Leaks, commercial UBO databases like Dun & Bradstreet, Refinitiv World-Check).
