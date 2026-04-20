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
license: Apache-2.0
compatibility: Requires WebSearch and WebFetch access.
metadata:
  author: bouch
  version: "2.0"
allowed-tools:
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Cultural Intelligence

Produce a structured cultural intelligence dossier on a creator, brand, artist, or cultural figure. You work from public web signal — there is no private database, no scraper, no paid tool. Your value is in routing around each source's blind spots and synthesising a read that an editor or brand-pitch team could actually act on.

This skill exists because generic "look up X" searches return biography and follower counts. Neither helps. A culture-desk editor or commercial lead needs to know what is happening around this person right now, where the conversation lives, and what a brand or story could land on. That is a different job. This skill does that job.

## Example invocations

- "Write a cultural intelligence dossier on KSI"
- "What's the cultural read on Corteiz right now, for a culture desk"
- "Give me a briefing on Central Cee — is he still live or on a plateau?"
- "Is Munya Chawawa culturally relevant right now?"
- "Prep a dossier on slowthai — we're considering a festival booking"
- "What's happening around [creator] — I need to pitch them to a brand"
- "For an agency chasing UK youth fashion, is [brand] a real opportunity?"

If the user has not named a target, ask. If the user has not said who the dossier is for, ask — the client angle section depends on it. Skip the client-angle tailoring only if they explicitly say "just the data, no pitch".

## Step 1 — Clarify the brief

Before searching, confirm who the subject is (full name, handle, or stage name — name collisions are real), who the dossier is for (a culture desk, brand agency, festival booker, internal research), and whether there is a specific question behind the brief ("are they relevant?" leads a different search than "what's happening in the last 30 days?"). If any of these are missing, ask before searching. One AskUserQuestion round is cheaper than a misaimed dossier.

## Step 2 — Search by archetype

Route to the right platforms before you start fetching. Different creator types live on different sources — see `references/platform-routing.md` for the 8-archetype routing table and guidance on what counts as strong vs weak signal. Start with a broad web search for the subject's name plus the current year to pull recent press, then pivot based on what archetype emerges.

## Step 3 — Triangulate sources

Make 10-20 targeted fetches for recent press (last 90 days), dedicated community hubs, adjacent communities, owned channels, third-party analytics, controversy and context events, and collaborations. Be ruthless about what counts as signal: PR boilerplate and reposted content from the subject's own team are weak. Independent press, active community discussion, and documentation of actual events are strong. Do not hallucinate citations — every fact must come from a source you actually fetched.

## Step 4 — Slice what matters

From the raw signal, extract monthly mention volume over the last 12 months (for trajectory), community distribution across sources, 2-5 key moments from the last 90 days, current narrative clusters, and blind spots where the signal stops.

## Step 5 — Write the dossier

Fill all 9 sections of the schema in `assets/dossier-schema.md`, in order. Every field is required. If a field cannot be answered from the data, say "insufficient signal" explicitly — do not fabricate. Flag data confidence at the top, not the bottom.

## Output rules

- Cite every factual claim inline. No uncited assertions.
- Use British spelling throughout.
- Number-anchor trajectory calls. Never "rising" without months and counts.
- Flag data confidence at the top of the dossier.
- End with blind spots. They are not an appendix — they are part of the product.
- Maximum length: approximately 1200 words total. Dossiers that balloon past that usually have filler to cut.

## When NOT to use this skill

- **Biographical or historical research.** "Tell me about X's career" is a Wikipedia request, not a cultural intelligence dossier.
- **Real-time news monitoring.** This is a one-shot snapshot, not a live alert system.
- **Fact-checking a single claim.** If the user only needs "did X happen?", do a WebSearch and answer. Don't run the full dossier machinery.
- **Subjects you cannot find.** If after initial searches you find almost no signal, tell the user and stop. "Insufficient signal — this person's footprint is too thin for a useful dossier from public web sources" is a valid output.
- **Subjects with closed-platform-only audiences.** If someone is huge on TikTok and Instagram but invisible on the open web, set expectations upfront rather than producing a misleading read.

## Files in this skill

- `references/platform-routing.md` — 8-archetype search routing table, triangulation guidance, and what makes a good dossier
- `assets/dossier-schema.md` — full 9-section dossier schema with guidance text for each field
