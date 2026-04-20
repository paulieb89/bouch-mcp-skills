---
name: workflow-auditor
description: |
  Analyse a business workflow to find where time is actually lost and
  recommend specific improvements. Use when someone asks to audit a process,
  find bottlenecks, improve efficiency, or figure out where AI could help
  in their business. Based on Theory of Constraints thinking.
license: Apache-2.0
compatibility: "No MCP required — standalone diagnostic skill."
metadata:
  author: bouch
  version: "2.0"
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
---

# Workflow Auditor

Analyse a business workflow to find the real constraint and recommend one specific, achievable improvement. No generic advice. No strategy documents. One thing that, if fixed, makes the biggest difference.

## Core Principle

Every workflow has one constraint. Improving anything other than the constraint is waste. The constraint is rarely where people think it is — they point at what annoys them most, which is often a symptom, not the cause.

## Workflow

**Step 1: Map the Process.** Ask the user to walk through the workflow step by step, as if explaining it to a new hire. Get timings, tools, people involved, and where things get stuck or wait. Do not assume. Take notes.

**Step 2: Classify time types.** For each step, categorise the time spent using the five types in `references/constraint-analysis.md`. Most people underestimate waiting, handoff, and setup time — these are usually bigger than the processing time itself.

**Step 3: Find the constraint.** The constraint is the step where work piles up and everything downstream is blocked. It has the highest ratio of non-processing time to processing time. See `references/constraint-analysis.md` for common constraint patterns.

**Step 4: Assess the Five C's.** Before recommending a fix, check Context, Control, Confidence, Coordination, and Capacity using the framework in `references/constraint-analysis.md`. If any are weak, fixing the technical constraint alone will not help.

**Step 5: Recommend one thing.** Specific, achievable this week, targeted at the constraint. Format it as:

```
The constraint: [what is actually slowing things down]
Why: [evidence from the workflow map]
Fix: [the specific action to take]
Expected result: [what should change if this works]
How to tell if it worked: [what to measure or observe]
```

## Output Rules

Be direct. Use the user's language, not consultant jargon. Do not recommend AI unless it solves the constraint — sometimes the answer is a spreadsheet or a phone call. One change at a time.

## Files in this skill

- `references/constraint-analysis.md` — five types of time, Five C's framework, and common constraint patterns
- `assets/audit-output-format.md` — recommendation block, what good looks like, and what this skill does not do
