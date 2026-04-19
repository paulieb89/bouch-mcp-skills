#!/usr/bin/env python3
"""Normalise UK rental listings from rightmove_search and rental_analysis.

Input: a JSON file with tool responses, expecting at minimum a
`rightmove_search_rent` key containing listings under `listings`.
Optionally `rental_analysis` for aggregate comparison.

Output: {pro: {...}, student: {...}, mixed: bool, sample_size: int,
         normalisation_notes: [...]}.

All rents normalised to monthly (weekly × 52 / 12).

Run standalone:
    python normalise_rents.py --input raw.json --output rental.json
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


STUDENT_SIGNALS = (
    "student",
    "students",
    "per room",
    "pcm per room",
    "pppw",  # per person per week
    "pw",  # weekly pricing — common in student HMOs
)


def weekly_to_monthly(price_pw: float) -> float:
    """UK convention: weekly × 52 / 12, rounded to whole £."""
    return round(price_pw * 52 / 12)


def is_student_listing(listing: dict[str, Any]) -> bool:
    """Heuristic: weekly pricing OR 'student' in title/description."""
    text = " ".join(
        str(listing.get(k, "")) for k in ("title", "description", "summary", "displayPrice")
    ).lower()
    if any(sig in text for sig in STUDENT_SIGNALS):
        return True
    freq = str(listing.get("priceFrequency", "")).lower()
    if freq in ("weekly", "pw"):
        return True
    return False


def extract_monthly_rent(listing: dict[str, Any]) -> float | None:
    """Pull a monthly rent figure from a Rightmove listing, normalising weekly."""
    price = listing.get("price") or listing.get("amount") or listing.get("displayPrice")
    if price is None:
        return None
    freq = str(listing.get("priceFrequency", "monthly")).lower()

    if isinstance(price, str):
        digits = "".join(c for c in price if c.isdigit() or c == ".")
        try:
            price = float(digits)
        except ValueError:
            return None
    price = float(price)

    if freq in ("weekly", "pw"):
        return weekly_to_monthly(price)
    if freq in ("yearly", "annually", "per annum", "pa"):
        return round(price / 12)
    return round(price)


def summarise(rents: list[float]) -> dict[str, Any]:
    if not rents:
        return {"count": 0, "median": None, "mean": None, "min": None, "max": None}
    return {
        "count": len(rents),
        "median": round(statistics.median(rents)),
        "mean": round(statistics.mean(rents)),
        "min": round(min(rents)),
        "max": round(max(rents)),
    }


def normalise(raw: dict[str, Any]) -> dict[str, Any]:
    rightmove = (
        raw.get("rightmove_search_rent")
        or raw.get("rightmove_search")
        or {}
    )
    listings = rightmove.get("listings") or rightmove.get("results") or []

    pro_rents: list[float] = []
    student_rents: list[float] = []
    skipped = 0
    notes: list[str] = []

    for listing in listings:
        monthly = extract_monthly_rent(listing)
        if monthly is None:
            skipped += 1
            continue
        if is_student_listing(listing):
            student_rents.append(monthly)
        else:
            pro_rents.append(monthly)

    total = len(pro_rents) + len(student_rents)
    mixed = bool(pro_rents) and bool(student_rents)

    if mixed:
        notes.append(
            f"Mixed market: {len(pro_rents)} professional lets, "
            f"{len(student_rents)} student lets. Professional median is the headline "
            "figure; student lets reported separately."
        )
    if total < 5:
        notes.append(
            f"Thin rental sample ({total} listings). Rental figures may not be representative."
        )
    if skipped:
        notes.append(f"{skipped} listings skipped (no parseable price).")

    rental_analysis = raw.get("rental_analysis") or {}
    aggregate_median = (
        rental_analysis.get("median_rent")
        or rental_analysis.get("median_monthly")
        or rental_analysis.get("median")
    )
    if aggregate_median and pro_rents:
        pro_median = statistics.median(pro_rents)
        if abs(aggregate_median - pro_median) / pro_median > 0.15:
            notes.append(
                f"rental_analysis aggregate median (£{aggregate_median:,}) diverges >15% "
                f"from professional-let median (£{int(pro_median):,}). Likely contaminated "
                "by student lets. Use the professional figure."
            )

    return {
        "pro": summarise(pro_rents),
        "student": summarise(student_rents),
        "mixed": mixed,
        "sample_size": total,
        "skipped_listings": skipped,
        "normalisation_notes": notes,
        "aggregate_comparison": {
            "rental_analysis_median": aggregate_median,
            "professional_only_median": summarise(pro_rents)["median"] if pro_rents else None,
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Path to raw tool-response JSON.")
    p.add_argument("--output", required=True, help="Path to write normalised rental JSON.")
    args = p.parse_args()

    raw = json.loads(Path(args.input).read_text())
    result = normalise(raw)
    Path(args.output).write_text(json.dumps(result, indent=2))
    print(f"Wrote {args.output}: {result['sample_size']} listings, "
          f"{'mixed' if result['mixed'] else 'single-segment'} market.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
