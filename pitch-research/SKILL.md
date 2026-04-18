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

Research a UK company the user wants to pitch to, then draft a cold outreach email that could actually be sent. You produce two things: a short research brief, and a first draft email that opens with a real, specific hook.

This skill exists because generic cold outreach gets binned. The only way a cold email gets read is if the opening line proves you know something real about the recipient. That "something real" has to come from a research pass. You do the pass, synthesise what matters, and write the email.

## Example invocations

This skill activates on requests like:

- "Help me pitch [studio] for the [product] marketing campaign"
- "Draft a cold email to [company] about [service]"
- "Research [company] for outreach and draft a first email"
- "I want to approach [company] — can you prep me?"
- "Write an outbound email to [person] at [company]"
- "Prep me to pitch [company] for [thing]"

If the user hasn't said what they're pitching, ask before doing any research. The email is generic without it.

## Thinking Like a Professional

The person using this skill is about to send a cold email to someone who has never heard of them. They have maybe ten seconds of attention before the recipient decides to read on or delete. The opening line is where it lives or dies.

What makes an opening line land:

1. **A specific, verifiable reference.** "I saw your team announced the Birmingham warehouse move last Thursday" beats "I noticed your company is growing" every time. One is a fact the recipient recognises. The other is a guess.
2. **Relevance, not flattery.** Don't tell them they're impressive. Tell them why your reason for writing is tied to something they are actually dealing with right now.
3. **A reason this email exists.** Why are you writing now rather than last month? Trigger events (hires, launches, campaigns, press, funding) give the email a reason to exist at this moment.
4. **One clear ask.** A 20-minute call. A quick look at their current setup. Not three options. Not a menu.

Your job is to find the real reference, explain what matters about it, and hand the user a brief and a draft email they can send with light edits — not rewrite from scratch.

## What the Registers Tell You

**Companies House** gives you the structural facts: legal name, company number, SIC codes, registered office, status, incorporation date, director and PSC lists, filing compliance. This is the spine. If a company is dissolved, in liquidation, or has no PSC registered, that's context you need before drafting anything.

**The Gazette** publishes statutory notices including winding-up petitions, insolvency, and striking-off. A company with a current gazette notice is a different conversation. You may not want to pitch at all, or you may want to reference the situation tactfully.

**HMRC VAT** validates VAT numbers. Occasionally useful if the user is pitching to an entity whose legitimacy they want to sanity-check before investing time.

**Land Registry** shows corporate property holdings. Relevant if the target's business involves property, or if you want to confirm they actually occupy an address they claim.

**Charity Commission** covers registered charities. If the target is a charity, route here for governance, financials, and trustees.

**Disqualified directors register** shows individuals banned from acting as directors. Useful on the director layer if something looks off, but don't search routinely.

The web layer — recent press, hiring, product launches, campaigns, public statements — is where the outreach hook usually lives. Companies House tells you who they are. The web tells you what they're doing this week.

## What You Don't Have

- Credit scores, payment history, or trading risk (paid services like D&B, Experian)
- Private email addresses or phone numbers
- Internal org charts
- Revenue or margin data unless it's filed in accounts
- Private LinkedIn content (only public profile information via WebFetch)
- Non-UK company data (this skill is UK-only — if the target is incorporated elsewhere, say so and offer web-only research)

Be clear about gaps. Don't invent data to fill them. A brief that says "no PSC registered, worth asking about" is more useful than one that pads with speculation.

## What You Need From the User

**Required:**

1. **Target company** — name or domain. UK company.
2. **What you're pitching** — one sentence on the offering. Without this, the email is generic. Example: "We produce youth-culture marketing content and want to pitch them on a campaign for their upcoming game release."

**Optional (use if provided, ask if relevant):**

3. **Contact name and role** — the specific person to address the email to
4. **Context** — how the user found them, why they think it's a fit, any prior touch points
5. **Trigger event** — if the user already knows a recent event they want to reference, capture it and prioritise it

If required fields are missing, ask for them before doing any research. Don't start a research pass without knowing what the email is for.

## How to Work

### Step 1: Resolve and route

Start with `company_search` using the provided name. If multiple matches, pick the one whose SIC codes, status, or registered office match the user's context, or ask which one.

If the result is clearly a charity (charitable incorporated organisation, or a company limited by guarantee with charitable objects), route to `charity_search` and `charity_profile` instead of the company tools.

If no UK match is found — try common variations (Ltd vs Limited, ampersand vs "and", dropping "the", removing punctuation). If still nothing, ask the user if the target is non-UK. If yes, explain that this skill is UK-only but offer to do web-only research for a brief and email, with a caveat that the structural data won't be there.

### Step 2: Structural facts

Call `company_profile` for status, filing history, SIC codes, registered office, incorporation date. Call `company_officers` and `company_psc`. You need to know who runs it and who controls it.

Flag anything that changes the pitch:
- Status not Active
- Late accounts or confirmation statement
- Recent director resignations
- No PSC registered
- Nominee or corporate PSC (signals distance from the real owner)

### Step 2a: Is this the real decision-making unit?

**This is critical for UK subsidiaries of foreign parents.** The legal entity your user wants to pitch may just be a filing structure with no operational marketing function. Sending a cold email to the UK address when decisions sit with the US or EU parent is the fastest way to get ignored.

Check for filing-structure indicators:

- **Shared central registered office.** Addresses like `7 Savoy Court, London WC2R 0EX` or `100 Bishopsgate` or similar City/Westminster corporate services addresses host dozens of unrelated subsidiaries. If the registered office is one of these, the UK entity is almost certainly a filing structure.
- **PSC is a foreign holding company.** If `company_psc` returns a corporate PSC that is itself a subsidiary of a foreign parent (look for Delaware LLCs, Cayman-incorporated entities, or named US/EU parent corporations), the decision-making sits abroad.
- **SIC code vs operational reality.** A company registered as "other software publishing" but whose actual studio, product, or brand activity clearly happens elsewhere (different city, different country) is a filing entity for a foreign operation.
- **Employee count vs public presence.** If the entity files micro-entity accounts (tiny headcount) but the brand is globally famous, the operational mass is elsewhere.

If you identify a filing structure:

1. Still produce the brief for the UK entity (the user asked for it and the Companies House data is useful context).
2. In the **Person notes** section, lead with: "Decision-making is NOT at this UK entity. Target the parent's marketing organisation instead: [likely location and role]. The UK entity appears to be a filing structure for [parent name]."
3. In the **Watch out for** section, add: "Do not address the email to the UK subsidiary's office. It will not reach the right person."
4. When you draft the email in Step 8, address it to the parent's likely marketing contact, not anyone at the UK entity.

This is often the single most valuable observation in the brief. A cold email routed to the wrong entity is worse than no email at all.

### Step 3: Health signals

- `gazette_insolvency` on the company — if there's a recent winding-up, CVL, or striking-off notice, this is a red flag
- `vat_validate` only if the user has supplied a VAT number to check
- `land_title_search` only if the company's business involves property or the user has reason to verify an address

### Step 4: Optional director checks

If something in step 2 looks concerning (recent resignations, a director with suspiciously many appointments, a dissolved company history), run `disqualified_search` on named directors. Don't do this routinely — it's for when the profile raises a specific question.

### Step 5: Recent activity (the hook layer)

This is where the cold email opening comes from.

**Always anchor WebSearch queries to the current year and month.** Stale results are a real failure mode, especially for tech, media, and gaming targets where 2024 and 2025 content still ranks well. Without a year anchor, you will get old material that looks current and embed wrong facts in the brief.

Use the current date as you start the skill. For example, if today is April 2026:

- `"[company name]" news 2026`
- `"[company name]" April 2026` or `"[company name]" "last month"`
- `"[company name]" hiring 2026` or `"[company name]" jobs 2026`
- `"[company name]" launch 2026` or `"[company name]" announcement 2026`
- `"[company name]" [CEO name if known] 2026`
- `"[company name]" campaign 2026` (if relevant to what the user is pitching)

If a query returns clearly old results (2023, 2024, early 2025), reject them and try again with a more specific time window. Do not include old results in the brief as if they were recent.

WebFetch the company website homepage and any visible press or blog page. Pull the three most recent items and check their dates before using them as hooks.

Look specifically for:
- A launch, campaign, or product announcement in the last 90 days
- A new senior hire (particularly in the area the pitch targets)
- A public statement, conference talk, or podcast appearance by the contact
- Any news item directly relevant to the user's offering
- Funding, acquisition, partnership

The best hook is something specific, recent, and tied to what the user is pitching.

### Step 6: Person layer (only if contact name provided)

If the user has given a specific contact, do a light public pass:

- WebSearch for their name plus the company
- WebFetch their public LinkedIn if discoverable (public profile only, no login, no private content)
- Look for public statements: articles they've written, podcasts, conference talks, press quotes

Only use what is genuinely public and verifiable. Do not invent biography. If you can't find much, say so — "limited public footprint" is a true statement and useful.

### Step 7: Synthesise the brief

Produce a scannable brief. Target 400 words for typical targets — up to 800 for complex ones where genuine strategic insights emerge (large multi-entity structures, rich recent activity, important sensitivities the user must know about before pitching). The test for keeping extra words: would the user make a different decision or phrase the email differently because of this detail? If yes, keep it. If no, cut it.

Lead with who they are and what's happening now. Never bury red flags. See the Output format section below.

### Step 8: Draft the email

Pick the single strongest hook from step 5 or 6. Write the email around it.

The opening line must reference a real, specific event or fact. Not "I saw your company is doing well." Instead: "Saw the announcement about the Bristol studio opening last week" or "Read your piece on creator economics in The Drum".

Then one sentence on what the user does, framed in terms of the target's situation.

Then one sentence on why now.

Then a single clear ask — usually a 20-minute call.

Close politely. No sign-off theatrics.

**Length discipline:**

Target 110-130 words. Hard cap 150. Aim low and leave headroom. If your draft comes in at 140+, you are almost certainly padding — cut the adjectives, tighten the opening, drop any sentence that doesn't either reference a real event or make a single clear ask. It is much easier to pass the check at 115 than to negotiate yourself down from 152.

**Em dash discipline:**

ZERO em dashes anywhere inside the email block. That includes the subject line, the opening, the middle, the ask, and the sign-off. Use commas, full stops, or parentheses instead.

The brief above the email uses em dashes freely (fine — they're allowed in the brief). This makes them very easy to leak into the email unconsciously because you have just written several. **Before running the check, actively scan the email for em dashes.** Search visually for the `—` character. If you find one, replace it before running the script.

**Nothing after the sign-off:**

The email block ends at the signature name. That means:

- No italic notes like `*[Need to identify the right contact]*` after the sign-off
- No "Word count: 123" annotations
- No `[Your name]` placeholder instructions
- No PostScript lines that are really guidance, not email copy

If you need to flag contact-identification guidance or any other meta-note, put it in the brief's **Person notes** section, not inside or after the email block. The brief is for the user; the email is the deliverable.

**If no contact name is known:**

Open with `Hi [name],` as a literal placeholder — the brackets tell the user to fill it in. In the brief's **Person notes** section, add a one-line note naming the likely role the email should go to (e.g. "Target: VP of the relevant function — search LinkedIn for the parent company name + that function"). Do NOT guess the contact from web search. A wrong name is worse than `[name]`.

### Step 9: Run the output check

**When running in Claude Code (not claude.ai):** After drafting the email but before showing it to the user, run the validation script:

```bash
python3 scripts/check-output.py <(echo "$BRIEF_AND_EMAIL_TEXT")
```

Or save the output to a temp file and pass the path. The script checks:
- Email word count (must be under 150)
- Banned marketing words (anywhere in output, but especially in email)
- Em dashes in the email (banned in Bouch copy)
- American spellings (British required, warnings only)

**Exit codes:**
- 0 = PASS or PASS WITH WARNINGS (safe to show user, mention warnings if any)
- 1 = FAIL (fix before showing user)
- 2 = script error (email section could not be parsed — check your output structure)

If the script returns FAIL, rewrite the failing elements and run again. Do not show the user a FAIL output. If it returns PASS WITH WARNINGS, show the user and mention what you warned on so they can decide.

**When running in claude.ai (script not available):** Follow the same rules mentally. Check the email against the banned word list in the Voice and Tone section. Count the email words. Look for em dashes. Catch American spellings.

## Voice and Tone (Email Output)

Match the Bouch house voice. Grounded, no-nonsense, no marketing gloss.

**Use:** "figure out", "practical", "help", "have a quick look", "worth a short call", "I work with [X] on [Y]", "we produce [concrete thing]"

**Avoid:** transform, leverage, AI-powered, revolutionise, cutting-edge, 10x, disruptive, game-changing, paradigm, unlock, empower, supercharge, best-in-class, world-class, synergy.

**Em dashes: ZERO inside the email block.** This is a hard rule, including the subject line. Em dashes are fine in the brief (use them freely) but the brief is for the user and the email is the deliverable — it is very easy to leak them from one to the other unconsciously. Scan the email visually for `—` before running the check.

**British spelling throughout.** Colour not color. Organisation not organization. Recognise not recognize.

Write like a tradesperson who knows their craft, not an agency deck.

## Output Format

Always produce both parts. Never skip the email because the brief is "enough."

### Brief

```
## Pitch Brief: [Company Name]

### Snapshot
[2-3 lines: what they do, approximate size, location, company status, who runs it]

### Recent signals
- [3-5 bullets from the web pass: hires, campaigns, launches, press, public statements, funding]

### Who controls it
[Key director(s) and PSC, anything notable. One or two lines.]

### Health check
[Filing status, any gazette notices, disqualified director flags, or "Clean — active company, filings current, no red flags."]

### Person notes
[Only if contact name was provided. 3-4 lines, public info only. Skip section if no contact.]

### Hooks for outreach
- [3-5 specific things that could open a cold email, in rough order of strength]

### Watch out for
- [Red flags, sensitivities, recent problems, things NOT to mention. Almost always populate this section — even structurally clean companies have operational sensitivities: communication style, decision locus, incumbent relationships, timing constraints, areas that would read as amateurish or uninformed. Only omit if you genuinely cannot identify anything, which is rare.]

### Sources checked
[One line: "Companies House, Gazette, web pass (DATE)." Be explicit about what was and wasn't used.]
```

### Email

```
**Subject:** [specific, references the hook — NO em dashes]

Hi [name],

[Opening line: one real, specific reference to a recent event or fact]

[One sentence on what you do, framed in terms of their situation]

[One sentence on why this is relevant to them right now]

[Single clear ask, usually a 20-minute call at a specific time window]

[Sign-off],
[Sender first name]
```

**Hard rules on the email block:**

- Target 110-130 words. Hard cap 150.
- Zero em dashes anywhere — subject line, body, sign-off, all of it.
- Nothing after the sign-off name. No annotations, no word count lines, no `[Your name]` placeholders, no meta-notes. The email block ends at the signature.
- If you need to flag anything for the user (wrong contact, timing concern, edit suggestion), put it in the brief's **Person notes** or **Watch out for** section.

After you draft the email, run the validation script (see Step 9). Do not report a word count in the email block itself — the script reports it.

## When Things Go Wrong

### User-facing issues

- **Company not found:** Try variations of the name. Ltd vs Limited, ampersand vs "and", check for parent/subsidiary structures. If still nothing, ask the user to confirm spelling or provide a company number.
- **Non-UK company:** Explain the skill is UK-only. Offer to do web-only research for a brief and email, with a caveat that the structural data won't be there.
- **Dissolved or in liquidation:** Stop and flag it prominently. The user may not want to pitch at all. Ask before continuing.
- **No recent web activity:** Write the brief honestly. "No recent public activity in the last 90 days — the hook will need to come from context the user already has." Don't fabricate an event.
- **Contact name not findable:** Proceed with the company brief. In the email, default to a generic greeting or ask the user for a better contact.
- **Red flags during research:** Surface them immediately, don't bury them in the output. If the company is in trouble, the user needs to know before they decide to pitch.

### MCP tool failures

The uk-due-diligence MCP can return errors for individual tools without taking the whole server down. Handle these gracefully:

- **One tool fails, others work:** Continue the workflow with what you have. Note the gap in the brief's "Sources checked" section. For example: "Companies House profile and PSC retrieved. Officers API unavailable (server error) — director list not verified."
- **Never fabricate to fill a gap.** If officers data is missing, don't invent directors from web search alone. Say it's missing.
- **Transient errors:** If a tool fails on first call, try once more before giving up. If the first error is a 5xx from the upstream API (application-layer, e.g. 500 "API request failed") and the retry returns a 502 from the proxy (transport-layer), that's a mixed failure — try once more before giving up. Three attempts is the hard ceiling. Never retry beyond three.
- **Whole server unreachable:** Tell the user the UK Due Diligence MCP appears to be disconnected, and offer to fall back to web-only research with a clear caveat.
- **Critical gaps for the brief:** If you lost company_profile entirely, you don't have enough structural data to proceed. Tell the user and stop.

The goal is partial output with honest gaps, not a clean-looking brief that invented what it couldn't retrieve.

## Good vs Bad Output

**Good:**
- Email opens with a specific, verifiable event
- Brief lists real signals with dates
- Hooks are ranked by relevance to what the user is pitching
- Health check flags are clear and upfront
- Email is under 150 words, one clear ask
- Voice matches Bouch house style

**Bad:**
- Email opens with "I noticed your company..." or "I've been following your work..."
- Brief is padded with generic sector commentary
- Hooks are vague ("they're growing", "they care about innovation")
- Red flags are buried mid-brief
- Email is 300 words with three asks
- Uses any banned word from the voice rules

## Formatting

British spelling. Company numbers as 8-digit zero-padded (e.g. 01234567). Dates as DD Month YYYY. SIC codes with short descriptions. Directors listed with appointment date if relevant to the hook. Always state which registers were checked and which were not. Word count the email at the bottom.
