---
name: property-to-sheets
description: |
  Generate a UK property report and save it to Google Sheets as a formatted
  spreadsheet. Combines property data (comps, EPC, yield, stamp duty) with
  Google Sheets integration to produce a shareable, editable investment analysis.
  Use when someone says "put this in a spreadsheet", "save to Sheets",
  "I want a property spreadsheet", or needs property data in a format they
  can share or edit. Requires the Property MCP server and Google Sheets
  integration (via Strata/BOUCH Integrations MCP).
---

# Property Report to Google Sheets

You generate a UK property investment report and save it directly to Google Sheets as a formatted, structured spreadsheet. The output is a shareable document that an investor, agent, or analyst can edit, annotate, and forward.

## When to Use This Skill

- "Put this property analysis in a spreadsheet"
- "Save the report to Google Sheets"
- "I want a property spreadsheet I can share"
- "Create a Sheets report for this postcode"
- "Analyse [address] and put it in Sheets"
- Any property analysis request where the user wants an editable/shareable output

## Required Setup

This skill requires two connections:

1. **Property MCP server** (property-shared) — for property data
2. **Google Sheets integration** (via Strata) — for creating and writing to spreadsheets

**Property tools:**
- `property_comps` — comparable sales with EPC enrichment
- `property_epc` — energy performance certificate
- `rental_analysis` — rental market aggregates
- `rightmove_search` — live listings
- `property_yield` — yield calculation
- `stamp_duty` — SDLT calculation

**Sheets tools (via Strata):**
- `google_sheets_create_spreadsheet` — create a new spreadsheet with data
- `google_sheets_write_to_cell` — write to specific cells (for updates)
- `google_sheets_list_spreadsheets` — check for existing spreadsheets

## Workflow

### Step 1: Gather Property Data

Follow the same data-gathering workflow as a standard property report:

1. Call `property_comps` with the postcode (filter by property_type if known)
2. Call `property_epc` if a street address is available
3. Call `rental_analysis` with median comp price as purchase_price
4. Call `rightmove_search` for live rental listings (channel: RENT)
5. Call `property_yield` for formal yield calculation
6. Call `stamp_duty` with the asking or median price

Collect all the numbers before creating the spreadsheet.

### Step 2: Structure the Spreadsheet Data

Organise the data into a structured layout. The spreadsheet should have these sections:

**Row mapping:**
- Rows 1-2: Header (title, date, address)
- Rows 4-12: Comparable Sales summary
- Rows 14-22: Rental Analysis
- Rows 24-30: Yield Analysis
- Rows 32-36: Stamp Duty
- Rows 38-44: EPC Data (if available)
- Rows 46-55: Individual Comps (top 10)

### Step 3: Create the Spreadsheet

Call `google_sheets_create_spreadsheet` (via Strata execute_action) with:
- **title**: "Property Report — [Address/Postcode] — [Date]"
- **data**: JSON object mapping row numbers to column letters to values

Structure the data parameter as follows:

```json
{
  "1": {"A": "Property Report", "B": "[Address or Postcode]", "C": "[Date]"},
  "2": {"A": ""},
  "3": {"A": "COMPARABLE SALES", "B": "", "C": ""},
  "4": {"A": "Median Price", "B": "[value]", "C": "Source: Land Registry"},
  "5": {"A": "Mean Price", "B": "[value]", "C": ""},
  "6": {"A": "Price per sqft", "B": "[value]", "C": "EPC enriched"},
  "7": {"A": "Transaction Count", "B": "[value]", "C": "Last 24 months"},
  "8": {"A": "Price Range", "B": "[min] - [max]", "C": ""},
  "9": {"A": "Property Type Filter", "B": "[type or All]", "C": ""},
  "10": {"A": ""},
  "11": {"A": "RENTAL ANALYSIS", "B": "", "C": ""},
  "12": {"A": "Median Monthly Rent", "B": "[value]", "C": "Source: Rightmove"},
  "13": {"A": "Rental Listings", "B": "[count]", "C": "Currently on market"},
  "14": {"A": "Rent Range", "B": "[min] - [max]", "C": ""},
  "15": {"A": ""},
  "16": {"A": "YIELD", "B": "", "C": ""},
  "17": {"A": "Gross Yield", "B": "[value]%", "C": ""},
  "18": {"A": "Net Yield", "B": "[value]%", "C": "After service charge"},
  "19": {"A": ""},
  "20": {"A": "STAMP DUTY", "B": "", "C": ""},
  "21": {"A": "Purchase Price", "B": "[value]", "C": ""},
  "22": {"A": "SDLT Total", "B": "[value]", "C": "Additional property rate"},
  "23": {"A": "Effective Rate", "B": "[value]%", "C": ""},
  "24": {"A": ""},
  "25": {"A": "EPC", "B": "", "C": ""},
  "26": {"A": "Rating", "B": "[value]", "C": ""},
  "27": {"A": "Floor Area", "B": "[value] sqm", "C": ""},
  "28": {"A": "Construction Age", "B": "[value]", "C": ""}
}
```

### Step 4: Add Individual Comps

If there are more than 5 comparable sales, add a second section with the top 10 individual transactions. Use `google_sheets_write_to_cell` to add each row:

- Column A: Address
- Column B: Price
- Column C: Date
- Column D: Property type
- Column E: Price per sqft (if EPC matched)
- Column F: EPC rating (if matched)

### Step 5: Share the Link

The `google_sheets_create_spreadsheet` response includes a `spreadsheetUrl`. Present this to the user:

> "Your property report is ready: [spreadsheet URL]"

If the user also wants an email with the link, offer to draft one via `gmail_draft_email` (if Gmail integration is available via Strata).

## Output Format

In the conversation, present a brief summary alongside the link:

```
# Property Report: [Address/Postcode]

**Spreadsheet created**: [Google Sheets URL]

## Quick Summary
- Median comp price: £[X] ([N] sales)
- Gross yield: [X]%
- Stamp duty: £[X]
- EPC: [rating]

The full report with individual comps is in the spreadsheet.
[Optional: "Want me to email this to someone?"]
```

## Key Principles

- **Spreadsheet first.** The whole point of this skill is the Sheets output. Don't produce a long text report — put the data in the spreadsheet and give the user a link.
- **Clean structure.** Section headers in column A, values in column B, source/notes in column C. Consistent, scannable.
- **All numbers, no prose.** The spreadsheet should be data, not paragraphs. Save the narrative for the conversation summary.
- **Offer the email.** Many users want to send the spreadsheet to someone. If Gmail is available, offer to draft it.
- **Date everything.** Property data decays. Put the date in the title and header so the user knows when the data was pulled.
