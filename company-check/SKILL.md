---
name: company-check
description: |
  Run a full due diligence check on a UK company or director. Cross-references
  Companies House, Gazette insolvency, HMRC VAT, and the Disqualified Directors
  register, then scores against a configurable risk profile (lender, journalist,
  acquirer, AML, or your own). Produces a CLEAR / WATCH / FLAG verdict with
  weighted reasons. Use when someone asks "check this company", "due diligence
  on X", "is this company legit", "who owns X Ltd", "is this director
  disqualified". Requires the UK Due Diligence MCP server.
license: Apache-2.0
compatibility: "Requires UK Due Diligence MCP server."
metadata:
  author: bouch
  version: "3.0"
allowed-tools:
  - mcp__claude_ai_uk-due-diligence__company_search
  - mcp__claude_ai_uk-due-diligence__company_profile
  - mcp__claude_ai_uk-due-diligence__company_officers
  - mcp__claude_ai_uk-due-diligence__company_psc
  - mcp__claude_ai_uk-due-diligence__gazette_insolvency
  - mcp__claude_ai_uk-due-diligence__vat_validate
  - mcp__claude_ai_uk-due-diligence__disqualified_search
  - mcp__claude_ai_uk-due-diligence__disqualified_profile
  - mcp__claude_ai_uk-due-diligence__charity_search
  - mcp__claude_ai_uk-due-diligence__charity_profile
  - mcp__claude_ai_uk-due-diligence__land_title_search
  - Bash
  - Read
  - Write
---

# Company Check — UK Due Diligence

Run a full due diligence check on a UK company or director using official government registers. The skill wraps the UK Due Diligence MCP in a deterministic pipeline: gather → enrich → score → report. Every verdict is traceable to the underlying register data, and the risk profile is a swappable JSON file (lender, journalist, acquirer, AML, or your own) so the same check produces the right answer for the right audience.

Data sources:

- Companies House (profile, officers, PSCs, filings)
- Companies House Register of Disqualified Directors
- The Gazette (insolvency notices: winding-up, administration, CVL, strike-off)
- HMRC VAT validation
- HM Land Registry (for asset checks, when relevant)

What this skill does NOT do: sanctions / PEP screening, credit scoring, trade references, forensic accounting, or legal advice. It supports those workflows; it does not replace them.

## Setup

This skill depends on the UK Due Diligence MCP. Verify connection:

```
Call company_profile with company_number "00445790" (Tesco PLC).
```

You should get a full profile back in ~2 seconds. If not, the MCP isn't connected — fix that before proceeding.

## Lane decision — pick one before calling any tool

**Lane A — Full DD (default).** User supplies a company name or number and a use case (or you infer the profile from context). Run the full pipeline: all MCP calls, risk scoring, rendered report. Takes 60–120 seconds end-to-end. This is the value case.

**Lane B — Quick lookup.** User wants a one-paragraph answer: "is Acme Ltd legit?" Skip enrichment and scoring. Run `company_profile` + `gazette_insolvency` + (if available) one `disqualified_search` on the first director. Return a single paragraph.

**Lane C — Director check only.** User gives a person's name, not a company. Run `disqualified_search`, then `disqualified_profile` on any hits. Optionally (if the name suggests an MP/Lord), offer to run `parliament_member_interests` via the legal-research skill. Return disqualification history, not a company report.

Always state which lane you're in at the start of your response so the user can redirect.

## Lane A workflow — full DD

### Step 1. Gather

If the user gave a name, resolve it to a company number first with `company_search`. Take the top match; ask the user to confirm if ambiguous.

Call these tools in parallel where possible, and save the combined response to `/tmp/dd-raw.json`:

1. `company_profile(company_number)` — status, filings, address, SIC codes, charges flag
2. `company_officers(company_number, include_resigned=true)` — active + resigned officers, appointment counts
3. `company_psc(company_number)` — beneficial ownership chain
4. `gazette_insolvency(entity_name=company_name)` — insolvency notices
5. `vat_validate(vat_number)` — only if a VAT number was supplied or appears in the profile

Then for each active director from step 2, call:

6. `disqualified_search(query=director_name)` — for each active director

For any disqualified search result that returns hits, call `disqualified_profile(officer_id)`.

Structure the combined JSON with top-level keys matching the tool names:

```json
{
  "user_inputs": {"company_number": "...", "use_case": "lender"},
  "company_profile": {...},
  "company_officers": {...},
  "company_psc": {...},
  "gazette_insolvency": {...},
  "vat_validate": {...},
  "disqualified_lookups": {
    "jane smith": {...disqualified_search result keyed by lowercased name...},
    "john doe": {...}
  },
  "disqualified_profiles": {
    "officer_id_1": {...disqualified_profile result...}
  }
}
```

Use the Write tool (or Bash with heredoc) to save this to `/tmp/dd-raw.json`.

### Step 2. Enrich

```bash
python scripts/cross_reference.py \
  --input /tmp/dd-raw.json \
  --output /tmp/dd-enriched.json
```

This computes: officer churn, high-appointment-count officers (nominee flags), overseas corporate PSC count, missing UBO flag, filing overdue days, insolvency signals by severity, VAT address match.

### Step 3. Score against the chosen criteria profile

Pick the right criteria file for the user's context:

| Use case | Criteria file |
|---|---|
| Lender, invoice finance, credit, property finance | `assets/dd-criteria-lender.json` |
| Investigative journalism, beneficial ownership tracing | `assets/dd-criteria-journalist.json` |
| M&A, acquisitions, strategic investment | `assets/dd-criteria-acquirer.json` |
| KYB onboarding, AML compliance, counterparty screening | `assets/dd-criteria-aml.json` |
| Unclear / default | `assets/dd-criteria-defaults.json` |

If the user wants custom thresholds, copy a preset, edit it (see notes in the `_notes` field), and pass the path.

```bash
python scripts/risk_score.py \
  --enriched /tmp/dd-enriched.json \
  --raw /tmp/dd-raw.json \
  --criteria assets/dd-criteria-lender.json \
  --output /tmp/dd-verdict.json
```

Output is `CLEAR`, `WATCH`, or `FLAG` with a weighted score percentage and per-check reasons.

### Step 4. Render

```bash
python scripts/render_check.py \
  --raw /tmp/dd-raw.json \
  --enriched /tmp/dd-enriched.json \
  --verdict /tmp/dd-verdict.json \
  --template assets/dd-report-template.md \
  --output /tmp/dd-report.md
```

### Step 5. Sanity gate

Before presenting, spot-check:

- Every `FLAG` reason has a specific pointer (a Gazette notice, an officer name, a filing date). No vague "risk" language.
- If disqualification returned a hit, confirm the match is real (date of birth or company-name overlap), not a namesake.
- If the verdict is `CLEAR` but the user described a high-risk scenario (recent insolvency elsewhere, known bad actor), flag the tension — the scan missed something the user knows.

### Step 6. Present and offer follow-on

Present the rendered markdown. Offer:

- Run the same data against a different profile: "want to see how this reads for an acquirer instead?"
- Pull the Land Registry for any properties owned by the company: `land_title_search`
- For charities: `charity_profile` if relevant
- Pull connected-officer companies: for any flagged director, run `company_search` on them to surface other active directorships

## Lane B workflow — quick lookup

1. `company_profile(company_number or company_search first result)`
2. `gazette_insolvency(entity_name=company_name, start_date=24 months ago)`
3. Optional: `disqualified_search(first_director_name)` if profile returns officers; skip if time-pressed

Return one paragraph:

> Acme Widgets Ltd (12345678) is an **active private limited company**, incorporated March 2018, with **accounts currently 62 days overdue**. No Gazette insolvency notices in the last 24 months. No disqualification hits on the named director. Verdict: low-risk with a filing-discipline caveat.

Do NOT run the full pipeline for Lane B. It's a one-paragraph answer.

## Lane C workflow — director check

1. `disqualified_search(person_name)`
2. For each hit, `disqualified_profile(officer_id)`
3. For each profile, check date of birth and company list against what the user told you
4. Report matches and mismatches separately

Example output:

> **John Smith** — 3 matches on the disqualified register, 1 of which appears to be the same person based on company overlap (Acme Ltd, Widget Co Ltd). That person was disqualified from 2019-03-15 to 2027-03-15 for causing Acme Ltd to trade to the detriment of HMRC. Two other "John Smith" matches are namesakes (different DOB, unrelated companies).

If user adds context ("John Smith the MP for Anytown"), consider whether legal-research skill's parliament tools are a better fit.

## Configurable thresholds — the user-preference design

The six preset criteria JSONs in `assets/` differ on these axes:

- **Filing discipline weight**: lenders care most (weight 3), journalists barely (0)
- **Appointment-count threshold**: journalists set it to 5 (surface nominees), lenders/AML use 10–15
- **PSC opacity weight**: AML cares most (weight 3), others 1–2
- **Disqualification history window**: journalists 20 years, acquirers 15, default 10
- **Insolvency block windows**: lenders 60 months on petitions, AML 24 months, journalists treat as history only
- **VAT address discrepancy**: AML blocks on it, others watch only

Users can edit any of these thresholds and re-run `risk_score.py` with their custom file. Same data, different verdict, different reasoning — the judgment is externalised in the JSON, not baked into the scripts.

## Formatting rules

British spelling throughout. Company numbers as 8-digit zero-padded (`01234567`). Dates as `YYYY-MM-DD` in tables, `D Month YYYY` in prose. Director names with their residence country when overseas. Always state which registers were checked AND which were not (see "What was NOT checked" in the template).

Never assert something the registers don't support:

- Don't infer revenue from VAT registration
- Don't infer trading activity from "Active" company status (could be dormant)
- Don't infer solvency from absence of Gazette notices alone (notices lag events by weeks)
- Don't call a person disqualified without a date-of-birth or company-name match

## When things go wrong

- **Company not found**: try name variations (Ltd ↔ Limited, ampersand ↔ "and"). Check for parent/subsidiary structures. Ask user to confirm trading name vs legal name.
- **Multiple matches on company_search**: present the top 3 with company numbers and status, ask user to pick.
- **No PSC registered**: this is itself a flag for a company incorporated post-2016. Include in report.
- **Dissolved company**: still useful — report dissolution date and whether Gazette notices preceded it.
- **VAT number invalid**: could be typo or fraud. Recommend user verify the number directly with the counterparty before escalating.
- **Disqualified_search returns 50+ hits on a common name**: filter by DOB or matched companies; report unique persons only.
- **MCP timeout or 5xx**: note the failure in the report under "What was NOT checked" and continue with what you have.

## Files in this skill

- `scripts/cross_reference.py` — enrich raw data with derived signals (churn, overseas %, disqualification matches)
- `scripts/risk_score.py` — score against criteria JSON, produce CLEAR/WATCH/FLAG verdict
- `scripts/render_check.py` — fill report template with raw + enriched + verdict data
- `references/companies-house-filings.md` — CS01/AA02 meaning, overdue signals, filing-address patterns
- `references/insolvency-red-flags.md` — Gazette codes by severity, winding-up vs CVL, phoenix patterns
- `references/psc-opacity.md` — nominee detection, overseas PSCs, UBO tracing
- `references/director-disqualification.md` — CDDA 1986, length-by-severity, match confidence
- `references/vat-and-mtd.md` — VAT validation signals, MTD April 2026, address discrepancy meaning
- `assets/dd-criteria-defaults.json` — balanced default thresholds
- `assets/dd-criteria-lender.json` — lender preset (strict filings, charges, insolvency windows)
- `assets/dd-criteria-journalist.json` — investigative preset (PSC opacity weighted, broad history window)
- `assets/dd-criteria-acquirer.json` — M&A preset (strictest across all categories)
- `assets/dd-criteria-aml.json` — AML preset (ownership transparency + VAT validity)
- `assets/dd-report-template.md` — markdown template with `{{dotted.path}}` placeholders
- `references/uk-registers.md` — legacy v2 reference, retained for compatibility
- `assets/dd-report-format.md` — legacy v2 template, retained for compatibility

## Scope

UK companies registered in England & Wales, Scotland, or Northern Ireland. Overseas companies appear only as PSCs of UK entities — their own filings are not accessible via this skill. No real-time sanctions or PEP screening. No credit scoring or Creditsafe-style predictive risk. No trade references or management interviews. Report is a scan, not an audit.
