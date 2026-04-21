#!/usr/bin/env python3
"""Render the DD report from a markdown template.

Consumes: raw MCP data, enriched signals, verdict.
Produces: filled markdown report at --output.

Template uses {{dotted.path}} placeholders. Missing values render as "—"
(en dash) rather than crashing, so partial data still produces a readable
document with gaps flagged.

Run standalone:
    python render_check.py --raw raw.json --enriched enriched.json \
        --verdict verdict.json --template ../assets/dd-report-template.md \
        --output report.md
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\{\{([\w\.\-]+)\}\}")


def resolve(ctx: dict[str, Any], path: str) -> Any:
    cur: Any = ctx
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
        if cur is None:
            return None
    return cur


def format_value(val: Any) -> str:
    if val is None:
        return "—"
    if isinstance(val, bool):
        return "yes" if val else "no"
    if isinstance(val, float):
        return f"{val:,.1f}" if val % 1 else f"{int(val):,}"
    if isinstance(val, int):
        return f"{val:,}"
    if isinstance(val, list):
        return ", ".join(str(v) for v in val) if val else "—"
    return str(val)


def _officers_md(active_officers: list[dict]) -> str:
    if not active_officers:
        return "_No active officers listed._"
    lines = []
    for o in active_officers:
        parts = [f"**{o.get('name') or '—'}**"]
        if o.get("role"):
            parts.append(str(o["role"]))
        if o.get("appointed_on"):
            parts.append(f"appointed {o['appointed_on']}")
        if o.get("country_of_residence"):
            parts.append(str(o["country_of_residence"]))
        ac = o.get("appointment_count")
        if ac:
            parts.append(f"{ac} appointments")
        lines.append("- " + " · ".join(parts))
    return "\n".join(lines)


def _psc_entries_md(entries: list[dict]) -> str:
    if not entries:
        return "_No active PSC entries._"
    lines = []
    for p in entries:
        parts = [f"**{p.get('name') or '—'}** ({p.get('kind') or 'unknown kind'})"]
        if p.get("country_of_residence"):
            parts.append(str(p["country_of_residence"]))
        if p.get("notified_on"):
            parts.append(f"notified {p['notified_on']}")
        if p.get("natures_of_control"):
            parts.append(", ".join(p["natures_of_control"]))
        lines.append("- " + " · ".join(parts))
    return "\n".join(lines)


def _disqualification_summary_md(disq: dict) -> str:
    if disq.get("checked_officer_count", 0) == 0:
        return "_No officers checked — disqualification lookup skipped._"
    if disq.get("hit_count", 0) == 0:
        return f"No disqualification hits across {disq['checked_officer_count']} active officer(s)."
    active = "**YES**" if disq.get("any_current_disqualification") else "no"
    historic = "**YES**" if disq.get("any_historic_disqualification") else "no"
    return (f"{disq['hit_count']} officer(s) matched against the disqualified register. "
            f"Active disqualification on a current officer: {active}. "
            f"Historic disqualification within window: {historic}.")


def _disqualification_hits_md(disq: dict) -> str:
    details = disq.get("details") or []
    if not details:
        return ""
    lines = ["### Disqualification details\n"]
    for d in details:
        flag = "🔴 ACTIVE" if d.get("active") else "⚪️ historic"
        lines.append(f"- {flag} — **{d.get('officer_name')}** matched as *{d.get('matched_name')}*")
        lines.append(f"  - From {d.get('disqualified_from') or '—'} to {d.get('disqualified_until') or '—'}")
        if d.get("reason"):
            lines.append(f"  - Reason: {d['reason']}")
        companies = d.get("company_names")
        if companies:
            preview = ", ".join(list(companies)[:3])
            extra = f" (+{len(companies) - 3} more)" if len(companies) > 3 else ""
            lines.append(f"  - Companies named: {preview}{extra}")
    return "\n".join(lines)


def _insolvency_summary_md(ins: dict) -> str:
    if ins.get("notice_count", 0) == 0:
        return "No Gazette notices found."
    parts = [f"{ins['notice_count']} notice(s) found"]
    if ins.get("winding_up_order_ever"):
        parts.append("**winding-up order in history**")
    if ins.get("recent_winding_up_petition_months") is not None:
        parts.append(f"most recent winding-up petition {ins['recent_winding_up_petition_months']}mo ago")
    if ins.get("recent_cvl_months") is not None:
        parts.append(f"CVL event {ins['recent_cvl_months']}mo ago")
    return "; ".join(parts) + "."


def _insolvency_notices_md(ins: dict) -> str:
    notices = ins.get("notices") or []
    if not notices:
        return ""
    lines = ["### Notices (severity-ranked)\n"]
    for n in notices:
        when = f"{n.get('months_ago')}mo ago" if n.get("months_ago") is not None else n.get("date", "—")
        lines.append(f"- **{n.get('notice_type')}** (severity {n.get('severity')}) · {when}")
        if n.get("title"):
            lines.append(f"  - {n['title']}")
    return "\n".join(lines)


def _psc_notes_md(psc: dict) -> str:
    notes = []
    if psc.get("overseas_corporate_count", 0) > 0:
        notes.append(f"- {psc['overseas_corporate_count']} overseas corporate PSC(s) — beneficial owner may be outside UK disclosure.")
    if psc.get("missing_ubo"):
        notes.append("- No named individual PSC: ultimate beneficial owner is not identified in the UK register.")
    if not notes:
        return ""
    return "**PSC notes:**\n" + "\n".join(notes)


def _filings_notes_md(filings: dict) -> str:
    notes = filings.get("notes") or []
    if not notes:
        return ""
    return "**Filing notes:**\n" + "\n".join(f"- {n}" for n in notes)


def _vat_notes_md(vat: dict) -> str:
    notes = []
    if vat.get("valid") is False:
        notes.append("- VAT number returned invalid by HMRC.")
    if vat.get("address_match") is False:
        notes.append("- VAT trading address does not match Companies House registered office postcode.")
    if not notes:
        return ""
    return "**VAT notes:**\n" + "\n".join(notes)


def _scope_not_checked_md(raw: dict, enriched: dict) -> str:
    missing = []
    if not raw.get("vat_validate"):
        missing.append("- VAT registration (no VAT number supplied).")
    if not raw.get("disqualified_lookups"):
        missing.append("- Director disqualification (not run for this report).")
    if not raw.get("gazette_insolvency"):
        missing.append("- Gazette insolvency (not fetched).")
    if not raw.get("land_title_search"):
        missing.append("- Land Registry ownership (not requested).")
    missing.append("- Sanctions screening (HMT/OFAC) — not available via this skill.")
    missing.append("- PEP (politically exposed persons) screening — not available via this skill.")
    missing.append("- Trade references, management interviews, or forensic accounting.")
    return "\n".join(missing)


def _verdict_reasons_md(verdict: dict) -> str:
    reasons = verdict.get("reasons") or []
    if not reasons:
        return "_No scoring rules applied._"
    lines = []
    for r in reasons:
        status = r.get("status", "—")
        icon = {"pass": "✓", "watch": "⚠", "fail": "✗", "skipped": "·", "unknown": "?"}.get(status, "?")
        detail = r.get("detail") or "—"
        weight = r.get("weight", 0)
        lines.append(f"- {icon} **{r.get('check')}** (weight {weight}) — {detail}")
    return "\n".join(lines)


def build_context(raw: dict, enriched: dict, verdict: dict) -> dict:
    profile = raw.get("company_profile") or {}
    address = profile.get("registered_office_address") or {}
    address_str = ", ".join(
        str(v) for v in [
            address.get("address_line_1"),
            address.get("address_line_2"),
            address.get("locality"),
            address.get("postal_code"),
        ] if v
    ) or "—"

    filings = enriched.get("filings") or {}
    officers = enriched.get("officers") or {}
    psc = enriched.get("psc") or {}
    disq = enriched.get("disqualification") or {}
    ins = enriched.get("insolvency") or {}
    vat = enriched.get("vat") or {}

    conf = profile.get("confirmation_statement") or {}
    accounts = profile.get("accounts") or {}

    return {
        "meta": {
            "date": date.today().isoformat(),
            "profile": verdict.get("criteria_profile") or "defaults",
        },
        "company": {
            "name": profile.get("company_name") or "—",
            "number": profile.get("company_number") or "—",
            "status": profile.get("company_status") or "—",
            "type": profile.get("company_type") or "—",
            "date_of_creation": profile.get("date_of_creation") or "—",
            "registered_office": address_str,
            "sic_codes": profile.get("sic_codes") or [],
            "has_charges": "yes" if profile.get("has_charges") else "no",
        },
        "filings": {
            "confirmation_status": "overdue" if conf.get("overdue") else "up-to-date",
            "confirmation_next_due": conf.get("next_due") or "—",
            "confirmation_overdue_days": filings.get("confirmation_overdue_days"),
            "accounts_status": "overdue" if accounts.get("overdue") else "up-to-date",
            "accounts_next_due": accounts.get("next_due") or "—",
            "accounts_overdue_days": filings.get("accounts_overdue_days"),
            "notes_md": _filings_notes_md(filings),
        },
        "officers": {
            "active_md": _officers_md(officers.get("active_officers") or []),
            "high_appointment_count_flag": len(officers.get("high_appointment_count_officers") or []),
        },
        "psc": {
            "entries_md": _psc_entries_md(psc.get("entries") or []),
            "overseas_corporate_count": psc.get("overseas_corporate_count") or 0,
            "missing_ubo": "yes" if psc.get("missing_ubo") else "no",
            "notes_md": _psc_notes_md(psc),
        },
        "disqualification": {
            "summary_md": _disqualification_summary_md(disq),
            "hits_md": _disqualification_hits_md(disq),
        },
        "insolvency": {
            "summary_md": _insolvency_summary_md(ins),
            "notices_md": _insolvency_notices_md(ins),
        },
        "vat": {
            "status": ("valid" if vat.get("valid") else "invalid") if vat.get("valid") is not None else "not checked",
            "trading_name": vat.get("trading_name") or "—",
            "trading_address": vat.get("trading_address") or "—",
            "address_match": ("yes" if vat.get("address_match") else "no") if vat.get("address_match") is not None else "—",
            "notes_md": _vat_notes_md(vat),
        },
        "scope": {
            "not_checked_md": _scope_not_checked_md(raw, enriched),
        },
        "verdict": {
            "decision": verdict.get("decision") or "—",
            "score_pct": verdict.get("score_pct") or "—",
            "score_earned": verdict.get("score_earned") or "—",
            "score_max": verdict.get("score_max") or "—",
            "reasons_md": _verdict_reasons_md(verdict),
        },
    }


def render(template: str, ctx: dict) -> str:
    def sub(match: re.Match) -> str:
        path = match.group(1)
        val = resolve(ctx, path)
        return format_value(val)
    return PLACEHOLDER_RE.sub(sub, template)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raw", required=True)
    p.add_argument("--enriched", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--template", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    raw = json.loads(Path(args.raw).read_text())
    enriched = json.loads(Path(args.enriched).read_text())
    verdict = json.loads(Path(args.verdict).read_text())
    template = Path(args.template).read_text()

    ctx = build_context(raw, enriched, verdict)
    rendered = render(template, ctx)
    Path(args.output).write_text(rendered)
    print(f"Wrote {args.output} ({len(rendered)} chars, verdict={verdict.get('decision')}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
