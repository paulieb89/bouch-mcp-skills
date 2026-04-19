#!/usr/bin/env python3
"""Produce a BUY / WATCH / PASS verdict against explicit underwriting criteria.

Reads raw MCP data, normalised rental, and yield output. Scores against
criteria JSON (defaults in assets/underwriting-defaults.json — override
via --criteria for client-specific thresholds).

Output: {decision, score, max_score, reasons: [{check, status, detail}]}

Run standalone:
    python underwrite.py --input raw.json --yield yield.json \
        --criteria ../assets/underwriting-defaults.json --output verdict.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EPC_GRADE_ORDER = {g: i for i, g in enumerate("GFEDCBA", start=1)}


def grade_meets_floor(current: str | None, floor: str) -> bool:
    if not current:
        return False
    return EPC_GRADE_ORDER.get(current.upper(), 0) >= EPC_GRADE_ORDER.get(floor.upper(), 0)


def check_yield(yield_data: dict, criteria: dict) -> dict:
    own = yield_data.get("own_calc") or {}
    gross = own.get("gross_yield_pct")
    min_gross = criteria.get("min_gross_yield_pct", 6.0)

    if gross is None:
        return {"check": "gross_yield", "status": "unknown", "detail": "no yield data",
                "pass": False, "weight": 2}
    if gross >= min_gross:
        return {"check": "gross_yield", "status": "pass",
                "detail": f"{gross}% ≥ {min_gross}%", "pass": True, "weight": 2}
    return {"check": "gross_yield", "status": "fail",
            "detail": f"{gross}% < {min_gross}%", "pass": False, "weight": 2}


def check_epc(raw: dict, criteria: dict) -> dict:
    epc = raw.get("property_epc") or {}
    current = epc.get("current_rating") or epc.get("rating")
    floor = criteria.get("min_epc_grade", "D")

    if not current:
        return {"check": "epc_grade", "status": "unknown",
                "detail": "no EPC on subject property", "pass": False, "weight": 1}
    if grade_meets_floor(current, floor):
        return {"check": "epc_grade", "status": "pass",
                "detail": f"EPC {current} meets {floor} floor", "pass": True, "weight": 1}
    return {"check": "epc_grade", "status": "fail",
            "detail": f"EPC {current} below {floor} floor — MEES exposure",
            "pass": False, "weight": 1}


def check_sample(raw: dict, criteria: dict) -> dict:
    comps = raw.get("property_comps") or {}
    count = (
        (comps.get("stats") or {}).get("transaction_count")
        or comps.get("count")
        or len(comps.get("transactions") or [])
    )
    min_count = criteria.get("min_comp_count", 5)

    if count >= min_count:
        return {"check": "comp_sample", "status": "pass",
                "detail": f"{count} comps (≥{min_count})", "pass": True, "weight": 1}
    return {"check": "comp_sample", "status": "fail",
            "detail": f"only {count} comps — thin market signal",
            "pass": False, "weight": 1}


def check_price_vs_median(raw: dict, criteria: dict) -> dict:
    """If user provided an asking price, check it against median."""
    asking = (raw.get("user_inputs") or {}).get("asking_price")
    if not asking:
        return {"check": "price_vs_median", "status": "skipped",
                "detail": "no asking price supplied", "pass": True, "weight": 0}

    comps = raw.get("property_comps") or {}
    median = (comps.get("stats") or {}).get("median_price") or comps.get("median_price")
    if not median:
        return {"check": "price_vs_median", "status": "unknown",
                "detail": "no median available", "pass": False, "weight": 1}

    premium_pct = (asking - median) / median * 100
    max_premium = criteria.get("max_premium_over_median_pct", 10)

    if premium_pct <= max_premium:
        return {"check": "price_vs_median", "status": "pass",
                "detail": f"asking {premium_pct:+.1f}% vs median (≤{max_premium}%)",
                "pass": True, "weight": 1}
    return {"check": "price_vs_median", "status": "fail",
            "detail": f"asking {premium_pct:+.1f}% above median — outside {max_premium}% tolerance",
            "pass": False, "weight": 1}


CHECKS = [check_yield, check_epc, check_sample, check_price_vs_median]


def underwrite(raw: dict[str, Any], yield_data: dict[str, Any], criteria: dict[str, Any]) -> dict[str, Any]:
    results = [check(raw, criteria) if check is check_sample or check is check_epc or check is check_price_vs_median
               else check(yield_data, criteria) for check in CHECKS]

    total_weight = sum(r["weight"] for r in results)
    earned = sum(r["weight"] for r in results if r.get("pass"))

    fail_count = sum(1 for r in results if r["status"] == "fail")
    score_pct = round(earned / total_weight * 100, 1) if total_weight else 0

    # Decision rules
    if fail_count >= 2 or score_pct < 50:
        decision = "PASS"
    elif fail_count == 1 or score_pct < 75:
        decision = "WATCH"
    else:
        decision = "BUY"

    return {
        "decision": decision,
        "score_pct": score_pct,
        "score_earned": earned,
        "score_max": total_weight,
        "criteria_source": criteria.get("_source", "defaults"),
        "reasons": results,
        "disclaimer": (
            "This is a criteria-based scan, not a recommendation. BUY/WATCH/PASS "
            "reflects the supplied underwriting thresholds only. Always verify "
            "with your own diligence before acting."
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--yield", dest="yield_path", required=True)
    p.add_argument("--criteria", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    raw = json.loads(Path(args.input).read_text())
    yield_data = json.loads(Path(args.yield_path).read_text())
    criteria = json.loads(Path(args.criteria).read_text())
    criteria["_source"] = args.criteria

    result = underwrite(raw, yield_data, criteria)
    Path(args.output).write_text(json.dumps(result, indent=2))
    print(f"Wrote {args.output}: {result['decision']} ({result['score_pct']}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
