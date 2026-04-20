---
name: bouch-voice
description: |
  Apply BOUCH voice rules to any UK business copy: websites, emails,
  proposals, case studies, or LinkedIn. Covers language to use and avoid,
  tone, British spelling, and formatting. Use when writing, rewriting,
  reviewing, or generating copy for a UK SMB audience.
license: Apache-2.0
compatibility: "No MCP required — standalone copywriting skill."
metadata:
  author: bouch
  version: "2.0"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# BOUCH Voice & Copy

BOUCH sounds like a tradesperson's site, not a tech agency. Grounded, no-nonsense, practical. "Here's what I do, here's the evidence, let's talk." Not inspirational. Not evangelical. Not slick.

Use one of three modes depending on the task.

## Three Modes

**Mode 1: Rewrite.** Run the humaniser skill first to strip AI patterns (em dashes, AI vocabulary, rule of three, promotional inflation). Then apply the BOUCH-specific rules in `references/voice-rules.md`. Return rewritten copy with a brief note on what changed.

**Mode 2: New Angles.** Generate 2-3 distinct copy angles for a section or topic. Each angle should have a different hook (problem-first, evidence-first, cynicism-disarming). Label them clearly. No inspirational framing. No buzzwords.

**Mode 3: Voice Review.** Review copy against the rules. Return: Pass / Fix / Fail verdict, specific lines that violate the voice rules, one-line fix for each violation.

## Key Messages

Use these as the foundation for any new angles:

1. The bottleneck is human, not technical. Most teams have the tools. The problem is nobody knows how to use them in their actual workflow.
2. One workflow at a time. Not a strategy. Not a roadmap. One thing that saves time, done properly.
3. Paul builds things. This is not theory. Live URLs, real clients, real outcomes.
4. Practical and individual. Every person in a team needs something different. One-size training does not work.
5. The audit comes first. Start by finding where time is actually lost, not where it looks like it's lost.

## Before / After Examples

**Before (AI-generated, generic):**
> "At BOUCH, we leverage cutting-edge AI solutions to transform your business workflows, driving efficiency and unlocking the potential of your team."

**After (BOUCH voice):**
> "Most teams have the tools. The problem is time — nobody has the space to figure out what actually works. That's what the audit is for."

---

**Before (inspirational, vague):**
> "AI is revolutionising the way businesses operate. Don't get left behind."

**After (specific, grounded):**
> "Your competitors aren't using AI better than you. Most of them bought the same tools and hit the same wall. The difference is in the workflow, not the software."

## Files in this skill

- `references/voice-rules.md` — language to use and avoid, formatting rules, and audience context
- `references/page-notes.md` — page-specific guidance for homepage, services, tools, work, and about
- `scripts/check_voice.py` — validates copy against BOUCH voice rules: banned words, em dashes, superlative claims, American spellings (exit 0=pass, 1=fail, 2=error)
