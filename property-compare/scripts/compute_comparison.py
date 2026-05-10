"""
compute_comparison.py — derive relative metrics and ranking from consolidated raw data.

Usage:
    python3 compute_comparison.py \
        --raw /tmp/prop-compare-raw.json \
        --criteria path/to/underwriting-defaults.json \
        --out /tmp/prop-compare-metrics.json

Outputs per-property metrics plus a ranked list of property labels.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

EPC_ORDER = {"A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1}

MEES_STATUS = {
    "A": "Compliant ✓",
    "B": "Compliant ✓",
    "C": "Compliant ✓",
    "D": "Compliant ✓",
    "E": "Compliant ✓",
    "F": "Cannot let (MEES) ✗",
    "G": "Cannot let (MEES) ✗",
}


def safe(d: dict | None, *keys: str, default: Any = None) -> Any:
    if d is None:
        return default
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)  # type: ignore[assignment]
        if d is None:
            return default
    return d


def compute_yield(monthly_rent: float | None, price: float | None) -> float | None:
    if monthly_rent and price and price > 0:
        return round((monthly_rent * 12 / price) * 100, 1)
    return None


def score_signal(value: Any, threshold: Any, mode: str = "gte") -> int:
    """Return 1 if signal passes, 0 if fails, -1 if N/A (no data)."""
    if value is None:
        return -1
    if mode == "gte":
        return 1 if value >= threshold else 0
    if mode == "lte":
        return 1 if value <= threshold else 0
    if mode == "epc":
        min_rank = EPC_ORDER.get(str(threshold), 3)
        actual_rank = EPC_ORDER.get(str(value), 0)
        return 1 if actual_rank >= min_rank else 0
    return -1


def score_signal_soft(value: Any, threshold: Any, mode: str = "gte") -> float:
    """Data-quality signals count as 0.5 each (soft flags)."""
    result = score_signal(value, threshold, mode)
    if result == -1:
        return 0.0
    return 0.5 if result == 1 else 0.0


def compute_prop_metrics(label: str, data: dict, asking_price: float | None, criteria: dict) -> dict:
    comps = data.get("property_comps") or {}
    epc = data.get("property_epc") or {}
    rental = data.get("rental_analysis") or {}
    yield_data = data.get("property_yield") or {}
    sdlt_primary = data.get("stamp_duty_primary") or {}
    sdlt_addl = data.get("stamp_duty_additional") or {}
    listing = data.get("rightmove_listing") or {}

    comp_median = safe(comps, "median")
    comp_count = safe(comps, "count")
    area_psf = safe(comps, "median_price_per_sqft")

    # Use asking price from listing if available, else fall back to passed-in price
    price = asking_price or safe(listing, "price") or comp_median

    # Price premium/discount vs comp median
    price_vs_median_pct: float | None = None
    if price and comp_median:
        price_vs_median_pct = round(((price - comp_median) / comp_median) * 100, 1)

    # Asking price per sqft
    sqft = safe(listing, "floor_area_sqft") or safe(epc, "floor_area") and (safe(epc, "floor_area", default=0) * 10.764)
    asking_psf: float | None = None
    if price and sqft and sqft > 0:
        asking_psf = round(price / sqft, 0)

    # Rental
    median_rent = safe(rental, "median_rent_monthly")
    rental_count = safe(rental, "rental_listings_count")

    # Yield
    gross_yield = compute_yield(median_rent, price)
    net_yield = round(gross_yield * (1 - criteria.get("net_yield_cost_allowance_pct", 30) / 100), 1) if gross_yield else None
    tool_yield = safe(yield_data, "gross_yield_pct")

    # EPC
    epc_rating = safe(epc, "rating")
    epc_score_val = safe(epc, "score")
    epc_potential = safe(epc, "potential_rating")
    epc_sqm = safe(epc, "floor_area")
    epc_sqft = round(epc_sqm * 10.764) if epc_sqm else None
    mees = MEES_STATUS.get(str(epc_rating), "No EPC data") if epc_rating else "No EPC data"

    # EPC/listing floor area mismatch flag
    epc_mismatch = False
    listing_sqft_raw = safe(listing, "floor_area_sqft")
    if listing_sqft_raw and epc_sqft:
        diff_pct = abs(listing_sqft_raw - epc_sqft) / listing_sqft_raw * 100
        epc_mismatch = diff_pct > 10

    # SDLT
    sdlt_primary_amt = safe(sdlt_primary, "total_sdlt")
    sdlt_primary_rate = safe(sdlt_primary, "effective_rate")
    sdlt_addl_amt = safe(sdlt_addl, "total_sdlt")
    sdlt_addl_rate = safe(sdlt_addl, "effective_rate")
    total_cost_addl = (price or 0) + (sdlt_addl_amt or 0) + 2000 if price else None

    # Lease
    lease_years = safe(listing, "years_remaining_on_lease")

    # Signal scoring
    s_yield = score_signal(gross_yield, criteria.get("min_gross_yield_pct", 5.0), "gte")
    s_price = score_signal(price_vs_median_pct, criteria.get("max_price_premium_pct", 10.0), "lte")
    s_epc = score_signal(epc_rating, criteria.get("min_epc_rating", "E"), "epc")
    s_comps = score_signal_soft(comp_count, criteria.get("min_comp_count", 3), "gte")
    s_rental = score_signal_soft(rental_count, criteria.get("min_rental_listing_count", 5), "gte")
    s_lease = score_signal(lease_years, criteria.get("min_lease_remaining_years", 90), "gte") if lease_years is not None else -1

    hard_signals = [s_yield, s_price, s_epc]
    soft_signals = [s_comps, s_rental]
    hard_score = sum(s for s in hard_signals if s >= 0)
    soft_score = sum(soft_signals)
    lease_score = max(s_lease, 0) if s_lease >= 0 else 0
    total_score = round(hard_score + soft_score + lease_score)

    def fmt_signal(s: int | float, mode: str = "hard") -> str:
        if s == -1:
            return "N/A"
        if mode == "soft":
            return "✓" if s > 0 else "⚑"
        return "✓" if s == 1 else "✗"

    return {
        "label": label,
        "price": price,
        "price_fmt": f"£{price:,.0f}" if price else "Unknown",
        "comp_median": comp_median,
        "comp_median_fmt": f"£{comp_median:,.0f}" if comp_median else "N/A",
        "price_vs_median_pct": price_vs_median_pct,
        "price_vs_median_fmt": (f"+{price_vs_median_pct:.1f}%" if price_vs_median_pct and price_vs_median_pct > 0 else f"{price_vs_median_pct:.1f}%") if price_vs_median_pct is not None else "N/A",
        "asking_psf": asking_psf,
        "asking_psf_fmt": f"£{asking_psf:.0f}" if asking_psf else "N/A",
        "area_psf": area_psf,
        "area_psf_fmt": f"£{area_psf}" if area_psf else "N/A",
        "comp_count": comp_count,
        "median_rent": median_rent,
        "median_rent_fmt": f"£{median_rent:,.0f}/month" if median_rent else "No data",
        "rent_range_fmt": f"£{safe(rental, 'rent_range_low'):,.0f}–£{safe(rental, 'rent_range_high'):,.0f}" if safe(rental, "rent_range_low") else "N/A",
        "rental_count": rental_count,
        "rental_conf": ("Good" if (rental_count or 0) >= 5 else "Low — thin market ⚑"),
        "gross_yield": gross_yield,
        "gross_yield_fmt": f"{gross_yield:.1f}%" if gross_yield is not None else "N/A",
        "net_yield": net_yield,
        "net_yield_fmt": f"{net_yield:.1f}%" if net_yield is not None else "N/A",
        "tool_yield": tool_yield,
        "tool_yield_fmt": f"{tool_yield:.1f}%" if tool_yield is not None else "N/A",
        "yield_pass_fmt": "✓ passes" if s_yield == 1 else ("✗ fails" if s_yield == 0 else "N/A"),
        "epc_rating": epc_rating,
        "epc_score": epc_score_val,
        "epc_potential": epc_potential,
        "epc_sqft": epc_sqft,
        "epc_sqft_fmt": f"{epc_sqft:,}" if epc_sqft else "N/A",
        "epc_age": safe(epc, "construction_age"),
        "heating": safe(epc, "main_heating") or "N/A",
        "energy_cost_fmt": f"£{(safe(epc, 'heating_cost_current', default=0) or 0) + (safe(epc, 'hot_water_cost_current', default=0) or 0) + (safe(epc, 'lighting_cost_current', default=0) or 0):,.0f}/yr" if epc_rating else "N/A",
        "mees": mees,
        "epc_mismatch": epc_mismatch,
        "sdlt_primary_fmt": f"£{sdlt_primary_amt:,.0f}" if sdlt_primary_amt is not None else "N/A",
        "sdlt_primary_rate_fmt": f"{sdlt_primary_rate:.2f}" if sdlt_primary_rate is not None else "N/A",
        "sdlt_addl_fmt": f"£{sdlt_addl_amt:,.0f}" if sdlt_addl_amt is not None else "N/A",
        "sdlt_addl_rate_fmt": f"{sdlt_addl_rate:.2f}" if sdlt_addl_rate is not None else "N/A",
        "total_cost_addl_fmt": f"£{total_cost_addl:,.0f}" if total_cost_addl else "N/A",
        "signal_yield": fmt_signal(s_yield),
        "signal_price": fmt_signal(s_price),
        "signal_epc": fmt_signal(s_epc),
        "signal_comps": fmt_signal(s_comps, "soft"),
        "signal_rental": fmt_signal(s_rental, "soft"),
        "signal_lease": fmt_signal(s_lease),
        "score": total_score,
        "score_fmt": f"{total_score}/6",
        # raw values for tie-breaking
        "_gross_yield_raw": gross_yield or 0,
        "_price_vs_median_raw": price_vs_median_pct or 999,
        "_epc_score_raw": epc_score_val or 0,
        "_comp_count_raw": comp_count or 0,
    }


def rank_properties(metrics: list[dict], criteria: dict) -> list[dict]:
    tiebreak = criteria.get("ranking_tiebreak_priority", ["gross_yield_pct", "price_vs_median_pct", "epc_score", "comp_count"])
    key_map = {
        "gross_yield_pct": ("_gross_yield_raw", False),
        "price_vs_median_pct": ("_price_vs_median_raw", True),
        "epc_score": ("_epc_score_raw", False),
        "comp_count": ("_comp_count_raw", False),
    }

    def sort_key(m: dict) -> tuple:
        primary = -m["score"]
        tiebreaks = []
        for tb in tiebreak:
            field, lower_is_better = key_map.get(tb, (None, False))
            if field:
                val = m.get(field, 0)
                tiebreaks.append(val if lower_is_better else -val)
        return (primary, *tiebreaks)

    ranked = sorted(metrics, key=sort_key)
    medals = ["🥇", "🥈", "🥉"]
    for i, m in enumerate(ranked):
        m["rank"] = i + 1
        m["rank_medal"] = medals[i] if i < 3 else f"#{i+1}"
    return ranked


def generate_rank_reasons(ranked: list[dict]) -> list[str]:
    reasons = []
    for m in ranked:
        parts = []
        if m["gross_yield"] is not None:
            parts.append(f"{m['gross_yield_fmt']} gross yield")
        if m["price_vs_median_pct"] is not None:
            parts.append(f"asking price {m['price_vs_median_fmt']} vs comp median")
        if m["epc_rating"]:
            parts.append(f"EPC {m['epc_rating']}")
        reasons.append("; ".join(parts) if parts else "insufficient data for full comparison")
    return reasons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, help="Path to consolidated raw JSON")
    parser.add_argument("--criteria", required=True, help="Path to underwriting-defaults.json")
    parser.add_argument("--out", required=True, help="Output metrics JSON path")
    args = parser.parse_args()

    with open(args.raw) as f:
        raw = json.load(f)

    with open(args.criteria) as f:
        criteria = json.load(f)

    props = raw.get("properties", {})
    if not props:
        print("[ERROR] No properties in raw JSON", file=sys.stderr)
        sys.exit(1)

    metrics_list = []
    for label, data in props.items():
        # asking_price: prefer rightmove_listing price, else None (compute_prop_metrics handles fallback)
        asking_price = safe(data.get("rightmove_listing"), "price") or safe(data.get("meta"), "asking_price")
        m = compute_prop_metrics(label, data, asking_price, criteria)
        metrics_list.append(m)

    ranked = rank_properties(metrics_list, criteria)
    rank_reasons = generate_rank_reasons(ranked)
    for m, reason in zip(ranked, rank_reasons):
        m["rank_reason"] = reason

    output = {
        "generated": raw.get("generated"),
        "property_count": raw.get("property_count"),
        "ranked": ranked,
        "by_label": {m["label"]: m for m in ranked},
    }

    with open(args.out, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[OK] Computed metrics for {len(ranked)} properties → {args.out}", file=sys.stderr)
    for m in ranked:
        print(f"  {m['rank_medal']} {m['label']}: score {m['score_fmt']}, yield {m['gross_yield_fmt']}", file=sys.stderr)


if __name__ == "__main__":
    main()
