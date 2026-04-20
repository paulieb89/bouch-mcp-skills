# OSCOLA Quick Reference

All citations from the UK Legal MCP tools are formatted to OSCOLA standard.

## Cases

```
Party v Party [Year] Court Report
R (Miller) v Secretary of State for Exiting the EU [2017] UKSC 5
Donoghue v Stevenson [1932] AC 562
```

Neutral citation format: `[Year] Court Number` — e.g. `[2023] EWCA Civ 12`

## Legislation

```
Name of Act Year, s.N(N)(n)
Human Rights Act 1998, s 3(1)
Equality Act 2010, s 149
```

Note: OSCOLA omits commas between Act name and year, and uses `s` not `s.`.

## Hansard

```
HC Deb [date] vol [N] col [N]
HL Deb [date] vol [N] col [N]
HC Deb 3 February 2020, vol 670, col 774
```

## Paragraph references in judgments

Paragraph numbers in square brackets, not page numbers:

```
Miller (n 3) [43]
R (Miller) v Secretary of State [2017] UKSC 5, [43]
```

## Short forms

After first full citation, use:
- Cases: short party name + `(n N)` where N is footnote number
- Acts: short popular name — `HRA 1998, s 3`
- `ibid` for immediately preceding source

## The UK Legal MCP tools return:

- Case law: neutral citations (`[Year] COURT Number`) — OSCOLA-ready
- Legislation: section references with in-force status — insert directly into citations
- `citations_parse`: extracts existing OSCOLA citations from text you paste
- `citations_resolve`: converts neutral citation to canonical TNA URL for verification
