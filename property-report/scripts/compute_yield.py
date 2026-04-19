#!/usr/bin/env python3
"""Compute gross and net yield from comp price + normalised rental data.

Assumptions (net yield):
  - 30% cost allowance (voids + management + maintenance + insurance)
  - Uses the professional-let median rent when available, otherwise flags
    the figure as student-influenced.

Cross-checks against the property_yield MCP tool's own output. If the
two diverge by more than 15% relative, both are reported with a note.

Run standalone:
    python compute_yield.py --input raw.json --rental rental.json --output yield.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


NET_COST_ALLOWANCE = 0.30  # 30% for voids, mgmt, maintenance, insurance


def extract_median_price(raw: dict[str, Any]) -> float | None:
    comps = raw.get("property_comps") or {}
    stats = comps.get("stats") or {}
    return (
        stats.get("median_price")
        or comps.get("median_price")
        or comps.get("median")
    )


def extract_tool_yield(raw: dict[str, Any]) -> dict[str, Any]:
    """Pull the property_yield MCP tool's own output, if present."""
    y = raw.get("property_yield") or {}
    return {
        "gross_yield_pct": y.get("gross_yield_pct") or y.get("gross_yield"),
        "net_yield_pct": y.get("net_yield_pct") or y.get("net_yield"),
        "assumption": y.get("assumption") or y.get("notes"),
    }


def compute(raw: dict[str, Any], rental: dict[str, Any]) -> dict[str, Any]:
    median_price = extract_median_price(raw)
    pro = rental.get("pro") or {}
    pro_median_monthly = pro.get("median")

    notes: list[str] = []
    own = {"gross_yield_pct": None, "net_yield_pct": None}

    if median_price and pro_median_monthly:
        annual = pro_median_monthly * 12
        gross = (annual / median_price) * 100
        net = gross * (1 - NET_COST_ALLOWANCE)
        own = {
            "gross_yield_pct": round(gross, 1),
            "net_yield_pct": round(net, 1),
            "inputs": {
                "median_price": median_price,
                "professional_monthly_rent": pro_median_monthly,
                "annual_rent": annual,
                "cost_allowance_pct": int(NET_COST_ALLOWANCE * 100),
            },
        }
    elif median_price and rental.get("student", {}).get("median"):
        notes.append(
            "Only student-let rents available. Yield from student data can vary wildly "
            "by occupancy and is not directly comparable to professional BTL. Skipping "
            "own-yield calc; rely on property_yield tool output with caveat."
        )
    else:
        notes.append("Insufficient data to compute yield (missing price or rent).")

    tool = extract_tool_yield(raw)

    divergence = None
    if own.get("gross_yield_pct") and tool.get("gross_yield_pct"):
        diff = abs(own["gross_yield_pct"] - tool["gross_yield_pct"])
        if own["gross_yield_pct"]:
            divergence = round(diff / own["gross_yield_pct"] * 100, 1)
        if divergence and divergence > 15:
            notes.append(
                f"Own gross yield ({own['gross_yield_pct']}%) diverges "
                f"{divergence}% from property_yield tool ({tool['gross_yield_pct']}%). "
                "Common causes: different rent source, student-let contamination, "
                "filter mismatch. Both figures reported."
            )

    return {
        "own_calc": own,
        "tool_output": tool,
        "divergence_pct": divergence,
        "notes": notes,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Path to raw tool-response JSON.")
    p.add_argument("--rental", required=True, help="Path to normalised rental JSON.")
    p.add_argument("--output", required=True, help="Path to write yield JSON.")
    args = p.parse_args()

    raw = json.loads(Path(args.input).read_text())
    rental = json.loads(Path(args.rental).read_text())
    result = compute(raw, rental)
    Path(args.output).write_text(json.dumps(result, indent=2))
    own = result["own_calc"].get("gross_yield_pct")
    tool = result["tool_output"].get("gross_yield_pct")
    print(f"Wrote {args.output}: own gross={own}% tool gross={tool}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
