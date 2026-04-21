# Companies House filings — what they mean and what to flag

The Companies House register tells you whether a company is keeping up with its statutory obligations. Overdue filings aren't just admin laziness — they correlate with governance failure, abandoned shells, and distressed operators about to be struck off.

## The two filings that matter most

### Confirmation statement (CS01)
- Replaced the annual return in 2016
- Confirms registered address, officers, PSCs, share capital, SIC codes
- Due once every 12 months, within 14 days of the review date
- Late = £nothing in fines directly, but company gets marked "overdue" and risks striking off
- **Overdue >14 days: soft flag. Overdue >30 days: real flag. Overdue >6 months: company is likely being abandoned.**

### Annual accounts (AA02 / full statutory accounts)
- Due 9 months after year end for private companies (21 months from incorporation for first-year filers)
- Late filing triggers automatic penalties: £150 if 1 month late, £375 if up to 3 months, £750 up to 6 months, £1,500 over 6 months (doubled if late two years running)
- **Overdue >0 days: small-company admin signal. Overdue >30 days: penalties accruing. Overdue >90 days: serious distress or abandonment.**

If both the confirmation statement AND accounts are overdue, the company is in one of three states: abandoned, distressed, or being deliberately allowed to lapse (phoenix pattern — directors preparing to resurrect assets in a new entity).

## Other filings worth knowing about

| Filing | What it signals |
|---|---|
| **PSC01–PSC09** | Changes to persons with significant control. Frequent PSC changes in a small company suggest ownership instability or nominee shuffling. |
| **AP01 / AP02 / TM01 / TM02** | Director appointments and terminations. Several in short succession = board churn. |
| **AD01** | Change of registered office. Moving to a formation agent's address (1-3 Briar Close, Guildford etc.) is neutral; moving to a residential address after previously being at a commercial one is a signal. |
| **SH01 / SH02** | Allotment and return of shares. Dilution events, capital raises, or share consolidations. |
| **MR01 / MR02** | Registration of a charge (secured debt). Bulk of recent charges = company borrowing. |
| **DS01** | Application to strike off. The company is winding down voluntarily. Usually benign if no outstanding creditors; suspicious if directors are trying to escape obligations. |

## Filing-address patterns

- **Formation agent address**: neutral by default. Many SMEs use them for privacy.
- **Residential address**: common for genuine sole-trader companies. Suspicious when previously commercial.
- **Mail forwarding / virtual office**: fine for legitimate home-based businesses; combined with overseas directors and no UK employees = shell pattern.
- **Same address as 50+ other companies**: classic formation agent. Check the agent name on the filings. If it's a known incorporator (1st Formations, Your Company Formations, Complete Formations), it's routine. If it's an unbranded address with dozens of unrelated companies registered, investigate further.

## What "Active" actually means

"Active" on Companies House means the company hasn't been dissolved or struck off. It does NOT mean:
- Trading (the company may be dormant — check accounts)
- Solvent (companies in administration can still show active for weeks)
- Compliant (overdue filings don't change the "Active" status for months)

Always check `accounts.overdue`, `confirmation_statement.overdue`, and cross-reference Gazette for strike-off notices before treating "Active" as clean.

## Reading `company_profile` output

Fields that matter:

| Field | What to check |
|---|---|
| `company_status` | Active / Dissolved / Liquidation / Administration / In Administration Order |
| `date_of_creation` | Very new (< 3 months) + high-risk ask = caution |
| `sic_codes` | Mismatch between declared SIC and what the company actually does is common but worth noting |
| `accounts.overdue` / `accounts.next_due` | The headline filing flag |
| `confirmation_statement.overdue` / `confirmation_statement.next_due` | Second filing flag |
| `has_charges` | Secured debt registered — see charges register for detail |
| `registered_office_address` | Compare against VAT trading address if available |

## When filings look clean but something is wrong

- Company was incorporated 18 months ago, one confirmation statement filed, no accounts yet due. Technically clean, tells you nothing about financial health.
- Accounts filed as "dormant" for 3+ years — company hasn't traded. If someone claims it's trading, the paperwork says otherwise.
- Accounts filed "small" vs "micro" — tells you revenue band. Small-company audit exemption applies under £10.2m turnover; micro under £632k.

Clean paperwork with suspicious substance (shell director, no PSC, mail-forward address, zero trading signals) is a common shape for special-purpose vehicles, tax-shelter entities, and occasionally fraud.

## Scope of this reference

Covers England & Wales + Scotland + Northern Ireland Companies House data. Companies registered in Jersey, Guernsey, Isle of Man, or further offshore are not on Companies House — you'll see them only as PSCs of UK entities. No UK public register exposes their accounts.
