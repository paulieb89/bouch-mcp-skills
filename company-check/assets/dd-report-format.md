<!-- This file is loaded by the company-check skill. It provides the output template. -->

# Due Diligence Report Format

## Good vs Bad Output

**Good:** Leads with a clear assessment. Groups red flags together. Explains what the findings mean in context. States what wasn't checked.

**Bad:** Lists every Companies House field with no interpretation. Buries insolvency notices at the bottom. Doesn't explain why late filings matter. Presents a dissolved company the same way as an active one.

---

## Report Template

```
## Company Check: [Company Name] ([Company Number])

**Report date:** [DD Month YYYY]
**Registers checked:** [Companies House, The Gazette, HMRC VAT, Land Registry, Charity Commission — list those actually queried]

### Headline
[Active / Dissolved / In Liquidation] — [one sentence summary of what the user needs to know]

### Corporate Profile
- Incorporated: [DD Month YYYY]
- Registered address: [address]
- SIC code(s): [code — description]
- Status: [Active / Dissolved / In Liquidation / etc.]

### Filing Compliance
- Latest accounts filed: [period end date, filed date]
- Confirmation statement: [last filed date]
- Overdue filings: [Yes — [detail] / None found]

### Directors & PSC
**Directors:**
- [Full name] — appointed [DD Month YYYY]
- [Full name] — appointed [DD Month YYYY]

**Persons with Significant Control:**
- [Full name or entity name] — [% holding or nature of control] — from [date]
- [None registered — note this as a flag if the company is not newly incorporated]

### Red Flags
[Gazette notices / VAT issues / other concerns — or "None found"]
[Group and explain each flag. Don't list without context.]

### What Wasn't Checked
Credit history, County Court Judgments, personal credit of directors, trading history and revenue, undeclared beneficial ownership.

### Recommendation
[Proceed / Investigate further / Walk away] — [brief rationale: what drove this assessment]
```

---

## Notes on Using This Template

- Fill every section. "None found" is a valid answer — leave no section blank.
- Lead with the Headline. The user reads top to bottom. Don't make them hunt for the verdict.
- Red flags go in the Red Flags section, not buried in Corporate Profile.
- The "What Wasn't Checked" section is mandatory — it manages the user's expectations and protects you from over-claiming.
- Recommendation must include a rationale. "Proceed" with no explanation is useless.
