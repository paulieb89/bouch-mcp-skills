"""
render_comparison.py — fill compare-template.md with computed metrics.

Usage:
    python3 render_comparison.py \
        --metrics /tmp/prop-compare-metrics.json \
        --template path/to/compare-template.md \
        --out /tmp/prop-compare.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


def load(path: str) -> Any:
    with open(path) as f:
        return json.load(f)


def read(path: str) -> str:
    with open(path) as f:
        return f.read()


def write(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def safe_get(d: dict | None, key: str, default: str = "N/A") -> str:
    if d is None:
        return default
    val = d.get(key)
    return str(val) if val is not None else default


def build_replacements(metrics: dict) -> dict[str, str]:
    ranked: list[dict] = metrics.get("ranked", [])
    by_label: dict[str, dict] = metrics.get("by_label", {})

    # Order properties as p1, p2, p3 by original label
    labels = list(by_label.keys())
    props = {f"p{i+1}": by_label[label] for i, label in enumerate(labels[:3])}

    repl: dict[str, str] = {
        "{{date}}": metrics.get("generated", ""),
        "{{property_count}}": str(metrics.get("property_count", len(labels))),
    }

    for key, m in props.items():
        k = key  # e.g. "p1"
        repl[f"{{{{{k}_address}}}}"] = safe_get(m, "label")
        repl[f"{{{{{k}_postcode}}}}"] = "—"
        repl[f"{{{{{k}_asking}}}}"] = safe_get(m, "price_fmt")
        repl[f"{{{{{k}_type}}}}"] = "—"
        repl[f"{{{{{k}_beds}}}}"] = "—"
        repl[f"{{{{{k}_sqft}}}}"] = safe_get(m, "epc_sqft_fmt")
        repl[f"{{{{{k}_tenure}}}}"] = "—"
        repl[f"{{{{{k}_ctax}}}}"] = "—"
        repl[f"{{{{{k}_epc}}}}"] = safe_get(m, "epc_rating")
        repl[f"{{{{{k}_epc_score}}}}"] = safe_get(m, "epc_score")
        repl[f"{{{{{k}_epc_potential}}}}"] = safe_get(m, "epc_potential")
        repl[f"{{{{{k}_epc_sqft}}}}"] = safe_get(m, "epc_sqft_fmt")
        repl[f"{{{{{k}_epc_age}}}}"] = safe_get(m, "epc_age")
        repl[f"{{{{{k}_heating}}}}"] = safe_get(m, "heating")
        repl[f"{{{{{k}_energy_cost}}}}"] = safe_get(m, "energy_cost_fmt")
        repl[f"{{{{{k}_mees}}}}"] = safe_get(m, "mees")
        repl[f"{{{{{k}_gross_yield}}}}"] = safe_get(m, "gross_yield_fmt").rstrip("%")
        repl[f"{{{{{k}_net_yield}}}}"] = safe_get(m, "net_yield_fmt").rstrip("%")
        repl[f"{{{{{k}_tool_yield}}}}"] = safe_get(m, "tool_yield_fmt").rstrip("%")
        repl[f"{{{{{k}_yield_pass}}}}"] = safe_get(m, "yield_pass_fmt")
        repl[f"{{{{{k}_comp_median}}}}"] = safe_get(m, "comp_median_fmt")
        repl[f"{{{{{k}_vs_median}}}}"] = safe_get(m, "price_vs_median_fmt")
        repl[f"{{{{{k}_asking_psf}}}}"] = safe_get(m, "asking_psf_fmt")
        repl[f"{{{{{k}_area_psf}}}}"] = safe_get(m, "area_psf_fmt")
        repl[f"{{{{{k}_comp_count}}}}"] = str(m.get("comp_count") or "N/A")
        repl[f"{{{{{k}_rent_median}}}}"] = safe_get(m, "median_rent_fmt")
        repl[f"{{{{{k}_rent_range}}}}"] = safe_get(m, "rent_range_fmt")
        repl[f"{{{{{k}_rental_count}}}}"] = str(m.get("rental_count") or "N/A")
        repl[f"{{{{{k}_rental_conf}}}}"] = safe_get(m, "rental_conf")
        repl[f"{{{{{k}_sdlt_primary}}}}"] = safe_get(m, "sdlt_primary_fmt")
        repl[f"{{{{{k}_sdlt_primary_rate}}}}"] = safe_get(m, "sdlt_primary_rate_fmt")
        repl[f"{{{{{k}_sdlt_addl}}}}"] = safe_get(m, "sdlt_addl_fmt")
        repl[f"{{{{{k}_sdlt_addl_rate}}}}"] = safe_get(m, "sdlt_addl_rate_fmt")
        repl[f"{{{{{k}_total_cost}}}}"] = safe_get(m, "total_cost_addl_fmt")
        repl[f"{{{{{k}_s_yield}}}}"] = safe_get(m, "signal_yield")
        repl[f"{{{{{k}_s_price}}}}"] = safe_get(m, "signal_price")
        repl[f"{{{{{k}_s_epc}}}}"] = safe_get(m, "signal_epc")
        repl[f"{{{{{k}_s_comps}}}}"] = safe_get(m, "signal_comps")
        repl[f"{{{{{k}_s_rental}}}}"] = safe_get(m, "signal_rental")
        repl[f"{{{{{k}_s_lease}}}}"] = safe_get(m, "signal_lease")
        repl[f"{{{{{k}_score}}}}"] = safe_get(m, "score_fmt")
        repl[f"{{{{{k}_rank}}}}"] = m.get("rank_medal", "—")

    # Ranking section
    medals = ["🥇 1st", "🥈 2nd", "🥉 3rd"]
    for i, m in enumerate(ranked[:3]):
        idx = i + 1
        repl[f"{{{{rank{idx}_label}}}}"] = m.get("label", "—")
        repl[f"{{{{rank{idx}_reason}}}}"] = m.get("rank_reason", "—")

    # Placeholder sections (populated by LLM from context)
    repl["{{search_level}}"] = "sector"
    repl["{{price_notes}}"] = ""
    repl["{{rental_notes}}"] = ""
    repl["{{yield_notes}}"] = ""
    repl["{{epc_notes}}"] = ""
    repl["{{recommendation_paragraph}}"] = "[Recommendation to be written by the agent from comparison context]"

    return repl


def apply_replacements(template: str, repl: dict[str, str]) -> str:
    for placeholder, value in repl.items():
        template = template.replace(placeholder, value)
    # Clear any remaining unfilled placeholders (e.g. p3 when only 2 properties)
    template = re.sub(r"\{\{[^}]+\}\}", "—", template)
    return template


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    metrics = load(args.metrics)
    template = read(args.template)
    repl = build_replacements(metrics)
    rendered = apply_replacements(template, repl)

    write(args.out, rendered)
    print(f"[OK] Rendered comparison report → {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
