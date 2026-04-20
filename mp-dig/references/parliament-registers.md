<!-- This file is loaded by the mp-dig skill. It provides register descriptions and constituent framing. -->

# Parliament Registers

## What the Registers Tell You

**Parliament Members API** gives you: name, party, constituency, member ID. The member ID is the key — it unlocks everything else. Use `parliament_find_member` with the MP's name (surname alone usually works). If the user gives a constituency, try the member's name if known, or search broadly.

**Register of Members' Financial Interests** is the richest source. It is a legal requirement — every declared interest is public record. Categories include:
- Employment and earnings
- Donations and sponsorship
- Gifts and hospitality from UK sources
- Overseas visits (who paid, destination, purpose)
- Land and property
- Shareholdings
- Family members employed and paid from parliamentary expenses
- Family members who lobby

Each entry has dates, amounts where declared, and the source. Use `parliament_member_interests` with the member ID.

**Hansard** records every speech, question, and intervention in both chambers. Filter by member and topic. Recent contributions carry more weight than old ones. Use `parliament_member_debates` with member ID and a topic filter, or `parliament_search_hansard` to search by keyword first.

**Division records** show exactly how an MP voted. The motion title, the date, ayes/noes, and whether it passed. Use `votes_search_divisions` with a topic keyword, then check if this member voted in those divisions, or filter by member to see their full voting pattern.

**Companies House cross-reference** (via the due diligence MCP) lets you check any companies that appear in the interests register. Pull the company profile: is it active? Who else is a director? Is it filing on time? Any gazette notices? Use `company_search` then `company_profile` and `company_officers`.

---

## What You Don't Have

- Undeclared interests (by definition, invisible)
- Local council voting records (Parliament API only covers Westminster)
- Expenses claims detail (IPSA publishes this separately, not in this API)
- Social media activity
- Private meetings or informal lobbying

Be clear about these limits. The user needs to know the difference between "nothing found" and "not checkable here".

---

## Thinking Like a Constituent

The person asking wants accountability. They might be a voter checking their local MP, a journalist researching a story, a campaigner tracking positions on an issue, or someone who just saw their MP on TV and wants to know the full picture. They want:

1. **Who funds them?** Donations, gifts, hospitality, overseas visits. Every declared interest is public record.
2. **What do they own?** Land, property, shareholdings. These create potential conflicts of interest.
3. **How do they vote?** Not what they say in interviews — how they actually vote in the division lobbies. Words and votes often diverge.
4. **What do they say in Parliament?** Hansard records every word. Filter by topic to see if they've spoken about the issue the user cares about.
5. **Who are they connected to?** If they have interests in companies, check those companies on Companies House. Directors, filing status, beneficial owners.

Present findings factually. Don't editorialize about whether an interest is good or bad. The user can draw their own conclusions. Your job is to surface the data clearly.

---

## Reading the Interests Register

The most significant categories are usually:
- **Donations and sponsorship** — who is paying for their campaigns
- **Employment and earnings** — what paid work they do outside Parliament
- **Land and property** — potential conflicts on housing policy
- **Shareholdings** — potential conflicts on regulatory and tax policy
- **Overseas visits** — who is taking them on trips and why

Less often significant (but worth noting if substantial):
- **Gifts and hospitality** — minor entries are routine; large or repeated entries from one source matter
- **Family members employed** — not inherently problematic but worth noting

The register is self-reported. Entries that are absent do not necessarily mean the interest doesn't exist — they mean it hasn't been declared. Note that distinction in your output.
