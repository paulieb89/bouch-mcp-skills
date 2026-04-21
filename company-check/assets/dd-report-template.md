# Due Diligence report — {{company.name}}

**Company number:** {{company.number}}
**Report date:** {{meta.date}}
**Criteria profile:** {{meta.profile}}

---

## Verdict

**{{verdict.decision}}** — {{verdict.score_pct}}% against the {{meta.profile}} profile ({{verdict.score_earned}} of {{verdict.score_max}} weighted points).

{{verdict.reasons_md}}

> Criteria-based scan against public UK registers. Not professional DD advice. Always verify before acting.

---

## Company snapshot

- **Status:** {{company.status}}
- **Incorporated:** {{company.date_of_creation}}
- **Type:** {{company.type}}
- **Registered office:** {{company.registered_office}}
- **SIC codes:** {{company.sic_codes}}
- **Has registered charges:** {{company.has_charges}}

## Filing compliance

- **Confirmation statement:** {{filings.confirmation_status}} (next due {{filings.confirmation_next_due}})
- **Annual accounts:** {{filings.accounts_status}} (next due {{filings.accounts_next_due}})
- **Confirmation overdue by:** {{filings.confirmation_overdue_days}} days
- **Accounts overdue by:** {{filings.accounts_overdue_days}} days

{{filings.notes_md}}

## Directors and beneficial ownership

### Active officers

{{officers.active_md}}

### Persons with significant control (PSC)

{{psc.entries_md}}

**Opacity flags:**
- Overseas corporate PSCs: {{psc.overseas_corporate_count}}
- Missing named ultimate beneficial owner: {{psc.missing_ubo}}
- Nominee-pattern officers (appointment count ≥ threshold): {{officers.high_appointment_count_flag}}

{{psc.notes_md}}

## Director disqualification check

{{disqualification.summary_md}}

{{disqualification.hits_md}}

## Insolvency history (Gazette)

{{insolvency.summary_md}}

{{insolvency.notices_md}}

## VAT

- **VAT status:** {{vat.status}}
- **Trading name:** {{vat.trading_name}}
- **Trading address:** {{vat.trading_address}}
- **Matches Companies House address:** {{vat.address_match}}

{{vat.notes_md}}

## What was NOT checked

{{scope.not_checked_md}}

## Disclaimer

Every finding above comes from an official UK register (Companies House, Gazette, HMRC, or the Disqualified Directors register) at the time of the report. Registers lag real-world events by days to weeks. This report does not replace professional due diligence, anti-money laundering screening, sanctions checks, or legal advice. It is designed to support those workflows, not substitute for them.

Data sources: Companies House · The Gazette · HMRC VAT · Companies House Register of Disqualified Directors.
