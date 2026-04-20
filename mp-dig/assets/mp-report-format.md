<!-- This file is loaded by the mp-dig skill. It provides the output template. -->

# MP Report Format

## Good vs Bad Output

**Good:** Opens with a one-paragraph summary of who this MP is (party, constituency, role). Groups interests by category with amounts. Highlights anything unusual — large donations, recent property acquisitions, companies with issues. Links voting record to declared interests where relevant. States what wasn't checked.

**Bad:** Lists every interest with equal weight. Doesn't connect interests to voting patterns. Editorializes about whether interests are corrupt. Misses the company cross-reference. Presents a wall of dates and numbers without context.

---

## Report Template

```
## MP Profile: [Full Name] ([Party])

**Constituency:** [name]
**Role / title:** [Minister for X / Shadow X / Backbencher — if applicable]
**Report date:** [DD Month YYYY]
**Sources:** Parliament API, Register of Members' Financial Interests, Hansard, Division records[, Companies House]

### Summary
[One paragraph: who this person is, their role, any headline findings from the interests register. Keep it factual and neutral.]

### Declared Financial Interests

**Employment and earnings**
- [Source, amount/description, date]
- [Source, amount/description, date]

**Donations and sponsorship**
- [Donor name, amount, date, purpose if stated]

**Gifts and hospitality**
- [Source, description, date]

**Overseas visits**
- [Destination, funder, purpose, date]

**Land and property**
- [Description, location if declared]

**Shareholdings**
- [Company name, description]

**Family members employed**
- [Role, amount if declared]

**Other / misc**
- [Any other declared interests]

[If a category has no entries: "None declared."]

### Voting Record
*(include only if requested or directly relevant to the user's question)*

| Division | Date | Voted | Passed |
|----------|------|-------|--------|
| [Motion title] | [DD Mon YYYY] | [Aye / No / Absent] | [Yes / No] |

### Hansard Contributions
*(include only if requested or directly relevant)*

| Date | Chamber | Topic | Summary |
|------|---------|-------|---------|
| [date] | [Commons/Lords] | [topic keyword] | [one-line summary] |

### Company Cross-References
*(include for any companies appearing in the interests register)*

| Company | Number | Status | Directors | Notes |
|---------|--------|--------|-----------|-------|
| [name] | [00000000] | [Active/Dissolved] | [names] | [any flags] |

### What Wasn't Checked
Undeclared interests, IPSA expenses, council voting records, social media, private meetings or informal lobbying.

---
*Information from official public registers: Parliament Members API, Register of Members' Financial Interests, Hansard, Division records[, Companies House].*
```

---

## Notes on Using This Template

- Fill the Summary and Interests sections for every report. The other sections are conditional on what the user asked for.
- Neutral tone throughout — present facts, not opinions. "The register shows £X donated by Y on [date]" not "suspiciously large donation from Y".
- Group interests by category as shown. Don't mix categories in a flat list.
- The disclaimer line at the bottom is mandatory.
- State which registers were checked and which weren't in the "What Wasn't Checked" section.
