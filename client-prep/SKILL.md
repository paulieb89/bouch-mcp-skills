---
name: client-prep
description: |
  Research a company or person before a meeting, call, or pitch.
  Pulls Companies House data, LinkedIn context, sector background,
  and recent news. Use when someone says "I have a meeting with X",
  "research this company", "prep me for a call", or "what should I
  know about X before we meet".
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - WebFetch
  - WebSearch
---

# Client Prep

You research a company or person before a business meeting and produce a structured brief the user can review in 5 minutes.

## When to Use This Skill

- "I have a meeting with [company] tomorrow"
- "Research [company] for me"
- "What should I know about [person/company] before this call?"
- "Prep me for a pitch to [company]"
- "Pull background on [company]"

## What You Need From the User

1. **Company name** (required)
2. **Person name and role** (if known)
3. **Purpose of the meeting** (sales, partnership, interview, follow-up)
4. **Any context** (how they found you, what they've asked about, industry)

If the user just gives a company name, start with that and ask about the rest after the research.

## Workflow

### Step 1: Company Basics

Search for the company. Gather:
- What they do (one sentence)
- Size (employees, revenue if public)
- Location(s)
- Founded / how long they've been operating
- Key people (CEO, founder, relevant contact)

**Sources:** Companies House (if UK, use `company_search` MCP tool if available), company website via WebFetch, WebSearch for recent coverage.

### Step 2: Recent Activity

Search for recent news, blog posts, press releases, job listings:
- Have they raised funding recently?
- Are they hiring? (Signals growth or gaps)
- Any recent product launches, partnerships, or changes?
- Any public problems or complaints?

**Sources:** WebSearch for "[company name] news", "[company name] hiring", check their blog/news page.

### Step 3: Sector Context

Brief sector overview relevant to the meeting:
- What is happening in their industry right now?
- Are they in a growing, stable, or declining sector?
- Who are their main competitors?
- Any regulatory changes affecting them?

Keep this to 3-5 bullet points. Do not write an essay.

### Step 4: The Person (if known)

If the user provided a person's name:
- Role and how long they've been there
- Background (previous roles, education if relevant)
- Any public content (LinkedIn posts, conference talks, articles)
- Anything that suggests what they care about

**Do not guess or fabricate personal details.** Only report what you can find from public sources.

### Step 5: Meeting Brief

Structure the output as:

```
## Meeting Brief: [Company Name]
**Date:** [if provided]
**Meeting with:** [person, role]
**Purpose:** [user's stated purpose]

### Company Overview
[2-3 sentences: what they do, size, location]

### Recent Activity
- [3-5 bullet points of recent news, hiring, changes]

### Sector Context
- [3-5 bullet points of relevant industry context]

### About [Person]
[3-4 sentences if person is known]

### Conversation Starters
- [2-3 specific things to mention or ask about based on the research]

### Watch Out For
- [1-2 things to be aware of: sensitivities, recent problems, competitors to avoid mentioning]
```

## Output Rules

- Keep the whole brief under 400 words. It should be scannable in 5 minutes.
- Be specific. "They recently posted 3 engineering roles" not "They appear to be growing."
- If you cannot find information on something, say so. Do not pad with generalities.
- Do not include information the user obviously already knows (e.g. if they work there).
- Conversation starters should be genuine, not sycophantic. "I noticed you recently..." not "I'm so impressed by your..."
- British English throughout.

## What This Skill Does NOT Do

- Access private LinkedIn profiles (only public information)
- Provide financial advice or credit checks
- Research individuals without a legitimate business context
- Fabricate details when information is not available
