---
name: legal-research
description: |
  Research a UK legal question and produce a structured brief. Finds relevant
  legislation with section text, case law, OSCOLA citations, and a plain
  English summary. Use when someone asks about UK law, compliance, case law,
  or "what does the law say about X". Requires the UK Legal MCP server.
allowed-tools:
  - mcp__claude_ai_uk-legal-tools__legislation_search
  - mcp__claude_ai_uk-legal-tools__legislation_get_toc
  - mcp__claude_ai_uk-legal-tools__legislation_get_section
  - mcp__claude_ai_uk-legal-tools__case_law_search
  - mcp__claude_ai_uk-legal-tools__case_law_get_judgment
  - mcp__claude_ai_uk-legal-tools__citations_parse
  - mcp__claude_ai_uk-legal-tools__citations_resolve
  - mcp__claude_ai_uk-legal-tools__parliament_search_hansard
  - mcp__claude_ai_uk-legal-tools__parliament_vibe_check
  - mcp__claude_ai_uk-legal-tools__parliament_find_member
  - mcp__claude_ai_uk-legal-tools__parliament_member_debates
  - mcp__claude_ai_uk-legal-tools__hmrc_search_guidance
---

# Legal Research Brief

Research a UK legal question using real statute text, case law, and parliamentary records. Produce a brief that a solicitor, business owner, or researcher can use.

## Thinking Like a Researcher

The user has a legal question. They might be a solicitor checking a point of law, a business owner worried about compliance, a paralegal preparing a brief, or a property investor checking their obligations. They want:

1. **What does the law actually say?** Not a summary from training data. The actual section text from legislation.gov.uk, with in-force status and territorial extent.
2. **What have the courts said about it?** Key cases that interpret or apply the relevant provisions. Principles extracted, not entire judgments quoted.
3. **Is there ambiguity?** If the law is unclear, say so. If there's a tension between statute and case law, explain it. The user needs to know where the risk sits.
4. **What should they do next?** This is a research brief, not legal advice. But "you should verify this with a solicitor" is more useful than nothing, and "the key section is s.21 Housing Act 1988, which is being amended by the Renters Reform Bill" gives them something to act on.

## What the Sources Give You

**legislation.gov.uk** has the authoritative text of UK Acts and Statutory Instruments. The API tells you whether a section is in force, when it commenced, and which parts of the UK it applies to. Always check extent — a provision that applies in England and Wales may not apply in Scotland.

**Find Case Law (TNA)** has UK court judgments. Search by keyword, filter by court level and date. The full judgment text is available in LegalDocML format.

**Hansard** has parliamentary debates. Useful when you need to understand legislative intent — what Parliament was trying to achieve when it passed a law. Also useful for assessing the political landscape around current or proposed legislation.

**HMRC guidance** covers tax questions — VAT, Making Tax Digital, and general tax guidance published on GOV.UK.

**OSCOLA citations** — the skill can parse legal citations from free text, resolve them to canonical URLs, and map the citation network within a judgment. Use this to verify references and build a proper bibliography.

## What You Don't Have

- Legal advice (you produce research, not opinions)
- Scottish or Northern Irish case law databases (TNA coverage is partial outside England and Wales)
- Unpublished judgments or tribunal decisions
- Solicitor-client privilege or case-specific advice
- EU retained law status post-Brexit (check manually)

## How to Work

**Understand the question first.** Parse it into: legal topic, jurisdiction (default England and Wales), and context (compliance, litigation, academic, general knowledge). If the question is vague, ask one clarifying question. Not two. Not three. One.

**Legislation first, then case law.** Find the relevant Act or SI, understand its structure, read the specific section. Then search for cases that interpret or apply it. This order matters — the statute is the primary source, case law interprets it.

**Check extent and in-force status on every section you cite.** A section that's been repealed or not yet commenced is worse than no answer at all.

**Hansard is optional but valuable.** If the statutory provision is ambiguous or recently enacted, Hansard debates can clarify what Parliament intended. Don't fetch it for every question — use it when interpretation is genuinely uncertain.

**Format citations properly.** OSCOLA style for all legislation and case law references. This isn't optional — it's the standard in UK legal practice and the user needs to be able to verify your sources.

## When Things Go Wrong

- **No legislation found:** The question might be common law (no statute, just case law). Or the user is using colloquial terms — "squatter's rights" means adverse possession, "being fired" means unfair dismissal. Translate and retry.
- **Section not in force:** Report it clearly. "Section 21 Housing Act 1988 is currently in force but will be abolished by the Renters' Rights Bill when commenced."
- **Conflicting case law:** This is valuable information, not a failure. Present both positions and which court level decided each.
- **Thin results:** Some areas of law have little case law. Say so. "No reported judgments found on this specific point" is honest and useful.

## Good vs Bad Output

**Good:** Leads with the answer in plain English. Cites the specific section. Quotes the relevant words of the statute. Lists 2-3 key cases with one-sentence principles. States territorial extent. Formats all citations in OSCOLA. Notes what wasn't found.

**Bad:** Summarises from training data without checking the actual text. Cites an Act without specifying the section. Misses that a provision has been repealed. Lists 10 cases with paragraph-long quotes from each. Doesn't check territorial extent.

## Formatting

British spelling. OSCOLA citations throughout. Section numbers as "s.21" not "Section 21" in running text. Acts in italics where the format supports it. Always state: this is legal research, not legal advice.
