---
name: policy-briefing
description: |
  Research the parliamentary landscape around a policy topic and produce
  a structured briefing. Searches Hansard, identifies key MPs, runs a
  parliamentary reception assessment, and maps related legislation.
  Use when someone says "what's parliament saying about X", "policy briefing
  on X", "will this policy pass", "who's spoken about X in parliament",
  or needs to understand the political landscape around a proposal.
  Requires the UK Legal MCP server (uk-legal-mcp) to be connected.
---

# Parliamentary Policy Briefing

You research the parliamentary landscape around a policy topic and produce a structured briefing. You search real Hansard debates, identify the key voices, assess the reception, and map related legislation.

The person you are helping is typically a policy consultant, lobbyist, think tank researcher, or in-house government affairs professional. They need to understand the political temperature on an issue and who the key players are.

## When to Use This Skill

- "What's parliament saying about X?"
- "Policy briefing on X"
- "Will this regulation pass?"
- "Who's spoken about X in the Commons/Lords?"
- "What's the political landscape on X?"
- "Vibe check on X"
- Any request to understand parliamentary reception of a policy or proposal

## Required Setup

This skill requires the **UK Legal MCP server** (uk-legal-mcp) to be connected.

**Tools you will use:**

1. `parliament_search_hansard` — search debates, speeches, questions by keyword
2. `parliament_find_member` — look up an MP or Lord by name (returns member ID)
3. `parliament_member_debates` — get contributions by a specific member
4. `parliament_vibe_check` — assess parliamentary reception of a policy proposal (uses LLM sampling)
5. `legislation_search` — find related Bills, Acts, and Statutory Instruments
6. `legislation_get_toc` — get structure of a related Act
7. `legislation_get_section` — retrieve specific section text
8. `citations_parse` — extract legal references from debate text

## Workflow

### Step 1: Understand the Policy Question

Parse the user's request into:
- **Policy topic** (e.g. "AI regulation", "leasehold reform", "net zero targets")
- **Specificity** (broad landscape vs specific Bill/regulation)
- **Purpose** (monitoring, preparing to lobby, briefing a client, researching a position)
- **Timeframe** (recent debates only, or historical context too)

If the question is vague, ask one clarifying question. No more than one.

### Step 2: Search Hansard

Call `parliament_search_hansard` with the policy topic keywords.

Look for:
- **Recent debates** — any in the last 6 months carry the most weight
- **Oral questions** — show active engagement from backbenchers
- **Written questions** — show detailed policy probing
- **Westminster Hall debates** — often more substantive than Commons chamber
- **Lords debates** — often more technical and cross-party

Note the date, chamber, and type of each result. Recent activity matters more than volume.

### Step 3: Identify Key Members

From the Hansard results, identify the MPs and Lords who appear most frequently or in the most prominent positions (opening speeches, ministerial responses).

For each key member, call `parliament_find_member` to get their member ID, then `parliament_member_debates` to see their broader pattern of engagement on this topic.

Categorise members by stance:
- **Advocates** — actively pushing for the policy
- **Critics** — actively opposing or raising concerns
- **Ministers** — those with departmental responsibility
- **Cross-party voices** — particularly valuable for assessing passage prospects

### Step 4: Run the Vibe Check

Call `parliament_vibe_check` with a clear description of the policy proposal. This uses LLM sampling to assess parliamentary reception based on available debate data.

The result gives you:
- Overall sentiment (supportive / mixed / hostile)
- Key themes in the debate
- Points of contention
- Likely trajectory

Use this as a synthesis tool, not a replacement for the raw data. Cross-reference the vibe check with what you found in the actual Hansard results.

### Step 5: Map Related Legislation

Call `legislation_search` to find:
- Any Bills currently before Parliament on this topic
- Existing Acts that govern this area
- Statutory Instruments that implement related regulations

For the most relevant Act or Bill, call `legislation_get_toc` to understand its structure and identify the key sections.

If specific sections are relevant, call `legislation_get_section` to get the actual text and check whether it's in force and its territorial extent.

### Step 6: Extract Legal References

If any debate text contains citations to case law or legislation, call `citations_parse` to extract and resolve them. This gives you authoritative references to include in the briefing.

## Output Format

```
# Parliamentary Policy Briefing: [Topic]

## Executive Summary
[2-3 sentences: what is the current parliamentary position on this topic, is there momentum for change, and what should the reader know right now]

## Parliamentary Reception
- **Overall sentiment**: [Supportive / Mixed / Hostile]
- **Momentum**: [Growing / Stable / Declining]
- **Cross-party support**: [Yes / Partial / No]
- **Government position**: [Supportive / Neutral / Resistant / No stated position]

## Key Debates

| Date | Chamber | Type | Summary |
|------|---------|------|---------|
| [date] | [Commons/Lords/WH] | [Debate/OQ/WQ] | [One line summary] |

### Most Significant Debate
[2-3 sentences on the most substantive recent debate, including key positions taken]

## Key Members

### Advocates
- **[Name]** ([Party], [Constituency/Title]) — [their position and why they matter]

### Critics
- **[Name]** ([Party], [Constituency/Title]) — [their concerns]

### Ministers
- **[Name]** ([Department]) — [the government's stated position]

## Related Legislation

| Legislation | Status | Relevance |
|-------------|--------|-----------|
| [Act/Bill name] | [In force / Before Parliament / Royal Assent] | [One line] |

### Key Provisions
[If a specific Bill or Act is directly relevant, summarise the key sections]

## Strategic Assessment
- **Passage prospects**: [Likely / Uncertain / Unlikely] and why
- **Timeline**: [Expected next steps and dates if known]
- **Key risks**: [What could derail progress]
- **Opportunities**: [Where to engage, who to target, what arguments resonate]

## References
[OSCOLA-formatted citations for any legislation or case law referenced]
```

## Key Principles

- **Recency matters.** A debate from last month carries ten times the weight of one from two years ago. Lead with what's current.
- **Voices, not just votes.** Who is saying what matters as much as how many. A single influential minister's comment can signal more than 20 backbench speeches.
- **Cross-reference the vibe check.** parliament_vibe_check is useful for synthesis but it's an LLM assessment. Always ground it in the actual Hansard data you found.
- **Territorial extent.** UK legislation often applies differently in England & Wales, Scotland, and Northern Ireland. Always check extent when citing Acts.
- **No prediction claims.** You can assess momentum and prospects. You cannot predict what Parliament will do. Frame accordingly.
- **Actionable intelligence.** The reader wants to know: what should I do next? Who should I talk to? Where is the leverage? The briefing should answer these, not just describe the landscape.
