# Cold Email Rules

## Em Dash Discipline

ZERO em dashes anywhere inside the email block. That includes the subject line, the opening, the middle, the ask, and the sign-off. Use commas, full stops, or parentheses instead.

The brief above the email uses em dashes freely (they are allowed in the brief). This makes them very easy to leak into the email unconsciously because you have just written several. Before running the check, actively scan the email for em dashes. Search visually for the `—` character. If you find one, replace it before running the script.

## Length Discipline

Target 110-130 words. Hard cap 150. Aim low and leave headroom.

If your draft comes in at 140+, you are almost certainly padding. What padding looks like:

- Opening sentence that restates what you do before the hook ("I work in content and noticed...")
- Two sentences where one would do ("We produce youth-culture marketing content. We've worked with brands like X and Y.")
- Hedging phrases ("I thought it might be worth reaching out to see if...")
- Sign-off that goes beyond name and greeting ("Looking forward to hearing from you — feel free to reply at any time")

How to cut: remove adjectives, tighten the opening, drop any sentence that does not either reference a real event or make a single clear ask. It is much easier to pass the check at 115 than to negotiate yourself down from 152.

## Nothing After Sign-Off

The email block ends at the signature name. That means:

- No italic notes like `*[Need to identify the right contact]*` after the sign-off
- No "Word count: 123" annotations
- No `[Your name]` placeholder instructions
- No PostScript lines that are really guidance, not email copy

If you need to flag contact-identification guidance or any other meta-note, put it in the brief's **Person notes** section, not inside or after the email block. The brief is for the user; the email is the deliverable.

## Contact Name Rules

If no contact name is known, open with `Hi [name],` as a literal placeholder — the brackets tell the user to fill it in. In the brief's **Person notes** section, add a one-line note naming the likely role the email should go to (e.g. "Target: VP of the relevant function — search LinkedIn for the parent company name and that function"). Do NOT guess the contact from web search. A wrong name is worse than `[name]`.

## Step 5 Hook Layer Detail

This is where the cold email opening comes from. Always anchor WebSearch queries to the current year and month — stale results are a real failure mode, especially for tech, media, and gaming targets where older content still ranks well.

Year-anchored query patterns (if today is April 2026):

- `"[company name]" news 2026`
- `"[company name]" April 2026` or `"[company name]" "last month"`
- `"[company name]" hiring 2026` or `"[company name]" jobs 2026`
- `"[company name]" launch 2026` or `"[company name]" announcement 2026`
- `"[company name]" [CEO name if known] 2026`
- `"[company name]" campaign 2026` (if relevant to what the user is pitching)

**Strong signal:** a specific event with a date in the last 90 days — product launch, campaign announcement, senior hire, funding round, conference talk, published article by the contact.

**Weak signal:** "they're growing", "they care about innovation", a 2024 press release, a generic about-page statement.

If a query returns clearly old results (2023, 2024, early 2025), reject them and try again with a more specific time window. Do not include old results in the brief as if they were recent. WebFetch the company homepage and any visible press or blog page — pull the three most recent items and check their dates before using them as hooks.
