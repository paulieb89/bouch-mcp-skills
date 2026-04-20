---
name: pitch-research
description: |
  Researches a UK company you want to pitch to and drafts a credible cold
  outreach email with a specific, verifiable opening hook. Combines
  Companies House data (profile, officers, PSC, insolvency, VAT, land
  registry) with a web sweep for recent press, hires, launches, and public
  statements. Produces two outputs: a scannable research brief and a first
  draft email under 150 words. Use when the user says "help me pitch X",
  "draft a cold email to X", "research X for outreach", "I want to
  approach X about Y", "prep me to pitch X", "write an outreach email
  to X", or similar outbound prospecting requests. Requires the UK Due
  Diligence MCP server. UK companies only (non-UK targets get web-only
  research with a caveat).
license: Apache-2.0
compatibility: Requires the UK Due Diligence MCP server and WebSearch/WebFetch access.
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
  - mcp__claude_ai_uk-due-diligence__disqualified_search
  - mcp__claude_ai_uk-due-diligence__disqualified_profile
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Pitch Research

Research a UK company the user wants to pitch to, then draft a cold outreach email that could actually be sent. Two outputs: a short research brief and a first draft email that opens with a real, specific hook.

This skill exists because generic cold outreach gets binned. The only way a cold email gets read is if the opening line proves you know something real about the recipient. That "something real" has to come from a research pass. You do the pass, synthesise what matters, and write the email.

## What You Need From the User

**Required:**

1. **Target company** — name or domain. UK company.
2. **What you're pitching** — one sentence on the offering. Without this, the email is generic.

**Optional (use if provided, ask if relevant):**

3. **Contact name and role** — the specific person to address
4. **Context** — how the user found them, why they think it's a fit, any prior touch points
5. **Trigger event** — if the user already knows a recent event they want to reference

If required fields are missing, ask before doing any research. Don't start a research pass without knowing what the email is for.

## Workflow

### Step 1: Resolve and route

Start with `company_search` using the provided name. If multiple matches, pick the one whose SIC codes, status, or registered office match the user's context, or ask. If the result is clearly a charity, route to `charity_search` and `charity_profile`. If no UK match is found, try variations (Ltd vs Limited, ampersand vs "and", removing punctuation). If still nothing, ask whether the target is non-UK — if yes, explain that this skill is UK-only and offer a web-only fallback with a caveat.

### Step 2: Structural facts

Call `company_profile`, `company_officers`, and `company_psc`. Flag anything that changes the pitch: status not Active, late filings, recent director resignations, no PSC registered, or a nominee/corporate PSC that signals distance from the real owner.

### Step 2a: Is this the real decision-making unit?

Critical for UK subsidiaries of foreign parents — see `references/filing-structure-detection.md` for the full signals list and what to do when you identify a filing structure. This is often the single most valuable observation in the brief.

### Step 3: Health signals

Call `gazette_insolvency`. Call `vat_validate` only if the user has supplied a VAT number. Call `land_title_search` only if the company's business involves property or there is a reason to verify an address.

### Step 4: Optional director checks

If something in Step 2 looks concerning (recent resignations, a director with suspiciously many appointments, dissolved company history), run `disqualified_search` on named directors. Do not do this routinely — it is for when the profile raises a specific question.

### Step 5: Recent activity (the hook layer)

This is where the cold email opening comes from. Always anchor WebSearch queries to the current year and month — stale results are a real failure mode. See `references/cold-email-rules.md` for year-anchored query patterns and guidance on strong vs weak signal. WebFetch the company website homepage and any visible press or blog page. Look for launches, campaigns, senior hires, funding, or public statements in the last 90 days.

### Step 6: Person layer

If a contact name is provided, do a light public pass: WebSearch for their name plus the company, WebFetch their public LinkedIn if discoverable, and look for articles, podcasts, or press quotes. Only use what is genuinely public and verifiable. "Limited public footprint" is a true statement and useful.

### Step 7: Synthesise the brief

Target 400 words for typical targets, up to 800 for complex multi-entity structures or targets with rich recent activity and important sensitivities. The test for keeping extra words: would the user make a different decision or phrase the email differently because of this detail? Use the template in `assets/pitch-brief-template.md`. Lead with who they are and what is happening now. Never bury red flags.

### Step 8: Draft the email

Pick the single strongest hook from Step 5 or 6. Write the email around it. The opening must reference a real, specific event or fact. Then one sentence on what the user does, framed in terms of the target's situation. Then one sentence on why now. Then a single clear ask — usually a 20-minute call. Close politely. See `assets/email-format.md` for the full structure, hard rules, and good vs bad examples.

### Step 9: Run the output check

When running in Claude Code: after drafting the email but before showing it to the user, run the validation script at `scripts/check-output.py`. Exit code 0 = pass or pass with warnings (safe to show, mention warnings). Exit code 1 = fail (rewrite and run again, do not show a fail output). When running in claude.ai: follow the same rules mentally — check word count, banned words, em dashes, American spellings.

## Voice and Tone

**Use:** "figure out", "practical", "help", "have a quick look", "worth a short call", "I work with [X] on [Y]", "we produce [concrete thing]"

**Avoid:** transform, leverage, AI-powered, revolutionise, cutting-edge, 10x, disruptive, game-changing, paradigm, unlock, empower, supercharge, best-in-class, world-class, synergy

See `references/cold-email-rules.md` for em dash rules, length discipline, and the nothing-after-sign-off rule.

## Files in this skill

- `references/filing-structure-detection.md` — how to identify UK filing shells and what to do when you find one
- `references/cold-email-rules.md` — em dash discipline, length rules, contact name rules, hook layer detail
- `references/uk-dd-registers.md` — what each register tells you, what you don't have, thinking like a professional
- `references/mcp-error-handling.md` — how to handle tool failures gracefully
- `assets/pitch-brief-template.md` — full brief schema with guidance for all 8 sections
- `assets/email-format.md` — email structure, hard rules, and good vs bad output examples
