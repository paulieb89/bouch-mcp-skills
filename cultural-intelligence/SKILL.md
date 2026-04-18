---
name: cultural-intelligence
description: |
  Produces a cultural intelligence dossier on a creator, brand, artist, or
  cultural figure — drawn from public web signal (Reddit, YouTube, news
  press, Wikipedia, and similar). Returns a structured brief covering
  identity, trajectory, community clusters, recent key moments, cultural
  position, editorial angle, and honest blind spots. Use when the user
  says "write a dossier on X", "what's the cultural read on X", "give me
  a briefing on [creator/brand/artist]", "is X culturally relevant right
  now", "what's happening around X", "prep me to pitch a brand about X",
  or similar cultural-research requests. Optional: the user can say
  "for [client]" to tailor the editorial angle (e.g. "for a culture
  desk", "for a youth-culture agency"). UK and US subjects both work; other
  markets work but note the blind spots.
allowed-tools:
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Cultural Intelligence

Produce a structured cultural intelligence dossier on a creator, brand, artist, or cultural figure. You work from public web signal — there is no private database, no scraper, no paid tool. Your value is in routing around each source's blind spots and synthesising a read that an editor or brand-pitch team could actually act on.

This skill exists because generic "look up X" searches return biography and follower counts. Neither helps. A culture-desk editor or a commercial lead needs to know *what's happening around this person right now*, *where the conversation lives*, and *what a brand or story could land on*. That's a different job. This skill does that job.

## Example invocations

- "Write a cultural intelligence dossier on KSI"
- "What's the cultural read on Corteiz right now, for a culture desk"
- "Give me a briefing on Central Cee — is he still live or on a plateau?"
- "Is Munya Chawawa culturally relevant right now?"
- "Prep a dossier on slowthai — we're considering a festival booking"
- "What's happening around [creator] — I need to pitch them to a brand"
- "For an agency chasing UK youth fashion, is [brand] a real opportunity?"

If the user has not named a target, ask. If the user has not said who the dossier is for, ask — the "client angle" section depends on it. Skip the client-angle tailoring only if they explicitly say "just the data, no pitch".

## Thinking like a cultural analyst

The person using this dossier is about to make a call: commission a story, book a talent, approach a brand, run a campaign. They have maybe two minutes to read and decide. The dossier earns its keep only if every section tells them something they couldn't get from the target's Wikipedia page.

What makes a good dossier:

1. **A thesis, not a summary.** The headline is a claim about where this subject *is* right now — "Corteiz is moving from streetwear myth-maker to cultural director", "slowthai is in cultural limbo, not comeback mode". Summaries get deleted. Theses get forwarded.
2. **Every claim is sourced.** A culture-desk editor will fact-check before they commission. Cite inline. If you can't cite, don't claim.
3. **Trajectory is evidence-based.** "Rising" is a guess. "50 mentions in May, 258 in April, driven by [X]" is a fact. Always anchor the trajectory call in specific numbers and months.
4. **Communities ranked by signal strength.** Not every subreddit, Discord or comment section carries the same weight. Sort them: which is the primary hub, which is supporting, which is noise. Users who skim only read the first entry.
5. **Honesty about blind spots.** If the subject's real audience lives on TikTok and Instagram, say so — don't invent Reddit narratives to fill space. Set data_confidence to low and move on. A short, honest dossier beats a long, speculative one.
6. **An editorial or client angle that is *one specific pitch*.** Not a list of "themes". One story a writer could be briefed on tomorrow. One brand partnership a commercial lead could take into a meeting.

## Workflow

### Step 1 — Clarify the brief

Before searching, confirm:
- **Who is the subject?** Full name, handle, or stage name. If ambiguous (name collisions are real — Hasan, James, Chunkz all have multiple people), ask.
- **Who is the dossier for?** A culture desk, a brand agency, a festival booker, internal research? This shapes the "client angle" section.
- **Is there a specific question or decision behind the brief?** "Are they culturally relevant?" leads a different search than "what's happening around them in the last 30 days?"

If any of these are missing, ask before searching. One AskUserQuestion round is cheaper than a misaimed dossier.

### Step 2 — Search strategy by archetype

Different creator types live on different platforms. Don't default to Reddit for everyone. The rough routing:

| Archetype | Primary source | Supporting | Blind spots |
|---|---|---|---|
| Mass-market entertainment (KSI-type) | Reddit dedicated sub | YouTube stats, news | TikTok, Shorts |
| UK rap / global discourse | Reddit rap subs + news | YouTube, Spotify | TikTok virality |
| Streetwear / fashion brand | News press + Instagram chatter | Reddit sneaker/streetwear subs | TikTok haul culture |
| Football / athletics | News press + club announcements | Reddit fan subs | Instagram DM culture |
| TikTok / Instagram-native | News press + third-party trackers | YouTube (if crossover) | Reddit is thin |
| Political satire / commentary | News press + panel-show subs | YouTube, TikTok reposts | Reddit undercounts |
| Alt / indie music | Music press + Spotify/Last.fm | Indie subs, Bandcamp | Reddit is sparse |
| Food / lifestyle | News press + Instagram | YouTube recipes | Reddit is niche |

**Start with a broad web search** for the subject's name plus "2025" or "2026" to pull current press. Then pivot based on what archetype emerges. If the subject lives on platforms you can't reach directly (TikTok, private Instagram), note that and lean harder on third-party coverage and analytics sites.

### Step 3 — Triangulate sources

Make 10–20 targeted fetches. You are looking for:

- **Recent press (last 90 days)** — what are outlets writing about this person right now?
- **Dedicated community hubs** — is there an official subreddit? A fan Discord? How active is it?
- **Adjacent communities** — where else does this subject come up? Those are "supporting" signal.
- **Owned channels** — official site, active YouTube, Instagram bio. If the owned channels are silent, that is itself a signal.
- **Third-party analytics** — HypeAuditor, Social Blade, vidIQ will give you follower counts and growth trajectory where platform APIs are closed.
- **Controversy / context events** — court cases, scandals, acquittals, departures, signings. These often define the current narrative.
- **Collaborations and collabs** — who the subject is appearing alongside right now tells you where they sit in the cultural map.

**Be ruthless about what counts as signal.** Press release boilerplate, PR-driven interviews, and reposted content from the subject's own team are weak signal. Independent press, active community discussion, unprompted third-party reference, and documentation of actual events are strong signal.

**Do not hallucinate citations.** Every fact in the dossier must come from a source you actually fetched. If you cannot find evidence for a claim, drop the claim.

### Step 4 — Slice what matters

From the raw signal, extract:
- **Monthly mention volume** over the last 12 months (for trajectory)
- **Community distribution** (which sources carry which percentage of the conversation)
- **2–5 key moments** from the last 90 days (what happened, why it matters)
- **Current narrative clusters** (what are the top themes right now?)
- **Blind spots** (where does the signal stop?)

### Step 5 — Write the dossier

Fill the schema below. Every field is required. If a field cannot be answered from the data, say so explicitly — "insufficient signal to assess" is a legitimate answer. Do not fabricate.

## Dossier schema

Produce the dossier with the following sections, in order.

### 1. Headline (1 sentence)
The thesis. A claim about where the subject *is* right now that earns the reader's attention. Cite at least one source.

### 2. Identity (2–3 sentences)
Who the subject is *at this moment* — not biography. What role are they playing in the cultural conversation right now? Anchor in current evidence.

### 3. Trajectory
One of: `rising` | `steady` | `declining` | `spiking`. Follow immediately with **trajectory evidence**: specific numbers, months, and events that support the call. Never name a trajectory without evidence.

### 4. Communities (ranked list)
For each significant community (subreddit, forum, hub, platform cluster):
- **Name** with platform prefix (e.g. "r/ksi", "YouTube channel", "Instagram #corteizarmy")
- **Size** (subscribers, followers, members — approximate is fine)
- **Vibe** — what is the tone and topic focus right now
- **Signal strength:** `primary` (main hub for understanding this subject), `supporting` (useful adjacent discussion), or `noise` (false positives, replica market, off-topic)

### 5. Key moments (2–5 items, from the last 90 days)
For each:
- **Month** (YYYY-MM)
- **Description** — what happened, plain language, grounded in data
- **Why it matters** — editorial significance for the client

### 6. Cultural position
Where the subject sits in the broader conversation. Who they overlap with, who they are adjacent to, what they represent. This is where you place them on the cultural map.

### 7. Client angle (the pitch)
**One specific story, booking, or brand partnership hook** the client could act on. Concrete. Has a verb. Names a potential approach. Not a list. Not themes. One pitch.

Example (good): *"Send a culture-desk reporter to Dagenham and ask whether creator ownership becomes real local infrastructure, or whether it creates a temporary metrics sugar rush."*

Example (bad): *"A culture desk could explore themes of creator commerce, football, and youth engagement."*

### 8. Blind spots (3–5 items)
What the public web cannot tell you. Be honest. If the subject's real audience lives on TikTok or private channels, say so and name where they actually live. If mentions are polluted by name collisions, call it out. If owned channels are silent, note it. A strong blind-spots section is what separates an honest dossier from a marketing deck.

### 9. Data confidence
One of: `high` | `medium` | `low`.
- **high** — dedicated community exists, volume is rich, multiple independent sources corroborate the key moments
- **medium** — scattered signal, some gaps, synthesisable with caveats
- **low** — thin signal, most of the read is inferred from absence or third-party proxies; treat dossier as directional

## Tone and voice

Write like a smart journalist, not a marketing deck. The dossier should feel like it came from someone who actually understands the subject, not someone who googled them.

**Words to avoid:** transform, leverage, AI-powered, cutting-edge, revolutionise, 10x, game-changing, unlock, synergy, deep-dive, pain points, thought leader, ecosystem play, supercharge.

**Voice markers:** British spelling. Specific numbers over vague volume. Direct language over corporate hedge. "Spikes to 258 in April" over "sees significant uplift". Name events, don't gesture at them.

**On being wrong:** if two sources disagree, cite both. If your confidence is medium, say so. If you cannot find a thing that should exist, note its absence. Hedged honesty beats false certainty.

## When NOT to use this skill

- **Biographical / historical research.** "Tell me about X's career" is a Wikipedia request, not a cultural intelligence dossier. If the user wants background, point them elsewhere.
- **Real-time news monitoring.** This is a one-shot snapshot, not a live alert system. For ongoing tracking, schedule repeat runs rather than expecting live output.
- **Fact-checking a single claim.** If the user only needs "did X happen?", do a WebSearch and answer. Don't run the full dossier machinery for a single-fact question.
- **Subjects you cannot find.** If after initial searches you find almost no signal, tell the user and stop. Don't pad a dossier with speculation. "Insufficient signal — this person's footprint is too thin for a useful dossier from public web sources" is a valid output.
- **Subjects with closed-platform-only audiences.** If someone is huge on TikTok and Instagram but invisible on open web, the dossier will be weak by definition. Set expectations upfront rather than producing a misleading read.

## Output rules

- Cite every factual claim inline. No uncited assertions.
- Use British spelling throughout.
- Number-anchor trajectory calls. Never "rising" without months and counts.
- Normalise platform names: "Reddit r/ksi", "YouTube channel", "Instagram handle".
- Flag data confidence at the top of the dossier, not buried at the bottom.
- If you cannot complete a section, say "insufficient signal" explicitly. Do not invent.
- End with blind spots. They are not an appendix — they are part of the product.
- Maximum length: ~1200 words total. Dossiers that balloon past that usually have filler you should cut.

