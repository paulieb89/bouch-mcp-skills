# Insolvency red flags — Gazette notices and what they mean

The Gazette is the UK's official public record for insolvency. Every winding-up petition, liquidation appointment, administration order, and strike-off notice is published here. A clean Gazette record for a named company is a strong signal; a hit requires reading.

## Notice codes by severity

Highest severity first. The MCP returns `severity` as a 1–10 score; this table explains what each code represents.

| Code | Name | Severity | Meaning |
|---|---|---|---|
| **2443** | Winding-Up Order | 10 | Court has ordered the company to be wound up. Terminal unless successfully appealed. Company is going out of business. |
| **2448** | Administration Order | 9 | Court-ordered administration. Directors lose control. Rescue may or may not follow. |
| **2449** | Administrative Receiver Appointed | 9 | Secured creditor (usually a bank with a floating charge pre-2003) has appointed a receiver. Company's assets are being liquidated to repay them. |
| **2456** | Creditors' Voluntary Liquidation (CVL) | 8 | Directors have called the shareholders and creditors to wind up. Company knows it cannot pay its debts. |
| **2445** / **2452** | Liquidator Appointed | 7 | Appointment step in a winding-up or CVL. |
| **2441** | Winding-Up Petition | 6 | A creditor has petitioned the court. Company has ~6 weeks to respond. If unresolved, becomes a winding-up order. **Petition itself is a FLAG** — even if dismissed. |
| **2460** | Striking-Off Notice | 5 | Registrar is proposing to strike the company off the register (non-filing or abandoned company). |
| **2455** | Voluntary Resolution to Wind Up | 4 | Members' voluntary liquidation — solvent wind-up. Business may be closing for benign reasons (retirement, group reorganisation). |
| **2450** | Moratorium | 3 | 20-day protection from creditors while restructuring is attempted. Not necessarily terminal — introduced in Corporate Insolvency and Governance Act 2020. |

## How to read a Gazette hit

1. **Check the notice date.** Recent (last 24 months) is live signal; 10 years old is history.
2. **Check the notice type.** 2443 or 2448 ever = the company went bust. 2441 within the last 5 years is the "distress" window.
3. **Check the content.** The MCP returns truncated content — for petitions, the content will name the petitioning creditor. For orders, it names the liquidator/administrator appointed.
4. **Check whether the company is still showing as Active on Companies House.** Gazette publication often precedes Companies House status change by days or weeks.

## Cross-reference with company_profile

A company showing:
- `company_status` = "active"
- But Gazette has a `2441` (winding-up petition) from last month

... is in acute distress. The Companies House status lags reality.

A company showing:
- `company_status` = "active"
- Gazette is clean
- Accounts overdue > 6 months, confirmation statement overdue

... is heading toward a `2460` strike-off notice.

## Winding-up petition: the specific flag

Winding-up petitions (2441) are public from the moment they hit the Gazette. This is the most useful DD signal the Gazette produces because:

- A petition often precedes all other Companies House changes
- It's filed by a creditor — meaning someone with standing is owed money and has gone to court
- Common petitioners: HMRC (for unpaid tax), former employees (for unpaid wages), commercial landlords, lenders
- Petition + no response from the company within ~6 weeks = winding-up order

**For lenders:** a winding-up petition within the last 5 years (even if dismissed) should usually FLAG. The company was close enough to insolvency that a creditor petitioned.

**For acquirers:** ever in history = WATCH minimum. The directors have form for running companies close to the wire.

## CVL (Creditors' Voluntary Liquidation) vs MVL (Members' Voluntary Liquidation)

These are easy to confuse:

- **CVL (2456)**: company CANNOT pay its debts. Directors call it before a creditor forces a winding-up. Effectively voluntary insolvency.
- **MVL (2455)**: company CAN pay its debts. Solvent liquidation — usually retirement, sale, or group reorganisation. Not a red flag.

Don't treat these the same. CVL is terminal distress. MVL is an orderly wind-down.

## Personal guarantee exposure

Director personal liability is triggered by:
- **Wrongful trading** (s.214 Insolvency Act 1986): continuing to trade when the director knew insolvency was inevitable.
- **Fraudulent trading** (s.213 Insolvency Act 1986): intent to defraud creditors.
- **Unlawful dividends**: paying dividends out of capital.
- **Personal guarantees signed on company debts**: banking facility, supplier credit, landlord deposit.

If a company has been through insolvency and a director is now starting a new company, check for **director disqualification** (separate reference) — unfit-conduct findings follow from these.

## The phoenix pattern

Pattern to watch:
1. Company A has winding-up order (2443)
2. Same directors form Company B shortly before or after
3. Company B trades from the same address / with the same branding / often buys the business assets at a discount
4. Company A's creditors get nothing

This is legal if:
- Directors are not disqualified
- The new company pays market value for the assets
- Creditors are notified under the Insolvency Act 1986 s.216 (name re-use restrictions)

It is illegal / unethical if the price paid is below market, or the name is re-used without notice, or disqualified directors are involved.

**To detect:** run `disqualified_search` on each named director. Run `company_officers` with `include_resigned=True` and look for overlapping incorporation dates across companies the director has been on.

## Moratorium (2450) — the newer code

Added by the Corporate Insolvency and Governance Act 2020. A 20-day protection period for directors attempting to rescue the company. NOT insolvency itself, but a signal the company needed protection. Treat as WATCH-level — directors thought it necessary.

## Scope

The Gazette covers companies registered in England & Wales, Scotland, and Northern Ireland (three separate gazettes combined by the MCP tool). LLP insolvencies, partnership insolvencies, and individual bankruptcies also appear but are NOT fetched by `gazette_insolvency` (which filters to company notices only).
