# Filing Structure Detection

## Step 2a: Is This the Real Decision-Making Unit?

This is critical for UK subsidiaries of foreign parents. The legal entity your user wants to pitch may just be a filing structure with no operational marketing function. Sending a cold email to the UK address when decisions sit with the US or EU parent is the fastest way to get ignored.

Check for filing-structure indicators:

- **Shared central registered office.** Addresses like `7 Savoy Court, London WC2R 0EX` or `100 Bishopsgate` or similar City/Westminster corporate services addresses host dozens of unrelated subsidiaries. If the registered office is one of these, the UK entity is almost certainly a filing structure.
- **PSC is a foreign holding company.** If `company_psc` returns a corporate PSC that is itself a subsidiary of a foreign parent (look for Delaware LLCs, Cayman-incorporated entities, or named US/EU parent corporations), the decision-making sits abroad.
- **SIC code vs operational reality.** A company registered as "other software publishing" but whose actual studio, product, or brand activity clearly happens elsewhere (different city, different country) is a filing entity for a foreign operation.
- **Employee count vs public presence.** If the entity files micro-entity accounts (tiny headcount) but the brand is globally famous, the operational mass is elsewhere.

## What to Do If You Identify a Filing Structure

1. Still produce the brief for the UK entity — the user asked for it and the Companies House data is useful context.
2. In the **Person notes** section, lead with: "Decision-making is NOT at this UK entity. Target the parent's marketing organisation instead: [likely location and role]. The UK entity appears to be a filing structure for [parent name]."
3. In the **Watch out for** section, add: "Do not address the email to the UK subsidiary's office. It will not reach the right person."
4. When you draft the email in Step 8, address it to the parent's likely marketing contact, not anyone at the UK entity.

This is often the single most valuable observation in the brief. A cold email routed to the wrong entity is worse than no email at all.
