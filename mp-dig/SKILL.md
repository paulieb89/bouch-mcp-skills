---
name: mp-dig
description: |
  Investigate a UK Member of Parliament. Pulls financial interests, voting
  record, Hansard contributions, and cross-references with Companies House.
  Use when someone asks "dig into my MP", "what are their interests",
  "how did they vote on X", "who funds them", or names a specific MP.
  Requires UK Legal MCP and UK Due Diligence MCP servers.
allowed-tools:
  - mcp__claude_ai_uk-legal-tools__parliament_find_member
  - mcp__claude_ai_uk-legal-tools__parliament_member_interests
  - mcp__claude_ai_uk-legal-tools__parliament_member_debates
  - mcp__claude_ai_uk-legal-tools__votes_search_divisions
  - mcp__claude_ai_uk-legal-tools__votes_get_division
  - mcp__claude_ai_uk-legal-tools__parliament_search_hansard
  - mcp__claude_ai_uk-due-diligence__company_search
  - mcp__claude_ai_uk-due-diligence__company_profile
  - mcp__claude_ai_uk-due-diligence__company_officers
---

# MP Dig

Investigate a UK Member of Parliament using official public registers. Financial interests, voting record, parliamentary contributions, and corporate connections.

## Thinking Like a Constituent

The person asking wants accountability. They might be a voter checking their local MP, a journalist researching a story, a campaigner tracking positions on an issue, or someone who just saw their MP on TV and wants to know the full picture. They want:

1. **Who funds them?** Donations, gifts, hospitality, overseas visits. The Register of Members' Financial Interests is a legal requirement — every declared interest is public record.
2. **What do they own?** Land, property, shareholdings. These create potential conflicts of interest.
3. **How do they vote?** Not what they say in interviews — how they actually vote in the division lobbies. Words and votes often diverge.
4. **What do they say in Parliament?** Hansard records every word. Filter by topic to see if they've spoken about the issue the user cares about.
5. **Who are they connected to?** If they have interests in companies, check those companies on Companies House. Directors, filing status, beneficial owners.

Present findings factually. Don't editorialize about whether an interest is good or bad. The user can draw their own conclusions. Your job is to surface the data clearly.

## What the Registers Tell You

**Parliament Members API** gives you: name, party, constituency, member ID. This is the key — the member ID unlocks everything else.

**Register of Members' Financial Interests** is the richest source. Categories include: employment and earnings, donations and sponsorship, gifts and hospitality from UK sources, overseas visits, land and property, shareholdings, family members employed and paid from parliamentary expenses, family members who lobby. Each entry has dates, amounts where declared, and the source.

**Hansard** records every speech, question, and intervention in both chambers. Filter by member and topic. Recent contributions carry more weight than old ones.

**Division records** show exactly how an MP voted. The motion title, the date, ayes/noes, and whether it passed. Filter by member to see their full voting pattern, or by topic to see where they stood on a specific issue.

**Companies House** (via the due diligence MCP) lets you cross-reference. If an MP declares an interest in "ABC Holdings Ltd", pull the company profile: is it active? Who else is a director? Is it filing on time? Any gazette notices?

## What You Don't Have

- Undeclared interests (by definition, invisible)
- Local council voting records (parliament only)
- Expenses claims detail (IPSA publishes this separately, not in this API)
- Social media activity
- Private meetings or informal lobbying

## How to Work

**Find the member first.** Use `parliament_find_member` with their name. Note the integer member ID — everything else needs it. If the user gives a constituency rather than a name, you may need to search more broadly.

**Pull their interests.** `parliament_member_interests` with the member ID. Scan all categories. The interesting entries are usually in donations, employment, land, and shareholdings. Group by category in your output.

**Check their voting record** if the user asks about a specific issue. `votes_search_divisions` with a topic keyword, then check if this member voted in those divisions. Or use the member_id filter to see all their votes.

**Search Hansard** for what they've said on specific topics. `parliament_member_debates` with the member ID and a topic filter gives you their actual words.

**Cross-reference companies** when they appear in the interests register. Pull the company profile, check directors, check filing compliance. A company that's been dissolved or has overdue filings is worth noting.

**Don't fetch everything.** Interests are the headline. Voting and Hansard are supplementary. If the user asks "dig into MP X", lead with the interests. If they ask "how did X vote on housing", lead with the votes. Read the question.

## When Things Go Wrong

- **Member not found:** Try surname only, or the constituency name. Some members use informal names (e.g. "Keir" vs "Sir Keir Starmer").
- **No interests registered:** Either they genuinely have none, or they haven't updated. Note which and check the date of last update if available.
- **No votes on a topic:** The topic may not have come to a division, or the member may have been absent. "No recorded vote" is different from "voted against".
- **Company not on Companies House:** Could be an overseas entity, a partnership, or a trading name rather than a registered company.

## Good vs Bad Output

**Good:** Opens with a one-paragraph summary of who this MP is (party, constituency, role). Groups interests by category with amounts. Highlights anything unusual — large donations, recent property acquisitions, companies with issues. Links voting record to declared interests where relevant. States what wasn't checked.

**Bad:** Lists every interest with equal weight. Doesn't connect interests to voting patterns. Editorializes about whether interests are corrupt. Misses the company cross-reference. Presents a wall of dates and numbers without context.

## Formatting

Full name with title on first mention. Party and constituency. Amounts in GBP. Dates as DD Month YYYY. Company numbers as 8-digit zero-padded. Neutral tone throughout — present facts, not opinions. Always state: information from official public registers.
