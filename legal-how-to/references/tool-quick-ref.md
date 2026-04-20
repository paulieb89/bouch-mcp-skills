# UK Legal MCP — Tool Quick Reference

All tools are available via the unified connector: `uk-business-mcp.fly.dev/mcp`

## Legislation

| Tool | What it does | Key inputs |
|------|-------------|-----------|
| `legislation_search` | Find Acts/SIs by keyword or title | `query`, optional `legislation_type` |
| `legislation_get_toc` | Table of contents for an Act | `legislation_type`, `year`, `number` |
| `legislation_get_section` | Retrieve specific section text | `legislation_type`, `year`, `number`, `section` |

**Returns:** Section text, in-force status, territorial extent, CLML source URL.

## Case Law

| Tool | What it does | Key inputs |
|------|-------------|-----------|
| `case_law_search` | Search TNA Find Case Law corpus | `query`, optional `court`, `date_from`, `date_to` |
| `case_law_grep_judgment` | Find paragraphs matching a term within one judgment | `uri` (from search result), `pattern` |

**Returns:** Neutral citations, court, date, `next_steps` hints, paragraph eIDs for drill-down.

## Citations

| Tool | What it does | Key inputs |
|------|-------------|-----------|
| `citations_parse` | Extract OSCOLA citations from free text | `text` |
| `citations_resolve` | Convert neutral citation to TNA URL | `citation` e.g. `[2017] UKSC 27` |
| `citations_network` | Map what a judgment cites + what cites it | `uri` |

## Parliament

| Tool | What it does | Key inputs |
|------|-------------|-----------|
| `parliament_search_hansard` | Search Commons/Lords debates | `query`, optional `date_from`, `date_to`, `member` |
| `parliament_vibe_check` | Quick read on how a policy/bill was received | `policy_text`, `topic` |
| `parliament_find_member` | Look up an MP or Lord by name | `name` |
| `parliament_member_debates` | Debates a specific member spoke in | `member_id` (from find_member) |
| `parliament_member_interests` | Registered interests for a member | `member_id` |

## Bills (live legislation)

| Tool | What it does | Key inputs |
|------|-------------|-----------|
| `bills_search_bills` | Search bills currently before Parliament | `query` |
| `bills_get_bill` | Full detail on a specific bill | `bill_id` |

## HMRC

| Tool | What it does | Key inputs |
|------|-------------|-----------|
| `hmrc_search_guidance` | Search published HMRC guidance on GOV.UK | `query` |
| `hmrc_get_vat_rate` | VAT liability for a supply category | `description` of the good/service |
| `hmrc_check_mtd_status` | MTD status for a VAT-registered business | `vrn` (9-digit, no GB prefix) |

## Court Codes for `case_law_search`

```
uksc        UK Supreme Court
ukpc        Privy Council
ewca/civ    Court of Appeal (Civil)
ewca/crim   Court of Appeal (Criminal)
ewhc/kb     High Court (King's Bench)
ewhc/ch     High Court (Chancery)
ewhc/comm   High Court (Commercial)
ewhc/admin  High Court (Administrative / Judicial Review)
ewhc/fam    High Court (Family)
ukut/iac    Upper Tribunal (Immigration)
ukftt/tc    First-tier Tribunal (Tax)
eat         Employment Appeal Tribunal
nica        Northern Ireland Court of Appeal
```
