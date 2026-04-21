#!/usr/bin/env python3
"""
Apply underwriting criteria to raw deal-screener MCP data and produce a verdict.

Reads raw MCP data from a JSON file and criteria from underwriting-criteria.json,
then outputs a structured verdict JSON with BUY / WATCH / PASS decision and reasons.

Exit codes:
  0 = verdict produced (check decision field)
  1 = input error (missing required data)
  2 = criteria file not found

Usage:
  python3 compute_verdict.py --input /tmp/deal-raw.json --output /tmp/deal-verdict.json
  python3 compute_verdict.py --input /tmp/deal-raw.json  # prints to stdout
"""

import argparse
import json
import sys
from pathlib import Path


DEFAULT_CRITERIA = {
    "min_gross_yield_pct": 5.0,
    "max_price_premium_pct": 10.0,
    "max_annual_service_charge": 5000,
    "min_lease_remaining_years": 90,
    "min_comp_count": 3,
    "min_rental_listing_count": 5,
}


def load_criteria(criteria_path: Path | None) -> dict:
    if criteria_path and criteria_path.exists():
        data = json.loads(criteria_path.read_text())
        merged = {**DEFAULT_CRITERIA}
        for k, v in data.items():
            if not k.startswith("_"):
                merged[k] = v
        return merged
    return DEFAULT_CRITERIA


def check_signal(label: str, value, threshold, direction: str, flags: list, reasons: list, unit: str = "%", fmt: str = ".1f"):
    """Evaluate one underwriting signal. direction: 'min' or 'max'."""
    if value is None:
        flags.append({"signal": label, "value": None, "result": "MISSING", "threshold": threshold})
        reasons.append(f"{label}: no data — treat as WATCH")
        return False, True  # (passed, is_flag)

    if direction == "min":
        passed = value >= threshold
    else:
        passed = value <= threshold

    result = "PASS" if passed else "FAIL"
    flags.append({"signal": label, "value": value, "threshold": threshold, "result": result})
    if not passed:
        if direction == "min":
            reasons.append(f"{label} {value:{fmt}}{unit} below minimum {threshold}{unit}")
        else:
            reasons.append(f"{label} {value:,.0f} exceeds maximum {threshold:,.0f}")
    return passed, False


def within_margin(value, threshold, direction: str, margin_pct: float = 10.0) -> bool:
    """Return True if value is within margin% of the threshold."""
    if value is None:
        return False
    gap = abs(value - threshold) / threshold
    if direction == "min":
        return not (value >= threshold) and gap <= margin_pct / 100
    else:
        return not (value <= threshold) and gap <= margin_pct / 100


def compute(raw: dict, criteria: dict) -> dict:
    signals = []
    fail_reasons = []
    watch_reasons = []

    # --- Gross yield ---
    gross_yield = (
        raw.get("property_yield", {}).get("gross_yield_pct")
        or raw.get("rental_analysis", {}).get("gross_yield_pct")
    )
    yield_passed, yield_missing = check_signal(
        "Gross yield", gross_yield,
        criteria["min_gross_yield_pct"], "min",
        signals, fail_reasons
    )

    # --- Price premium vs comp median ---
    asking_price = raw.get("user_inputs", {}).get("asking_price")
    comp_median = raw.get("property_comps", {}).get("median")
    if asking_price and comp_median:
        premium_pct = (asking_price - comp_median) / comp_median * 100
    else:
        premium_pct = None

    premium_passed, premium_missing = check_signal(
        "Price premium vs median", premium_pct,
        criteria["max_price_premium_pct"], "max",
        signals, fail_reasons
    )

    # --- Service charge (leasehold only) ---
    service_charge = raw.get("rightmove_listing", {}).get("annual_service_charge")
    is_leasehold = raw.get("rightmove_listing", {}).get("tenure", "").lower() == "leasehold"
    sc_passed = True
    if is_leasehold and service_charge is not None:
        sc_passed, _ = check_signal(
            "Annual service charge", service_charge,
            criteria["max_annual_service_charge"], "max",
            signals, fail_reasons
        )
    elif is_leasehold:
        signals.append({"signal": "Annual service charge", "value": None, "result": "MISSING"})
        watch_reasons.append("Service charge not available — verify before proceeding")

    # --- Lease remaining (leasehold only) ---
    lease_years = raw.get("rightmove_listing", {}).get("lease_remaining_years")
    lease_passed = True
    if is_leasehold and lease_years is not None:
        lease_passed, _ = check_signal(
            "Lease remaining", lease_years,
            criteria["min_lease_remaining_years"], "min",
            signals, fail_reasons,
            unit=" years",
            fmt=".0f",
        )
    elif is_leasehold:
        signals.append({"signal": "Lease remaining", "value": None, "result": "MISSING"})
        watch_reasons.append("Lease length not available — verify before proceeding")

    # --- Comp count (flag, not hard fail) ---
    comp_count = raw.get("property_comps", {}).get("count", 0)
    min_comps = criteria["min_comp_count"]
    if comp_count < min_comps:
        watch_reasons.append(f"Thin comp sample ({comp_count} transactions) — median unreliable")
        signals.append({"signal": "Comp count", "value": comp_count,
                        "threshold": min_comps, "result": "THIN"})
    else:
        signals.append({"signal": "Comp count", "value": comp_count,
                        "threshold": min_comps, "result": "PASS"})

    # --- Rental listing count (flag, not hard fail) ---
    rental_count = raw.get("rightmove_search_rent", {}).get("count", 0)
    min_rentals = criteria["min_rental_listing_count"]
    if rental_count < min_rentals:
        watch_reasons.append(f"Thin rental market ({rental_count} listings) — yield confidence low")
        signals.append({"signal": "Rental listing count", "value": rental_count,
                        "threshold": min_rentals, "result": "THIN"})
    else:
        signals.append({"signal": "Rental listing count", "value": rental_count,
                        "threshold": min_rentals, "result": "PASS"})

    # --- EPC flag ---
    epc_rating = raw.get("property_epc", {}).get("rating", "")
    if epc_rating in ("F", "G"):
        watch_reasons.append(f"EPC {epc_rating} — below minimum rental standard, must improve before letting")

    # --- Decision logic ---
    hard_fails = [s for s in signals if s["result"] == "FAIL"]
    marginal = []
    if not yield_passed and gross_yield is not None:
        if within_margin(gross_yield, criteria["min_gross_yield_pct"], "min"):
            marginal.append("Gross yield marginally below threshold")
    if not premium_passed and premium_pct is not None:
        if within_margin(premium_pct, criteria["max_price_premium_pct"], "max"):
            marginal.append("Price premium marginally above threshold")

    fail_count = len(hard_fails)
    if fail_count == 0 and not watch_reasons and not marginal:
        decision = "BUY"
        score_pct = 100
    elif fail_count == 0 and (watch_reasons or marginal):
        decision = "WATCH"
        score_pct = 65
    elif fail_count == 1:
        decision = "WATCH"
        score_pct = 45
    else:
        decision = "PASS"
        score_pct = max(0, 100 - fail_count * 30)

    all_reasons = fail_reasons + watch_reasons + marginal

    return {
        "decision": decision,
        "score_pct": score_pct,
        "fail_count": fail_count,
        "reasons": all_reasons,
        "signals": signals,
        "inputs": {
            "asking_price": asking_price,
            "comp_median": comp_median,
            "gross_yield_pct": gross_yield,
            "price_premium_pct": round(premium_pct, 1) if premium_pct is not None else None,
            "comp_count": comp_count,
            "rental_count": rental_count,
            "epc_rating": epc_rating or None,
            "is_leasehold": is_leasehold,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to raw MCP data JSON")
    parser.add_argument("--output", help="Output path for verdict JSON (default: stdout)")
    parser.add_argument("--criteria", help="Path to underwriting-criteria.json (optional)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 1

    try:
        raw = json.loads(input_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in input: {e}", file=sys.stderr)
        return 1

    criteria_path = Path(args.criteria) if args.criteria else None
    if criteria_path and not criteria_path.exists():
        print(f"ERROR: criteria file not found: {args.criteria}", file=sys.stderr)
        return 2

    criteria = load_criteria(criteria_path)
    verdict = compute(raw, criteria)
    output = json.dumps(verdict, indent=2)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Verdict written to {args.output}: {verdict['decision']} ({verdict['score_pct']}%)")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
