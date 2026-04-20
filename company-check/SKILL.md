---
name: company-check
description: |
  Run a due diligence check on a UK company. Pulls corporate status, filing
  compliance, directors, beneficial owners, insolvency notices, and VAT
  validation from official registers. Use when someone asks "check this
  company", "is this company legit", "who owns X Ltd", "due diligence on X".
  Requires the UK Due Diligence MCP server to be connected.
license: Apache-2.0
compatibility: "Requires UK Due Diligence MCP server."
metadata:
  author: bouch
  version: "2.0"
allowed-tools:
  - mcp__claude_ai_uk-due-diligence__company_search
  - mcp__claude_ai_uk-due-diligence__company_profile
  - mcp__claude_ai_uk-due-diligence__company_officers
  - mcp__claude_ai_uk-due-diligence__company_psc
  - mcp__claude_ai_uk-due-diligence__gazette_insolvency
  - mcp__claude_ai_uk-due-diligence__vat_validate
  - mcp__claude_ai_uk-due-diligence__charity_search
  - mcp__claude_ai_uk-due-diligence__charity_profile
  - mcp__claude_ai_uk-due-diligence__land_title_search
---

# Company Check

Run a due diligence check on a UK company using official government registers. Find out if a company is real, active, compliant, and who actually controls it.

The tools here go directly to Companies House, The Gazette, HMRC VAT, Land Registry, and the Charity Commission. Every finding is from a register, not a web search. State which registers were checked and which were not.

## How to Work

**Gather.** Start with `company_search` if you have a name, or `company_profile` if you have a company number. Pull the profile first: status, filing compliance, SIC codes, registered address. Then pull officers and PSCs. If anything looks concerning — late filings, recently resigned directors, unusual SIC codes — check the Gazette for insolvency notices. If a VAT number was provided, validate it with `vat_validate`.

**Assess.** Look for patterns, not just data points. Late filings alone might be sloppy admin. Late filings plus recently resigned directors plus a Gazette notice is a different story. A company incorporated last month at a mail forwarding address with no PSC registered is worth flagging even if technically compliant at this moment.

**Present.** Lead with the headline: is this company in good standing or not? Then the detail. Do not bury red flags in the middle of a data summary.

## When Things Go Wrong

- **Company not found:** Try name variations — Ltd vs Limited, ampersand vs "and", and check for parent or subsidiary structures.
- **No PSC registered:** This is itself a flag. All active companies should have at least one PSC or a relevant legal entity registered. Note it.
- **Dissolved company:** Still useful — report when it was dissolved and whether Gazette notices preceded dissolution.
- **VAT number invalid:** Could be a typo or could be fraud. Ask the user to verify the number directly with the counterparty.

## Formatting

British spelling. Company numbers as 8-digit zero-padded (e.g. 01234567). Dates as DD Month YYYY. Directors listed with appointment date. Always state which registers were checked.

## Files in this skill

- `references/uk-registers.md` — what each register covers, its limitations, and how to read common findings
- `assets/dd-report-format.md` — output format template with good and bad examples
