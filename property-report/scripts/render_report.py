#!/usr/bin/env python3
"""Render the property report from a markdown template.

Consumes: raw MCP data, normalised rental, yield computation, verdict.
Produces: a filled markdown report at --output.

The template uses {{dotted.path}} placeholders. Missing values render
as "—" (en dash) rather than crashing, so partial data still produces
a coherent document with the gaps flagged.

Run standalone:
    python render_report.py --raw raw.json --rental rental.json \
        --yield yield.json --verdict verdict.json \
        --template ../assets/report-template.md --output report.md
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
    if isinstance(val, float):
        return f"{val:,.1f}" if val % 1 else f"{int(val):,}"
    if isinstance(val, int):
        return f"{val:,}"
    if isinstance(val, list):
        return ", ".join(str(v) for v in val) if val else "—"
    return str(val)


def money(val: Any) -> str:
    if val is None:
        return "—"
    try:
        return f"£{int(round(float(val))):,}"
    except (TypeError, ValueError):
        return "—"


def build_context(raw: dict, rental: dict, yield_data: dict, verdict: dict) -> dict:
    comps = raw.get("property_comps") or {}
    stats = comps.get("stats") or {}
    epc = raw.get("property_epc") or {}
    sdlt = raw.get("stamp_duty") or {}
    user = raw.get("user_inputs") or {}

    median = stats.get("median_price") or comps.get("median_price")

    ctx = {
        "meta": {
            "address": user.get("address") or "—",
            "postcode": user.get("postcode") or "—",
            "date": date.today().isoformat(),
            "asking_price_fmt": money(user.get("asking_price")),
        },
        "comps": {
            "count": stats.get("transaction_count") or comps.get("count") or "—",
            "median_fmt": money(median),
            "mean_fmt": money(stats.get("mean_price")),
            "min_fmt": money(stats.get("min_price")),
            "max_fmt": money(stats.get("max_price")),
            "median_price_per_sqft_fmt": money(stats.get("median_price_per_sqft")),
            "epc_match_rate_pct": (
                round((stats.get("epc_match_rate") or 0) * 100)
                if stats.get("epc_match_rate") is not None else "—"
            ),
        },
        "epc": {
            "current_rating": epc.get("current_rating") or epc.get("rating") or "—",
            "potential_rating": epc.get("potential_rating") or "—",
            "floor_area_sqm": epc.get("floor_area_sqm") or epc.get("total_floor_area") or "—",
            "annual_energy_cost_fmt": money(
                epc.get("annual_energy_cost") or epc.get("total_energy_cost")
            ),
            "construction_age": epc.get("construction_age_band") or "—",
        },
        "rental": {
            "pro_count": (rental.get("pro") or {}).get("count") or 0,
            "pro_median_fmt": money((rental.get("pro") or {}).get("median")),
            "pro_min_fmt": money((rental.get("pro") or {}).get("min")),
            "pro_max_fmt": money((rental.get("pro") or {}).get("max")),
            "student_count": (rental.get("student") or {}).get("count") or 0,
            "student_median_fmt": money((rental.get("student") or {}).get("median")),
            "mixed": "yes" if rental.get("mixed") else "no",
            "notes": rental.get("normalisation_notes") or [],
        },
        "yield": {
            "gross_own_pct": (yield_data.get("own_calc") or {}).get("gross_yield_pct") or "—",
            "net_own_pct": (yield_data.get("own_calc") or {}).get("net_yield_pct") or "—",
            "gross_tool_pct": (yield_data.get("tool_output") or {}).get("gross_yield_pct") or "—",
            "divergence_pct": yield_data.get("divergence_pct") or "—",
            "notes": yield_data.get("notes") or [],
        },
        "sdlt": {
            "primary_fmt": money(sdlt.get("primary_residence") or sdlt.get("sdlt_primary")),
            "additional_fmt": money(sdlt.get("additional_property") or sdlt.get("sdlt_additional")),
        },
        "verdict": {
            "decision": verdict.get("decision") or "—",
            "score_pct": verdict.get("score_pct") or "—",
            "reasons_md": "\n".join(
                f"- **{r['check']}** — {r['status']}: {r['detail']}"
                for r in (verdict.get("reasons") or [])
            ),
        },
    }
    return ctx


def render(template: str, ctx: dict) -> str:
    def sub(match: re.Match) -> str:
        path = match.group(1)
        val = resolve(ctx, path)
        return format_value(val)
    return PLACEHOLDER_RE.sub(sub, template)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raw", required=True)
    p.add_argument("--rental", required=True)
    p.add_argument("--yield", dest="yield_path", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--template", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    raw = json.loads(Path(args.raw).read_text())
    rental = json.loads(Path(args.rental).read_text())
    yield_data = json.loads(Path(args.yield_path).read_text())
    verdict = json.loads(Path(args.verdict).read_text())
    template = Path(args.template).read_text()

    ctx = build_context(raw, rental, yield_data, verdict)
    rendered = render(template, ctx)
    Path(args.output).write_text(rendered)
    print(f"Wrote {args.output} ({len(rendered)} chars).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
