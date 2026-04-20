# Email Format

## Email Structure

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

## Hard Rules

- **Target 110-130 words. Hard cap 150.** If you hit 140+, you are padding — cut adjectives, tighten the opening, drop any sentence that does not reference a real event or make a single clear ask.
- **Zero em dashes everywhere** — subject line, body, sign-off, all of it. Use commas, full stops, or parentheses instead. Scan visually for the `—` character before running the check.
- **Nothing after the sign-off name.** The email block ends at the signature. No italic notes, no word count annotations, no `[Your name]` placeholder instructions, no PostScript lines. Meta-notes go in the brief's Person notes or Watch out for sections.

## Good vs Bad Output

**Good email opening:**
> "Saw the announcement about the Bristol studio opening last week — looks like you're building out the production side properly."

Why it works: specific event, specific date window, no flattery, connects naturally to what follows.

**Bad email opening:**
> "I've been following your company's impressive growth and innovative approach to content creation."

Why it fails: no specific event, could apply to any company, classic marketing deck language, will be deleted.

**Good hook (from Step 5):**
> "Read your piece on creator economics in The Drum — the point about measurement gaps in cultural campaigns landed."

Why it works: names the publication, names the piece, names the specific claim that resonated.

**Bad hook (from Step 5):**
> "I noticed your company is doing great work in the youth space."

Why it fails: no source, no event, no reason this email exists today rather than last year.

## What to Do After Drafting

**In Claude Code:** run the validation script at `scripts/check-output.py`. Do not show the user a FAIL output — rewrite and run again. Pass with warnings is fine to show; mention the warnings.

**In claude.ai:** follow the same rules mentally. Check the email against the banned word list in the Voice and Tone section. Count the email words. Look for em dashes. Catch American spellings.
