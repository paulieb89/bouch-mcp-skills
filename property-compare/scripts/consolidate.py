"""
consolidate.py — merge raw MCP tool outputs for up to 3 properties into a single JSON.

Usage:
    python3 consolidate.py --props '{"p1": {...}, "p2": {...}}' --out /tmp/prop-compare-raw.json

Each prop dict may contain any subset of these keys:
    rightmove_listing, property_comps, property_epc, rental_analysis,
    rightmove_search_sale, rightmove_search_rent, property_yield, stamp_duty_primary,
    stamp_duty_additional, meta

The script validates required keys are present, fills missing optional keys with None,
and writes a normalised JSON to --out.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from typing import Any

EXPECTED_KEYS = [
    "rightmove_listing",
    "property_comps",
    "property_epc",
    "rental_analysis",
    "rightmove_search_sale",
    "rightmove_search_rent",
    "property_yield",
    "stamp_duty_primary",
    "stamp_duty_additional",
    "meta",
]

REQUIRED_KEYS = ["property_comps"]


def normalise_prop(label: str, raw: dict[str, Any]) -> dict[str, Any]:
    missing_required = [k for k in REQUIRED_KEYS if not raw.get(k)]
    if missing_required:
        print(f"[WARN] {label}: missing required keys: {missing_required}", file=sys.stderr)

    result: dict[str, Any] = {"label": label}
    for key in EXPECTED_KEYS:
        result[key] = raw.get(key)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Consolidate property comparison data")
    parser.add_argument("--props", required=True, help="JSON string of {p1: {...}, p2: {...}, p3: {...}}")
    parser.add_argument("--out", required=True, help="Output JSON file path")
    args = parser.parse_args()

    try:
        props_raw: dict[str, dict] = json.loads(args.props)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse --props JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not (1 <= len(props_raw) <= 3):
        print(f"[ERROR] Expected 1–3 properties, got {len(props_raw)}", file=sys.stderr)
        sys.exit(1)

    output = {
        "generated": str(date.today()),
        "property_count": len(props_raw),
        "properties": {
            label: normalise_prop(label, data)
            for label, data in props_raw.items()
        },
    }

    with open(args.out, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[OK] Consolidated {len(props_raw)} properties → {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
