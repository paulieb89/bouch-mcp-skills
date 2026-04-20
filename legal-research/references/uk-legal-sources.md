<!-- This file is loaded by the legal-research skill. It provides source descriptions and researcher framing. -->

# UK Legal Sources

## What the Sources Give You

**legislation.gov.uk** has the authoritative text of UK Acts and Statutory Instruments. The API tells you whether a section is in force, when it commenced, and which parts of the UK it applies to. Always check extent — a provision that applies in England and Wales may not apply in Scotland.

**Find Case Law (TNA)** has UK court judgments. `case_law_search` finds them by keyword, court, judge, party, or date. To read a specific judgment without blowing context, use the resource sub-paths:
- `judgment://{slug}/header` — metadata only (~1k tokens)
- `judgment://{slug}/index` — paragraph map (~4k tokens)
- `judgment://{slug}/para/{eId}` — individual paragraphs (~400–1700 tokens each)

For "what did the court say about X" questions, use `case_law_grep_judgment` to find matching paragraphs by pattern, then read just those paragraphs. Never pull the whole LegalDocML XML into context — a typical Supreme Court judgment is 50k+ tokens.

**Hansard** has parliamentary debates. Useful when you need to understand legislative intent — what Parliament was trying to achieve when it passed a law. Also useful for assessing the political landscape around current or proposed legislation.

**HMRC guidance** covers tax questions — VAT, Making Tax Digital, and general tax guidance published on GOV.UK. Search via `hmrc_search_guidance`.

**OSCOLA citations** — the skill can parse legal citations from free text, resolve them to canonical URLs, and map the citation network within a judgment. Use `citations_parse` and `citations_resolve` to verify references and build a proper bibliography.

---

## What You Don't Have

- Legal advice (you produce research, not opinions)
- Scottish or Northern Irish case law databases (TNA coverage is partial outside England and Wales)
- Unpublished judgments or tribunal decisions
- Solicitor-client privilege or case-specific advice
- EU retained law status post-Brexit (check manually)

Be clear about these gaps. The user needs to know what else to check.

---

## Thinking Like a Researcher

The user has a legal question. They might be a solicitor checking a point of law, a business owner worried about compliance, a paralegal preparing a brief, or a property investor checking their obligations. They want:

1. **What does the law actually say?** Not a summary from training data. The actual section text from legislation.gov.uk, with in-force status and territorial extent.
2. **What have the courts said about it?** Key cases that interpret or apply the relevant provisions. Principles extracted, not entire judgments quoted.
3. **Is there ambiguity?** If the law is unclear, say so. If there's a tension between statute and case law, explain it. The user needs to know where the risk sits.
4. **What should they do next?** This is a research brief, not legal advice. But "you should verify this with a solicitor" is more useful than nothing, and "the key section is s.21 Housing Act 1988, which is being amended by the Renters Reform Bill" gives them something to act on.

---

## OSCOLA Citation Format

OSCOLA is the standard citation style for UK legal practice. Always format citations correctly so the user can verify your sources.

**Acts of Parliament:**
_Housing Act 1988_
_Renters' Rights Bill_

**Section references (in running text):**
s.21, s.8, ss.1–3

**Cases:**
_R v Jones_ [2021] UKSC 10
_Donoghue v Stevenson_ [1932] AC 562

**Statutory Instruments:**
SI 2020/1234

**In a bibliography or references section:** spell out the full citation. In running text, use the short form after the first full mention.

**Citing a specific paragraph of a judgment:**
_R v Jones_ [2021] UKSC 10 [45] — where [45] is the paragraph number.
