# BOUCH Skills

Free Claude skills for UK professionals — property, legal, due diligence, Primavera P6 schedules, Pine Script, and general-purpose workflow utilities.

Each skill is a SKILL.md file that tells Claude which tools to call, in what order, and how to present the results. MCP-backed skills need a server connected; standalone skills run on any Claude (claude.ai, Claude Desktop, Claude Code) without infrastructure.

![Property report output — Newcastle family homes analysis](assets/property-report-output.png)

## MCP-backed skills

Connect the MCP server, drop in the skill, go. Real data from UK registries and APIs, not AI imagination.

### Property Quick Comps
Comparable sales for any UK postcode. Median price, transaction count, price per sqft.
```json
{ "mcpServers": { "property": { "url": "https://property-shared.fly.dev/mcp" } } }
```

### Reduced Listings
Find Rightmove listings with reduced prices in a postcode — motivated-seller signal.
```json
{ "mcpServers": { "property": { "url": "https://property-shared.fly.dev/mcp" } } }
```

### Legislation Lookup
Search UK Acts of Parliament and read specific section text with in-force status and territorial extent.
```json
{ "mcpServers": { "uk-legal": { "url": "https://uk-legal-mcp.fly.dev/mcp" } } }
```

### MP Dig
Hansard contributions, registered interests, and voting record on a given UK MP.
```json
{ "mcpServers": { "uk-legal": { "url": "https://uk-legal-mcp.fly.dev/mcp" } } }
```

### BAILII Case Law
Search UK case law and retrieve judgments. Local STDIO MCP (BAILII blocks cloud IPs).
```json
{ "mcpServers": { "bailii": { "command": "python", "args": ["-m", "bailii_mcp"] } } }
```

### P6 Quick Summary
Load a Primavera P6 XER file and get activity count, status breakdown, completion percentage.
```json
{ "mcpServers": { "pyp6xer": { "url": "https://pyp6xer-mcp.fly.dev/mcp" } } }
```

### Pine Function Lookup
Look up Pine Script v6 functions with correct signatures, parameters, and usage examples.
```json
{ "mcpServers": { "pinescript": { "url": "https://pinescript-mcp.fly.dev/mcp" } } }
```

## Standalone skills (no MCP required)

These run on any Claude with no infrastructure setup. Upload and go.

### Humaniser
Strips AI writing patterns (em dashes, "certainly!", hedge phrases) from business text.

### Workflow Auditor
Finds where time actually gets lost in a repeated process. Structured scoring framework.

### Meeting Actions
Turns messy meeting notes into a structured list of actions with owners and deadlines.

### Client Prep
Turns a pile of prior notes or emails into a focused pre-meeting brief.

### AI Policy
Generates a practical UK AI acceptable-use policy covering GDPR, shadow AI, and provider rules.

## How to install

**Claude Code plugin (easiest — one command):**
```
/plugin marketplace add paulieb89/bouch-plugins
/plugin install foundations@bouch-plugins
```

**Git clone (Claude Code manual):**
```bash
git clone https://github.com/paulieb89/bouch-mcp-skills.git
cp -r bouch-mcp-skills/property-quick-comps ~/.claude/skills/
```

**Claude.ai or Claude Desktop:**
1. Settings > Customise > Add skill (or equivalent on your version)
2. Paste the SKILL.md content
3. If the skill requires an MCP server, connect it under Settings > MCP Servers

## MCP servers referenced

All servers are free, hosted on Fly.io. Source code:

- [property-shared](https://github.com/paulieb89/property-shared) — UK property data
- [uk-legal-mcp](https://github.com/paulieb89/uk-legal-mcp) — UK legal research
- [uk-due-diligence-mcp](https://github.com/paulieb89/uk-due-diligence-mcp) — Companies House + VAT + Charity + Gazette
- [bailii-mcp](https://github.com/paulieb89/bailii-mcp) — UK case law (local STDIO)
- [pyp6xer-mcp](https://github.com/paulieb89/pyp6xer-mcp) — P6 schedule analysis
- [pinescript-mcp](https://github.com/paulieb89/pinescript-mcp) — Pine Script v6 docs
- [govuk-mcp](https://github.com/paulieb89/govuk-mcp) — GOV.UK content, organisations, postcode lookup

## More skills (on bouch.dev)

Full-workflow skills that compose the above into end-to-end analyses:

- [Property Report Generator](https://bouch.dev/downloads/property-report/v1/SKILL.md) — comps, EPC, yield, stamp duty, price positioning
- [Deal Screener](https://bouch.dev/downloads/deal-screener/v1/SKILL.md) — BUY/WATCH/PASS decision with underwriting criteria
- [Rightmove Investment Finder](https://bouch.dev/downloads/rightmove-investment-finder/v1/SKILL.md) — investment analysis from a Rightmove URL
- [Property to Google Sheets](https://bouch.dev/downloads/property-to-sheets/v1/SKILL.md) — property report saved to a spreadsheet
- [Legal Research Brief](https://bouch.dev/downloads/legal-research/v1/SKILL.md) — case law, OSCOLA citations, Hansard, plain-English summary
- [Policy Briefing](https://bouch.dev/downloads/policy-briefing/v1/SKILL.md) — parliamentary landscape, key MPs, reception assessment
- [Company Check](https://bouch.dev/downloads/company-check/v1/SKILL.md) — cross-register DD (Companies House, VAT, Charity, Gazette)
- [P6 Health Check](https://bouch.dev/downloads/p6-health-check/v1/SKILL.md) — health score, critical path, float, logic quality
- [P6 Earned Value](https://bouch.dev/downloads/p6-earned-value/v1/SKILL.md) — CPI, SPI, forecasts, WBS breakdown
- [Pine Strategy Builder](https://bouch.dev/downloads/pine-strategy-builder/v1/SKILL.md) — trading idea to validated v6 code
- [HMRC Tax & VAT](https://bouch.dev/downloads/hmrc-tax-vat/v1/SKILL.md) — VAT rates, MTD status, HMRC guidance

All skills at [bouch.dev/products](https://bouch.dev/products/).

## Paid products

Free skills show you how. Paid products ship them as packaged systems:

- **BOUCH Skills Foundations** (£39 on Gumroad) — 30-page guide on writing your own skills + 10 curated worked examples + Claude Code plugin + markdown fallback
- **UK Property Investor OS** (£49) — property workflow kit launching week of 21 April
- **UK Legal Research OS** (£49) — legal workflow kit, following soon
- **UK Due Diligence OS** (£39) — DD workflow kit, following soon

## Licence

Apache 2.0
