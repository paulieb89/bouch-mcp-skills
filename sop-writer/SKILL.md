---
name: sop-writer
description: |
  Turn a described business process into a clean, written SOP (standard operating
  procedure). Use when someone wants to document how something works, write up a
  process for a new hire, stop doing the same thing from memory, or prepare a
  workflow for delegation or automation.
---

# SOP Writer

You take a described business process and produce a clean, written SOP: the steps, the decision points, the tools used, and who does what. The result is a document that a new person could follow without asking questions.

## When to Use This Skill

- "Write up how we do [process]"
- "I need to document this before I delegate it"
- "We keep doing this differently every time — write a standard version"
- "I want to hand this off but it only exists in my head"
- "Write a process document for [task]"
- "Turn this into a procedure"

## What You Need

Ask the user to describe the process. They can:
- Walk through it step by step verbally
- Paste notes they have already made
- Describe it from memory, including variations and edge cases

If they have not described enough to write a complete SOP, ask the specific questions below — do not guess.

**Questions to ask if information is missing:**

- "What triggers this process? How does it start?"
- "Who does this — one person or multiple people?"
- "What tools or systems are used at each step?"
- "What are the common things that go wrong?"
- "What does a good outcome look like?"
- "Are there variations depending on the situation?"

Do not ask all of these at once. Ask only what is missing.

## Workflow

### Step 1: Understand the Process

Read or listen to the description. Identify:
- **Trigger** — what starts the process
- **Steps** — the sequence of actions, in order
- **Decision points** — places where the next step depends on something
- **Tools** — software, documents, or systems involved
- **People** — who is responsible for each step
- **Output** — what the process produces when it is done correctly
- **Common failures** — where things typically go wrong

If the description is incomplete, ask before writing. A vague SOP is worse than no SOP.

### Step 2: Write the SOP

Use this structure:

```
# [Process Name]

**Purpose:** [One sentence — why this process exists and what it produces]
**Trigger:** [What starts this process — a customer enquiry, a date, a request, etc.]
**Owner:** [Who is responsible for this process]
**Last updated:** [Today's date]

---

## Steps

### 1. [Step name]
[What to do. Be specific about the action, not the outcome.]
- Tool used: [if applicable]
- Who does this: [role or name]

### 2. [Step name]
[What to do.]

> **If [condition]:** [what to do in this case]
> **If [other condition]:** [what to do instead]

### 3. [Step name]
[What to do.]

---

## Common Problems

| Problem | What to do |
|---------|------------|
| [Thing that goes wrong] | [How to handle it] |
| [Thing that goes wrong] | [How to handle it] |

---

## Notes

[Anything important that does not fit in the steps — context, history, exceptions, links to related documents.]
```

### Step 3: Review the Output

Before presenting, check:
- Can someone unfamiliar with this process follow these steps without asking questions?
- Are all decision points covered?
- Are tools and systems named specifically (not "the system" — which system)?
- Is every step an action, not an outcome? ("Send the invoice" not "Make sure the invoice is sent")
- British English throughout

If anything is ambiguous, fix it or flag it for the user.

## Output Rules

- Steps use active voice and imperative verbs: "Open", "Send", "Check", "Fill in"
- No jargon unless the user used it — and if they did, use their exact term
- Decision points use the `> **If [condition]:**` format so they stand out
- Do not add steps that were not described. If a step is missing, ask — do not invent
- Do not pad with generic advice about SOPs. Just write the document.
- Keep it to what is actually needed. A one-page SOP for a simple process is correct.

## After Writing

Once the SOP is written, offer one of:
- "Want me to save this as a file?"
- "Want me to add a checklist version at the end for quick reference?"

Do not offer both at once.

## What This Skill Does NOT Do

- Audit whether the process is a good process (that is the Workflow Auditor skill)
- Recommend tools or software
- Write SOPs for processes it has not been told about
- Produce generic templates — every SOP it writes is specific to what the user described
