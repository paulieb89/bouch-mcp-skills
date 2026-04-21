#!/usr/bin/env python3
"""Enrich raw DD data with derived signals.

Consumes: raw MCP data saved by the orchestrating LLM (/tmp/dd-raw.json).
Produces: enriched data (/tmp/dd-enriched.json) with computed signals.

Signals computed:
  - officer_churn: resignations in the last 12 months
  - high_appointment_count_officers: officers with appointment_count >= threshold
  - disqualification_hits: matches between active officers and disqualified_search results
  - overseas_corporate_psc_count: number of non-UK corporate PSCs
  - missing_ubo: whether any individual PSC is identified (not just corporate entities)
  - address_discrepancy: VAT trading address vs Companies House registered office
  - filing_overdue_days: days overdue for confirmation and accounts

Run standalone:
    python cross_reference.py --input /tmp/dd-raw.json --output /tmp/dd-enriched.json
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _days_since(d: date | None, reference: date | None = None) -> int | None:
    if d is None:
        return None
    ref = reference or date.today()
    return (ref - d).days


def _normalise_name(name: str) -> str:
    """Case-fold, strip titles/suffixes, collapse whitespace for matching."""
    if not name:
        return ""
    n = name.strip().lower()
    for prefix in ("mr ", "mrs ", "ms ", "miss ", "dr ", "sir ", "dame ", "lord ", "lady "):
        if n.startswith(prefix):
            n = n[len(prefix):]
            break
    for suffix in (" obe", " mbe", " cbe", " kbe", " dbe"):
        if n.endswith(suffix):
            n = n[: -len(suffix)]
    n = re.sub(r"[^\w\s'-]", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n


def _names_match(a: str, b: str) -> bool:
    """Conservative name match: normalised forms equal, OR same token set
    (order-insensitive). Handles the SURNAME, First vs First SURNAME split
    between Companies House officer records and the disqualified register.
    """
    an, bn = _normalise_name(a), _normalise_name(b)
    if not an or not bn:
        return False
    if an == bn:
        return True
    aparts, bparts = set(an.split()), set(bn.split())
    if len(aparts) >= 2 and aparts == bparts:
        return True
    # Fall back to first + last positional match for 2-token names
    alist, blist = an.split(), bn.split()
    if len(alist) >= 2 and len(blist) >= 2:
        return alist[0] == blist[0] and alist[-1] == blist[-1]
    return False


def enrich_filings(raw: dict) -> dict:
    profile = raw.get("company_profile") or {}
    accounts = profile.get("accounts") or {}
    conf = profile.get("confirmation_statement") or {}

    conf_next_due = _parse_date(conf.get("next_due"))
    accounts_next_due = _parse_date(accounts.get("next_due"))

    conf_overdue = None
    if conf_next_due:
        delta = _days_since(conf_next_due)
        conf_overdue = max(0, delta) if delta is not None else None

    accounts_overdue = None
    if accounts_next_due:
        delta = _days_since(accounts_next_due)
        accounts_overdue = max(0, delta) if delta is not None else None

    notes = []
    if conf_overdue and conf_overdue > 30:
        notes.append(f"Confirmation statement {conf_overdue} days overdue — abandonment signal.")
    if accounts_overdue and accounts_overdue > 90:
        notes.append(f"Annual accounts {accounts_overdue} days overdue — distress or abandonment signal.")
    if conf.get("overdue") and accounts.get("overdue"):
        notes.append("Both confirmation statement AND accounts overdue — possible phoenix pattern or abandonment.")

    return {
        "confirmation_overdue_days": conf_overdue,
        "accounts_overdue_days": accounts_overdue,
        "confirmation_overdue_flag": bool(conf.get("overdue")),
        "accounts_overdue_flag": bool(accounts.get("overdue")),
        "notes": notes,
    }


def enrich_officers(raw: dict) -> dict:
    officers_result = raw.get("company_officers") or {}
    officers = officers_result.get("officers") or []

    active = [o for o in officers if not o.get("resigned_on")]
    resigned = [o for o in officers if o.get("resigned_on")]

    # Resignations in the last 12 months
    today = date.today()
    recent_resignations = 0
    for o in resigned:
        d = _parse_date(o.get("resigned_on"))
        if d and (today - d).days <= 365:
            recent_resignations += 1

    # Overseas directors percentage (active only)
    overseas_count = 0
    for o in active:
        residence = (o.get("country_of_residence") or "").lower()
        if residence and residence not in ("united kingdom", "england", "scotland", "wales", "northern ireland", "uk", "gb"):
            overseas_count += 1
    overseas_pct = round(100 * overseas_count / len(active), 1) if active else 0.0

    # High-appointment-count flag (nominee/phoenix pattern) — carried from MCP
    high_appointment_threshold = 10  # default, can be overridden by criteria
    high_count_officers = [
        {"name": o.get("name"), "appointment_count": o.get("appointment_count")}
        for o in active
        if (o.get("appointment_count") or 0) >= high_appointment_threshold
    ]

    return {
        "active_count": len(active),
        "resigned_count": len(resigned),
        "recent_resignations_12mo": recent_resignations,
        "overseas_director_count": overseas_count,
        "overseas_director_pct": overseas_pct,
        "high_appointment_count_officers": high_count_officers,
        "active_officers": [
            {
                "name": o.get("name"),
                "role": o.get("officer_role") or o.get("role"),
                "appointed_on": o.get("appointed_on"),
                "country_of_residence": o.get("country_of_residence"),
                "appointment_count": o.get("appointment_count"),
            }
            for o in active
        ],
    }


def enrich_psc(raw: dict) -> dict:
    psc_result = raw.get("company_psc") or {}
    pscs = psc_result.get("psc") or []

    active_pscs = [p for p in pscs if not p.get("ceased_on")]

    individual_pscs = [p for p in active_pscs if "individual" in (p.get("kind") or "").lower()]
    corporate_pscs = [p for p in active_pscs if "corporate" in (p.get("kind") or "").lower()]
    legal_pscs = [p for p in active_pscs if "legal-person" in (p.get("kind") or "").lower()]

    overseas_corporate = [
        p for p in corporate_pscs
        if (p.get("country_of_residence") or p.get("country_registered_in") or "").lower()
        not in ("united kingdom", "england", "scotland", "wales", "northern ireland", "uk", "gb", "")
    ]

    return {
        "total_active": len(active_pscs),
        "individual_count": len(individual_pscs),
        "corporate_count": len(corporate_pscs),
        "legal_person_count": len(legal_pscs),
        "overseas_corporate_count": len(overseas_corporate),
        "missing_ubo": len(individual_pscs) == 0 and len(corporate_pscs) > 0,
        "entries": [
            {
                "kind": p.get("kind"),
                "name": p.get("name"),
                "country_of_residence": p.get("country_of_residence") or p.get("country_registered_in"),
                "natures_of_control": p.get("natures_of_control") or [],
                "notified_on": p.get("notified_on"),
            }
            for p in active_pscs
        ],
    }


def enrich_disqualification(raw: dict, officers_enriched: dict) -> dict:
    """Match active officer names against disqualified_search results."""
    hits_by_officer = {}
    disqualified_lookups = raw.get("disqualified_lookups") or {}

    for officer in officers_enriched.get("active_officers", []):
        officer_name = officer.get("name") or ""
        lookup_key = _normalise_name(officer_name)
        search_result = (
            disqualified_lookups.get(lookup_key)
            or disqualified_lookups.get(officer_name)
            or disqualified_lookups.get(officer_name.lower())
            or {}
        )
        items = search_result.get("items") or []

        matches = []
        for item in items:
            if _names_match(officer_name, item.get("title", "") + " " + item.get("name", "")) or \
               _names_match(officer_name, item.get("name", "")):
                matches.append({
                    "officer_id": item.get("officer_id"),
                    "title_plus_name": f"{item.get('title', '')} {item.get('name', '')}".strip(),
                    "date_of_birth": item.get("date_of_birth"),
                    "snippet": item.get("snippet"),
                })
        if matches:
            hits_by_officer[officer_name] = matches

    # Profile details for any hits
    profile_details = raw.get("disqualified_profiles") or {}

    any_active = False
    any_historic = False
    today = date.today()
    details = []
    for officer_name, matches in hits_by_officer.items():
        for match in matches:
            oid = match.get("officer_id")
            profile = profile_details.get(oid) or {}
            for disq in (profile.get("disqualifications") or []):
                until = _parse_date(disq.get("disqualified_until"))
                is_active = until and until >= today
                if is_active:
                    any_active = True
                else:
                    any_historic = True
                details.append({
                    "officer_name": officer_name,
                    "matched_name": match.get("title_plus_name"),
                    "disqualified_from": disq.get("disqualified_from"),
                    "disqualified_until": disq.get("disqualified_until"),
                    "reason": disq.get("reason"),
                    "company_names": disq.get("company_names"),
                    "active": is_active,
                })

    return {
        "checked_officer_count": len(officers_enriched.get("active_officers", [])),
        "hit_count": len(hits_by_officer),
        "any_current_disqualification": any_active,
        "any_historic_disqualification": any_historic,
        "details": details,
    }


def enrich_insolvency(raw: dict) -> dict:
    result = raw.get("gazette_insolvency") or {}
    notices = result.get("notices") or []

    today = date.today()
    most_severe = 0
    winding_up_order = False
    recent_petition_months = None  # months since most recent winding-up petition
    recent_cvl_months = None

    enriched_notices = []
    for n in notices:
        notice_date = _parse_date(n.get("date"))
        notice_type = n.get("notice_type") or n.get("notice_code")
        severity = n.get("severity") or 0

        months_ago = None
        if notice_date:
            months_ago = round((today - notice_date).days / 30.4, 1)

        if str(notice_type) == "2443":
            winding_up_order = True
        if str(notice_type) == "2441" and months_ago is not None:
            if recent_petition_months is None or months_ago < recent_petition_months:
                recent_petition_months = months_ago
        if str(notice_type) == "2456" and months_ago is not None:
            if recent_cvl_months is None or months_ago < recent_cvl_months:
                recent_cvl_months = months_ago

        if severity > most_severe:
            most_severe = severity

        enriched_notices.append({
            "notice_type": notice_type,
            "date": n.get("date"),
            "months_ago": months_ago,
            "severity": severity,
            "title": n.get("title"),
            "content": n.get("content"),
        })

    return {
        "notice_count": len(notices),
        "most_severe": most_severe,
        "winding_up_order_ever": winding_up_order,
        "recent_winding_up_petition_months": recent_petition_months,
        "recent_cvl_months": recent_cvl_months,
        "notices": enriched_notices,
    }


def enrich_vat(raw: dict) -> dict:
    vat = raw.get("vat_validate") or {}
    profile = raw.get("company_profile") or {}
    ch_address = (profile.get("registered_office_address") or {})
    ch_address_str = ", ".join(
        str(v) for v in [
            ch_address.get("address_line_1"),
            ch_address.get("address_line_2"),
            ch_address.get("locality"),
            ch_address.get("postal_code"),
        ] if v
    )

    vat_address = vat.get("registered_address") or ""
    if isinstance(vat_address, dict):
        vat_address = ", ".join(str(v) for v in vat_address.values() if v)

    # Crude address comparison — postcode match is the most reliable signal
    postcode_re = re.compile(r"\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b", re.IGNORECASE)
    ch_pc = postcode_re.search(ch_address_str or "")
    vat_pc = postcode_re.search(vat_address or "")
    address_match = False
    if ch_pc and vat_pc:
        address_match = ch_pc.group(1).replace(" ", "").upper() == vat_pc.group(1).replace(" ", "").upper()

    return {
        "valid": vat.get("valid"),
        "vat_number": vat.get("vat_number"),
        "trading_name": vat.get("trading_name"),
        "trading_address": vat_address or None,
        "ch_registered_address": ch_address_str or None,
        "address_match": address_match if (ch_pc and vat_pc) else None,
    }


def cross_reference(raw: dict) -> dict:
    filings = enrich_filings(raw)
    officers = enrich_officers(raw)
    psc = enrich_psc(raw)
    disqualification = enrich_disqualification(raw, officers)
    insolvency = enrich_insolvency(raw)
    vat = enrich_vat(raw)

    return {
        "filings": filings,
        "officers": officers,
        "psc": psc,
        "disqualification": disqualification,
        "insolvency": insolvency,
        "vat": vat,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    raw = json.loads(Path(args.input).read_text())
    enriched = cross_reference(raw)
    Path(args.output).write_text(json.dumps(enriched, indent=2, default=str))
    print(f"Wrote {args.output} with signals for "
          f"{enriched['officers']['active_count']} active officers, "
          f"{enriched['psc']['total_active']} PSCs, "
          f"{enriched['insolvency']['notice_count']} Gazette notices.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
