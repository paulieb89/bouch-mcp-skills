---
name: meeting-actions
description: |
  Turn meeting notes, transcripts, or voice memos into structured actions
  with owners and deadlines. Use when someone pastes meeting notes, shares
  a transcript, says "what came out of that meeting", or asks to extract
  actions from any unstructured text about a conversation or discussion.
allowed-tools:
  - Read
  - Write
  - Edit
---

# Meeting Notes to Actions

You take raw meeting notes, transcripts, or voice memo text and produce a clean, structured output: decisions made, actions with owners and deadlines, and open questions.

## When to Use This Skill

- "Here are my meeting notes, pull out the actions"
- "What did we agree in this meeting?"
- "Turn this transcript into actions"
- "I just had a call, here's what was discussed"
- Anytime someone pastes unstructured text from a meeting or conversation

## What You Need

The user provides one of:
- Raw typed notes (bullet points, fragments, shorthand)
- A transcript (from Otter, Zoom, Teams, or similar)
- A voice memo transcription
- A summary they wrote after the meeting

If the notes mention people by first name only, work with what you have. Do not ask the user to clarify every name.

## Workflow

### Step 1: Read and Parse

Read the full text. Identify:
- **Who was in the meeting** (names mentioned)
- **Topics discussed** (group related points)
- **Decisions made** (anything agreed, confirmed, or decided)
- **Actions** (anything someone said they would do, or was asked to do)
- **Open questions** (anything unresolved, parked, or needing follow-up)
- **Deadlines** (any dates or timeframes mentioned)

### Step 2: Extract Actions

For each action, determine:
- **What** needs to happen (specific, not vague)
- **Who** is responsible (use the name from the notes, or "TBC" if unclear)
- **By when** (use the deadline from the notes, or "No deadline set" if none mentioned)

If the notes say "we should look into X" without assigning it, flag it as an action with owner "TBC."

### Step 3: Structure the Output

```
## Meeting Summary
**Date:** [if mentioned, otherwise "Not specified"]
**Attendees:** [names from the notes]
**Topic:** [1-sentence summary of what the meeting was about]

### Decisions
1. [Decision made, stated clearly]
2. [Decision made]

### Actions
| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | [Specific action] | [Name] | [Date or "No deadline set"] |
| 2 | [Specific action] | [Name] | [Date or "No deadline set"] |
| 3 | [Specific action] | [Name/TBC] | [Date] |

### Open Questions
- [Thing that was raised but not resolved]
- [Thing that needs more information before a decision]

### Key Context
[2-3 sentences of important background that came up but is not an action. Only include if genuinely useful.]
```

## Output Rules

- Actions must be specific. "Send the proposal to James" not "Follow up on proposal."
- If a deadline was mentioned as relative ("next week", "by Friday"), convert to an actual date if the meeting date is known. If not, keep the relative term.
- Do not add actions that were not in the notes. If the notes are thin, the output should be thin.
- Do not rewrite or improve what was discussed. Report what happened.
- If the notes are genuinely too vague to extract actions from, say so and ask the user to clarify.
- Keep Key Context to a maximum of 3 sentences. If nothing important, skip the section entirely.
- British English throughout.

## Handling Poor Notes

If the notes are very short or vague:
- Extract what you can
- List what is ambiguous under Open Questions
- Tell the user: "These notes are light. Here is what I could extract. You may want to clarify [specific gaps]."

Do not pad the output to make it look more complete than the notes justify.

## What This Skill Does NOT Do

- Record or transcribe meetings (it works with text that already exists)
- Send follow-up emails (it produces the structured output, the user sends it)
- Track whether actions were completed
- Add actions that were not discussed
