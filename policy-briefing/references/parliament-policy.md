<!-- This file is loaded by the policy-briefing skill. It provides source guidance and analyst framing. -->

# Parliamentary Policy Research

## Audience Context

The person you are helping is typically a policy consultant, lobbyist, think tank researcher, or in-house government affairs professional. They need to understand the political temperature on an issue and who the key players are. They are not looking for a general summary — they want actionable intelligence: who matters, what the mood is, and where the leverage is.

---

## Hansard Result Types Explained

When you get results from `parliament_search_hansard`, the type of result signals how to weight it:

- **Oral questions** — show active engagement from backbenchers. MPs have to secure a slot; it signals genuine interest in the topic.
- **Written questions** — show detailed policy probing. Often more substantive than oral questions for technical policy detail.
- **Westminster Hall debates** — frequently more substantive than main chamber debates. Smaller attendance, longer contributions, more cross-party.
- **Lords debates** — often more technical and cross-party than Commons. Lords committees produce detailed scrutiny reports worth noting.
- **Main chamber debates** — high profile but shorter individual contributions. Government set-piece events.
- **Ministerial statements** — the government's current stated position. High signal for policy direction.

**Weighting:** Recent debates (last 6 months) carry significantly more weight than older ones. Volume of activity matters less than recency and prominence of speakers.

---

## Member Categorisation

When identifying key members from Hansard results, categorise them:

- **Advocates** — actively pushing for the policy. These are your allies or the policy's champions. Note their seniority (backbencher vs minister vs committee chair).
- **Critics** — actively opposing or raising concerns. Understand their specific objections — this tells you where the policy is vulnerable.
- **Ministers** — those with departmental responsibility. A minister's statement is the government's current position. If a minister has spoken in support, that's a strong indicator.
- **Cross-party voices** — particularly valuable for assessing passage prospects. If MPs from multiple parties have spoken in favour, it signals broader political viability.

A single influential minister's comment can signal more than 20 backbench speeches. Look for the seniority and role of each speaker, not just the count.

---

## Using parliament_vibe_check

`parliament_vibe_check` returns an LLM-sampled assessment of parliamentary reception:
- Overall sentiment (supportive / mixed / hostile)
- Key themes in the debate
- Points of contention
- Likely trajectory

**How to interpret it:** Use as a synthesis tool, not a primary source. It aggregates patterns from debate data. Always cross-reference with the actual Hansard results you found — if the vibe check says "mixed" but your search found recent ministerial support and no recent opposition, note the discrepancy.

**When to run it:** After you've searched Hansard and identified key members. It works best when you have a clear, specific policy description to pass to it. Vague descriptions produce vague assessments.

**When NOT to treat it as definitive:** For very recent policy developments (last 4–6 weeks), the vibe check may not reflect the most current position. Cross-reference with the most recent Hansard dates you found.

---

## Key Principles

- **Recency matters.** A debate from last month carries ten times the weight of one from two years ago. Lead with what's current.
- **Voices, not just votes.** Who is saying what matters as much as how many. A single influential minister's comment can signal more than 20 backbench speeches.
- **Cross-reference the vibe check.** `parliament_vibe_check` is useful for synthesis but it's an LLM assessment. Always ground it in the actual Hansard data you found.
- **Territorial extent.** UK legislation often applies differently in England & Wales, Scotland, and Northern Ireland. Always check extent when citing Acts.
- **No prediction claims.** You can assess momentum and prospects. You cannot predict what Parliament will do. Frame accordingly.
- **Actionable intelligence.** The reader wants to know: what should I do next? Who should I talk to? Where is the leverage? The briefing should answer these, not just describe the landscape.
