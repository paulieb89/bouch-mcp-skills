---
name: legal-how-to
description: |
  A practical guide for UK lawyers and legal researchers using Claude with the
  UK Legal MCP server. Explains the five core research workflows — legislation
  lookup, case law drill-down, citation tracing, parliamentary intent, and HMRC
  guidance — with example prompts and real output. Use when a lawyer wants to
  understand what the tools can do or how to structure a legal research session.
license: Apache-2.0
compatibility: Requires the UK Legal MCP server (uk-legal-mcp). Connect via Claude Code, Cursor, Windsurf, or any MCP-compatible client.
metadata:
  author: bouch
  version: "1.0"
---

# UK Legal MCP — Lawyer's Guide

You have access to live UK legal data via real government APIs: legislation.gov.uk,
the National Archives Find Case Law, Hansard, and HMRC. This is not a training-data
summary — it is the actual text of Acts, SI provisions, and court judgments as they
stand today.

This guide walks you through five workflows with example prompts. Use whichever fits
your question.

---

## Workflow 1 — Find and read a statutory provision

**Use when:** You need the actual text of a section, not a summary.

**Example prompts:**
- "What does section 21 of the Housing Act 1988 say?"
- "Get me the table of contents for the Equality Act 2010."
- "What does section 172 Companies Act 2006 say, and is it in force?"

**What happens:** The tool searches legislation.gov.uk, reads the table of contents
to locate the section, retrieves the live CLML text, and reports territorial extent
(England/Wales/Scotland/NI) and in-force status.

**Key details:**
- Always checks extent — a provision may not apply in Scotland or Northern Ireland.
- Point-in-time research: add a date to get the law as it stood on a specific day
  (useful for historic transactions or disputes).
- Large statutes (Companies Act 2006, 1300+ sections) are paged — ask for a specific
  section rather than the whole Act.

---

## Workflow 2 — Find cases and read specific paragraphs

**Use when:** You need what the courts have said about a legal point.

**Example prompts:**
- "Find Supreme Court cases on indirect discrimination and proportionality."
- "Search for Court of Appeal decisions on section 21 notices and prescribed information."
- "What did the court say about the definition of 'woman' in For Women Scotland v Scottish Ministers?"

**What happens:**
1. `case_law_search` returns matching judgments with neutral citations, court, and dates.
2. Each result includes `next_steps` hints — no need to look up where to go next.
3. `case_law_grep_judgment` searches within a specific judgment for a keyword or phrase,
   returning matching paragraph eIds and snippets.
4. `read_resource` retrieves the verbatim paragraph text.

**The drill-down pattern:**
```
search → find the case → grep for your term → read the exact paragraph
```

This avoids pulling entire judgments into context. A Supreme Court judgment can be
50,000+ tokens. Grepping for "proportionate" and reading 3 paragraphs costs ~2,000.

**Court codes for filtering:**
`uksc` · `ukpc` · `ewca/civ` · `ewca/crim` · `ewhc/kb` · `ewhc/ch` · `ewhc/comm`
`ewhc/admin` · `ewhc/fam` · `ukut/iac` · `ukftt/tc` · `eat` · `nica`

---

## Workflow 3 — Trace a citation

**Use when:** You have a citation string and need to verify it, resolve it to a URL,
or understand a judgment's citation network.

**Example prompts:**
- "Parse the citations from this paragraph: [paste text]"
- "Resolve [2017] UKSC 27 to a canonical URL."
- "What does Essop v Home Office cite, and what has cited it since?"

**What happens:**
- `citations_parse` extracts OSCOLA-format citations from free text.
- `citations_resolve` converts a neutral citation to the TNA URL.
- `citations_network` maps what a judgment cites and which subsequent cases cite it —
  useful for checking whether a case has been approved, distinguished, or overruled.

---

## Workflow 4 — Check parliamentary intent (Pepper v Hart)

**Use when:** A statutory provision is ambiguous and you need evidence of what
Parliament intended when it passed the law.

**Example prompts:**
- "Search Hansard for debates on the Online Safety Bill, specifically on 'legal but harmful'."
- "What was the parliamentary reception of the Renters Reform Bill?"
- "Did any minister explain what 'woman' meant in the Equality Act debates?"

**What happens:**
- `parliament_search_hansard` searches the full record of Commons and Lords debates.
- `parliament_vibe_check` gives a quick read on how a piece of legislation or policy
  was received — useful for assessing political risk or finding dissenting voices.

**Note:** Hansard is admissible as an aid to statutory interpretation under *Pepper v Hart*
[1993] AC 593 where the legislation is ambiguous and a minister made a clear statement
on the precise point.

---

## Workflow 5 — Track live bills and HMRC guidance

**Use when:** You need to know the current status of pending legislation, or need
HMRC's official position on a tax question.

**Example prompts:**
- "What stage is the Employment Rights Bill at?"
- "Search for bills relating to leasehold reform currently before Parliament."
- "What is HMRC's guidance on input tax recovery for mixed-use buildings?"
- "What is the current VAT rate for children's car seats?"

**What happens:**
- `bills_search_bills` and `bills_get_bill` return current parliamentary stage, sponsors,
  and text of bills before Parliament.
- `hmrc_search_guidance` searches published HMRC guidance on GOV.UK.
- `hmrc_get_vat_rate` returns the current VAT liability for a supply category.

---

## What this is not

- **Not legal advice.** Output is research material. Verify before advising a client.
- **Not a case law database subscription.** Coverage is the TNA Find Case Law corpus —
  strong for appellate courts from ~2001 onwards, partial for older cases and tribunals.
- **Not EU law.** Post-Brexit retained EU law must be checked separately.
- **Not Westlaw or LexisNexis.** No headnotes, no catchwords, no editorial treatment.
  You get the raw judgment and statute text and work with it directly.

---

## Tips

**Be specific about the court.** "Find cases on breach of confidence" returns hundreds.
"Find Supreme Court cases on breach of confidence after 2015" returns a workable set.

**Use grep before reading.** Never ask for "the judgment on X" in full. Ask Claude to
grep the judgment for your term, then read the paragraphs that match.

**Check extent on every section you cite.** The tools report it. Use it.

**OSCOLA throughout.** All citations are formatted to OSCOLA standard — ready to drop
into a brief or advice note.

**Point-in-time legislation.** For historic disputes, add: "as it stood on [date]".
The legislation resource accepts a `?date=` parameter automatically.

---

## Quick References

- [All tools with inputs/outputs](references/tool-quick-ref.md)
- [OSCOLA citation format](references/oscola-quick-ref.md)
- [Copy-paste starter prompts](assets/starter-prompts.md)
