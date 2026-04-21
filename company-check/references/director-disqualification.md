# Director disqualification — what it means and how to read it

A disqualification order prevents someone from acting as a director or being involved in the management of a UK company for a fixed period (2–15 years). The order lives on the public Companies House register of disqualified directors. It's one of the strongest adverse signals in UK due diligence.

## The legal framework

Governed by the Company Directors Disqualification Act 1986 (CDDA). Disqualification is ordered by:

- **The court** (s.6 CDDA 1986) after the Secretary of State's investigation of unfit conduct
- **The court** after criminal conviction for an offence connected with company management
- **Undertaking** (s.1A CDDA 1986) — the director agrees to disqualification, avoiding court. Legally equivalent to a court order.

## Length of disqualification signals severity

| Length | Category | Typical reason |
|---|---|---|
| 2–5 years | Lower bracket | Bookkeeping failures, late filing pattern, misconduct without fraud |
| 5–10 years | Middle bracket | Trading while knowingly insolvent, unpaid VAT/PAYE, misuse of company funds |
| 10–15 years | Top bracket | Fraudulent trading, repeated failures, multi-company insolvency pattern |

A 15-year order is reserved for the most serious cases — essentially a permanent ban.

## The disqualification record

`disqualified_search` returns a list of matches by name. Each match gives you:
- `officer_id` — use with `disqualified_profile` for full detail
- `title` — usually "Mr", "Mrs", "Ms", "Dr"
- `date_of_birth` — month/year only (full DOB is private)
- `snippet` — short context

`disqualified_profile` returns for each disqualification:
- `disqualified_from` — date the order started
- `disqualified_until` — date it expires
- `reason` — text of the misconduct finding (this is where the substance is)
- `company_names[]` — companies connected to the misconduct

## How to tell a real hit from a name collision

Names are not unique. Before treating a `disqualified_search` hit as a match against a director of the target company:

1. **Compare date of birth** (month/year). Close-match required.
2. **Compare name spelling and title.** "John Smith" and "Jon Smith" might be the same person — or two people.
3. **Compare associated companies.** If the disqualification order names companies the target director has been on, it's almost certainly the same person.
4. **Compare address / residence country** where available.

A hit without DOB match and no overlapping companies is probably a namesake. Don't flag it. Note it and move on.

## Disqualification vs insolvency

These are separate registers and separate findings:

- **Insolvency (Gazette)**: the company failed.
- **Disqualification (CDDA)**: the director's conduct during that failure was unfit.

Most insolvencies don't result in disqualification. When they do, it's because the Insolvency Service investigation found specific unfit conduct — not just that the company went bust.

A director who's been through multiple insolvencies without disqualification is not unfit — they may just have had bad luck, or conducted themselves properly each time.

A director who IS disqualified did something the court or the Insolvency Service considered fundamentally wrong.

## Reading the reason text

The `reason` field is verbatim from the Insolvency Service's press release or court order. Common phrasings and what they mean:

| Phrase | What it indicates |
|---|---|
| "caused X Ltd to trade to the detriment of HMRC" | Unpaid VAT, PAYE, or corporation tax — trading while unable to pay the tax bill |
| "caused X Ltd to make excessive dividend payments" | Paid shareholders out of funds that should have gone to creditors |
| "failed to cooperate with the Official Receiver" | Post-insolvency misconduct |
| "failed to maintain adequate accounting records" | Books and records failure |
| "provided false or misleading information" | Misrepresentation |
| "misappropriated company funds" | Outright theft |
| "traded while knowingly insolvent" | Wrongful trading under s.214 Insolvency Act 1986 |
| "bounce back loan" | Misuse of COVID-era emergency lending. A large and active strand of current disqualifications. |

## What "active" vs "expired" disqualification means

An active disqualification (today's date is between `disqualified_from` and `disqualified_until`) is an absolute bar on UK directorship. Any current UK directorship of a disqualified person is itself a criminal offence.

An expired disqualification is historic. The person can legally act as a director again. But for DD purposes:

- **Lender**: treat expired disqualification within 10–15 years as FLAG. The misconduct finding is permanent.
- **Acquirer**: treat expired disqualification within 15 years as FLAG.
- **Journalist**: relevant for 20+ years — the pattern is newsworthy long after the legal effect.
- **AML**: pattern-based — one expired disqualification is a WATCH, multiple or within 10 years is a FLAG.

## The cascade check

For every active director of the target company, run `disqualified_search` on their name. If a hit returns, run `disqualified_profile` for full detail and check name/DOB/companies match.

This is the single highest-value enrichment step in the whole DD workflow. A disqualified person shouldn't be on an active UK company board. If they are:

- It may be a name collision (most common)
- It may be a data lag (Companies House update pending)
- It may be a criminal offence in progress

For multi-director companies, check each. A company with 3 directors where 1 is disqualified is a FLAG regardless of the other 2.

## Sources and publication lag

Disqualification orders are published by the Insolvency Service press office, usually 1–4 weeks after the court decision or undertaking is signed. The Companies House register of disqualified directors reflects this publication. Expect a lag of up to a month between legal effect and register visibility.

## Scope

Covers UK disqualifications (CDDA 1986) for England & Wales, Scotland, and Northern Ireland. Does not cover disqualifications in other jurisdictions (Republic of Ireland has its own regime, as do Jersey/Guernsey/Isle of Man — none of which are accessible via this MCP).
