<!-- This file is loaded by the company-check skill. It provides register descriptions and professional framing. -->

# UK Company Registers

## What the Registers Tell You

**Companies House** is the baseline. Company status, SIC codes, filing history, registered office, directors, and PSCs. If a company isn't on Companies House, it isn't a UK limited company. Use `company_search` to find by name, `company_profile` for the full record, `company_officers` for directors, `company_psc` for beneficial owners.

**The Gazette** publishes statutory notices — insolvency, winding-up, striking-off. A gazette notice is a legal event, not a rumour. If there's a winding-up petition, that's a fact. Use `gazette_insolvency` to check.

**HMRC VAT** validation confirms whether a VAT number is genuine. Useful for verifying invoices and supply chain checks. Use `vat_validate` with the number provided.

**Land Registry** shows corporate property holdings. Relevant for freeholders, property management companies, or any entity claiming to own land. Use `land_title_search`.

**Charity Commission** covers registered charities. Relevant when the entity is a charity or claims charitable status. Use `charity_search` to find, `charity_profile` for the full record.

---

## What You Don't Have

- Credit scores or payment history (Dun & Bradstreet, Experian — not in this API)
- Court judgments (County Court Judgments require a paid search)
- Beneficial ownership beyond what's declared to Companies House (PSC register is self-reported — a determined bad actor can lie)
- Trading history or revenue figures (unless filed in accounts)
- Personal credit of directors

Be clear about these gaps. The user needs to know what else to check.

---

## Thinking Like a Professional

The person asking is about to do business with this company. They might be a landlord checking a management company, a contractor vetting a client, a solicitor doing pre-transaction checks, or an investor assessing a target. They want to know:

1. **Is this company real and active?** Incorporation date, registered address, status. A company dissolved last year or in liquidation is a very different conversation.
2. **Is it well run?** Are accounts filed on time? Is the confirmation statement current? Late filings signal either negligence or distress.
3. **Who controls it?** Directors and persons with significant control (PSC) are legally mandated disclosures. A company with no PSC registered is either non-compliant or structured to obscure ownership.
4. **Are there red flags?** Gazette insolvency notices, winding-up petitions, charges registered against assets. These are public record for a reason.

Everything you present should help the user decide whether to proceed, investigate further, or walk away. A clean profile with current filings and identifiable owners is boring and good. That's the point.

---

## Reading the Patterns

Look for patterns, not just data points. Late filings alone might be sloppy admin. Late filings plus recently resigned directors plus a gazette notice is a different story. A company incorporated last month with a registered address at a mail forwarding service and no PSC is worth flagging even if technically compliant.

**Green flags:** Accounts filed on time, current confirmation statement, identifiable PSC with a UK address, SIC code matching the stated business, long trading history, no gazette notices.

**Amber flags:** Accounts slightly overdue, recent change of directors, address is a registered agent, no PSC filed but company is small and newly incorporated.

**Red flags:** Gazette winding-up or insolvency notice, multiple resigned directors in the last 12 months, accounts overdue by more than a year, no PSC when the company has been trading for years, dissolved status when the user thinks it's active.
