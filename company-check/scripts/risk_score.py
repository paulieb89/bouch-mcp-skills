#!/usr/bin/env python3
"""Score enriched DD data against criteria JSON. Produce CLEAR / WATCH / FLAG verdict.

Consumes: enriched data from cross_reference.py, criteria JSON (one of
the presets in assets/ or a user-customised copy).

Each check returns {check, status (pass/watch/fail/skipped), detail, weight, pass}.
Weighted score → decision:
  - Any hard-block fail (disqualification current, winding-up order ever
    when blocked by criteria) → FLAG regardless of score
  - score_pct >= 85 AND no fails → CLEAR
  - 50 <= score_pct < 85 OR one fail → WATCH
  - score_pct < 50 OR two+ fails → FLAG

Run standalone:
    python risk_score.py --enriched enriched.json \
        --criteria ../assets/dd-criteria-lender.json \
        --output verdict.json
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Individual checks — each returns a result dict with pass/status/detail/weight
# ---------------------------------------------------------------------------

def check_filings(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("filings") or {}
    weight = cfg.get("weight", 0)
    filings = enriched.get("filings") or {}

    conf_overdue = filings.get("confirmation_overdue_days")
    accounts_overdue = filings.get("accounts_overdue_days")
    max_conf = cfg.get("max_confirmation_statement_overdue_days", 30)
    max_accounts = cfg.get("max_accounts_overdue_days", 90)

    problems = []
    if conf_overdue is not None and conf_overdue > max_conf:
        problems.append(f"confirmation statement {conf_overdue}d overdue (limit {max_conf}d)")
    if accounts_overdue is not None and accounts_overdue > max_accounts:
        problems.append(f"accounts {accounts_overdue}d overdue (limit {max_accounts}d)")

    if not problems:
        return {"check": "filings", "status": "pass",
                "detail": "filings within tolerance",
                "pass": True, "weight": weight, "hard_block": False}
    return {"check": "filings", "status": "fail",
            "detail": "; ".join(problems),
            "pass": False, "weight": weight, "hard_block": False}


def check_officers(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("officers") or {}
    weight = cfg.get("weight", 0)
    officers = enriched.get("officers") or {}

    churn = officers.get("recent_resignations_12mo") or 0
    max_churn = cfg.get("max_director_resignations_12mo", 3)
    overseas_pct = officers.get("overseas_director_pct") or 0
    max_overseas_pct = cfg.get("overseas_directors_pct_threshold", 50)
    threshold = cfg.get("flag_appointment_count_threshold", 10)
    high_count = [
        o for o in officers.get("active_officers", [])
        if (o.get("appointment_count") or 0) >= threshold
    ]

    problems = []
    if churn > max_churn:
        problems.append(f"{churn} director resignations in 12mo (limit {max_churn})")
    if overseas_pct > max_overseas_pct:
        problems.append(f"{overseas_pct}% overseas-resident directors (limit {max_overseas_pct}%)")
    if high_count:
        names = ", ".join(o.get("name", "?") for o in high_count)
        problems.append(f"{len(high_count)} officer(s) with ≥{threshold} appointments: {names}")

    if not problems:
        return {"check": "officers", "status": "pass",
                "detail": "officer pattern within tolerance",
                "pass": True, "weight": weight, "hard_block": False}
    # Appointment count alone = watch; resignation churn or overseas is fail
    status = "fail" if (churn > max_churn or overseas_pct > max_overseas_pct) else "watch"
    return {"check": "officers", "status": status,
            "detail": "; ".join(problems),
            "pass": status == "watch", "weight": weight, "hard_block": False}


def check_psc(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("psc") or {}
    weight = cfg.get("weight", 0)
    psc = enriched.get("psc") or {}

    problems = []
    if cfg.get("flag_overseas_corporate_psc") and (psc.get("overseas_corporate_count") or 0) > 0:
        problems.append(f"{psc['overseas_corporate_count']} overseas corporate PSC(s)")
    if cfg.get("require_named_ultimate_beneficial_owner") and psc.get("missing_ubo"):
        problems.append("no named individual PSC (corporate-only ownership chain)")

    if not problems:
        return {"check": "psc", "status": "pass",
                "detail": "beneficial ownership traceable",
                "pass": True, "weight": weight, "hard_block": False}
    return {"check": "psc", "status": "fail",
            "detail": "; ".join(problems),
            "pass": False, "weight": weight, "hard_block": False}


def check_disqualification(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("disqualification") or {}
    weight = cfg.get("weight", 0)
    disq = enriched.get("disqualification") or {}

    if disq.get("checked_officer_count", 0) == 0:
        return {"check": "disqualification", "status": "skipped",
                "detail": "no officers checked (Lane B or no officers listed)",
                "pass": True, "weight": 0, "hard_block": False}

    # Current disqualification
    if cfg.get("block_any_current_disqualification") and disq.get("any_current_disqualification"):
        return {"check": "disqualification", "status": "fail",
                "detail": "active disqualification order on a current officer",
                "pass": False, "weight": weight, "hard_block": True}

    # Historic disqualification within the window
    window_years = cfg.get("block_any_historic_disqualification_years", 0)
    if window_years and disq.get("any_historic_disqualification"):
        today = date.today()
        in_window = False
        for detail in disq.get("details", []):
            until = _parse_date(detail.get("disqualified_until"))
            if until and (today - until).days / 365.25 <= window_years:
                in_window = True
                break
        if in_window:
            return {"check": "disqualification", "status": "fail",
                    "detail": f"historic disqualification within {window_years}-year window",
                    "pass": False, "weight": weight, "hard_block": False}

    return {"check": "disqualification", "status": "pass",
            "detail": f"no disqualification hits across {disq['checked_officer_count']} officer(s)",
            "pass": True, "weight": weight, "hard_block": False}


def check_insolvency(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("insolvency") or {}
    weight = cfg.get("weight", 0)
    ins = enriched.get("insolvency") or {}

    if cfg.get("block_winding_up_order_ever") and ins.get("winding_up_order_ever"):
        return {"check": "insolvency", "status": "fail",
                "detail": "winding-up order in company history",
                "pass": False, "weight": weight, "hard_block": True}

    petition_months = ins.get("recent_winding_up_petition_months")
    window_petition = cfg.get("block_winding_up_petition_months", 0)
    if window_petition and petition_months is not None and petition_months <= window_petition:
        return {"check": "insolvency", "status": "fail",
                "detail": f"winding-up petition {petition_months} months ago (within {window_petition}-month window)",
                "pass": False, "weight": weight, "hard_block": False}

    cvl_months = ins.get("recent_cvl_months")
    window_cvl = cfg.get("watch_creditors_voluntary_liquidation_months", 0)
    if window_cvl and cvl_months is not None and cvl_months <= window_cvl:
        return {"check": "insolvency", "status": "watch",
                "detail": f"creditors' voluntary liquidation event {cvl_months} months ago",
                "pass": True, "weight": weight, "hard_block": False}

    return {"check": "insolvency", "status": "pass",
            "detail": "no insolvency hits in the window",
            "pass": True, "weight": weight, "hard_block": False}


def check_charges(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("charges") or {}
    weight = cfg.get("weight", 0)
    window_months = cfg.get("flag_recent_charges_months", 0)

    if not weight or not window_months:
        return {"check": "charges", "status": "skipped",
                "detail": "not weighted in this profile",
                "pass": True, "weight": 0, "hard_block": False}

    # Charges detail requires a separate MCP call we don't currently make (cheap
    # addition later). For now, signal only via the company_profile.has_charges flag.
    raw_has_charges = enriched.get("_has_charges_from_profile")
    if raw_has_charges is None:
        return {"check": "charges", "status": "unknown",
                "detail": "charges register not fetched",
                "pass": False, "weight": weight, "hard_block": False}
    if raw_has_charges:
        return {"check": "charges", "status": "watch",
                "detail": f"registered charges exist (dates within last {window_months}mo not verified)",
                "pass": True, "weight": weight, "hard_block": False}
    return {"check": "charges", "status": "pass",
            "detail": "no registered charges",
            "pass": True, "weight": weight, "hard_block": False}


def check_vat(enriched: dict, criteria: dict) -> dict:
    cfg = criteria.get("vat") or {}
    weight = cfg.get("weight", 0)
    vat = enriched.get("vat") or {}

    if vat.get("valid") is None:
        return {"check": "vat", "status": "skipped",
                "detail": "no VAT number supplied or not validated",
                "pass": True, "weight": 0, "hard_block": False}

    problems = []
    if cfg.get("require_valid_vat_if_trading") and vat.get("valid") is False:
        problems.append("VAT number invalid")
    if cfg.get("flag_address_discrepancy") and vat.get("address_match") is False:
        problems.append("VAT trading address does not match Companies House")

    if not problems:
        return {"check": "vat", "status": "pass",
                "detail": "VAT valid, addresses aligned (or address match not applicable)",
                "pass": True, "weight": weight, "hard_block": False}
    return {"check": "vat", "status": "fail",
            "detail": "; ".join(problems),
            "pass": False, "weight": weight, "hard_block": False}


CHECKS = [
    check_filings,
    check_officers,
    check_psc,
    check_disqualification,
    check_insolvency,
    check_charges,
    check_vat,
]


def score(enriched: dict, criteria: dict) -> dict:
    # Add the charges-from-profile signal into the enriched dict for the charges check
    raw_has_charges = (
        (enriched.get("_raw", {}) or {}).get("company_profile", {}) or {}
    ).get("has_charges")
    enriched_with_ctx = {**enriched, "_has_charges_from_profile": raw_has_charges}

    results = [check(enriched_with_ctx, criteria) for check in CHECKS]

    total_weight = sum(r["weight"] for r in results)
    earned = sum(r["weight"] for r in results if r.get("pass"))
    fail_count = sum(1 for r in results if r["status"] == "fail")
    hard_block = any(r.get("hard_block") for r in results)

    score_pct = round(earned / total_weight * 100, 1) if total_weight else 0.0

    if hard_block or fail_count >= 2 or score_pct < 50:
        decision = "FLAG"
    elif fail_count == 1 or score_pct < 85:
        decision = "WATCH"
    else:
        decision = "CLEAR"

    return {
        "decision": decision,
        "score_pct": score_pct,
        "score_earned": earned,
        "score_max": total_weight,
        "fail_count": fail_count,
        "hard_block": hard_block,
        "criteria_source": criteria.get("_source", "defaults"),
        "criteria_profile": criteria.get("_profile", "defaults"),
        "reasons": results,
        "disclaimer": (
            "Criteria-based scan against UK public registers. CLEAR/WATCH/FLAG "
            "reflects the supplied criteria profile only. Always verify before acting."
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--enriched", required=True)
    p.add_argument("--raw", help="Optional raw file, used to pull has_charges signal")
    p.add_argument("--criteria", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    enriched = json.loads(Path(args.enriched).read_text())
    criteria = json.loads(Path(args.criteria).read_text())
    criteria["_source"] = args.criteria
    if args.raw:
        enriched["_raw"] = json.loads(Path(args.raw).read_text())

    result = score(enriched, criteria)
    Path(args.output).write_text(json.dumps(result, indent=2, default=str))
    print(f"Wrote {args.output}: {result['decision']} ({result['score_pct']}%, "
          f"{result['fail_count']} fails, profile={result['criteria_profile']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
