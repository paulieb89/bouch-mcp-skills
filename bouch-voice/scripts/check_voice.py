#!/usr/bin/env python3
"""
Validate copy against BOUCH voice rules.

Checks for banned marketing language, em dashes, exclamation marks,
superlative ownership claims, and American spellings. Works on any
UK business copy: website pages, emails, proposals, case studies.

Exit codes:
  0 = PASS or PASS WITH WARNINGS (safe to use; review warnings before publish)
  1 = FAIL (banned word, em dash, or ownership claim found — rewrite first)
  2 = script error (empty input, bad file)

Usage:
  python3 check_voice.py path/to/copy.md
  cat page.md | python3 check_voice.py
  python3 check_voice.py --count-only path/to/copy.md
"""

import argparse
import re
import sys
from pathlib import Path


BANNED_WORDS = [
    # AI vendor language
    "ai-powered", "ai powered",
    "leverage", "leverages", "leveraged", "leveraging",
    "revolutionise", "revolutionize", "revolutionary",
    "cutting-edge", "cutting edge",
    "disruptive", "disruption",
    "game-changing", "game changing", "game-changer",
    "paradigm", "paradigm shift",
    "seamless", "seamlessly",
    "next-generation", "next gen",
    "ecosystem",
    # Management consultant language
    "transform your", "transformation",
    "digital transformation",
    "unlock potential", "unlock the potential",
    "future-proof", "future proof",
    "scale with ai", "scale your business with",
    "automate everything",
    "10x", "10 x",
    "supercharge", "supercharged",
    "empower", "empowers", "empowering", "empowerment",
    "synergy", "synergies", "synergistic",
    "best-in-class", "world-class",
    "industry-leading", "market-leading",
    # BOUCH-specific bans
    "deep dive", "deep-dive",
    "innovative solution", "innovative solutions",
    "seamless integration",
]

SUPERLATIVE_CLAIMS = [
    (r"\bthe only\b", "the only"),
    (r"\bthe first\b", "the first"),
    (r"\bworld'?s leading\b", "world's leading"),
    (r"\buk'?s leading\b", "UK's leading"),
    (r"\bnumber one\b", "number one"),
    (r"\b#1\b", "#1"),
    (r"\bunrivalled\b", "unrivalled"),
    (r"\bunparalleled\b", "unparalleled"),
    (r"\bunmatched\b", "unmatched"),
]

AMERICAN_SPELLINGS = {
    "color": "colour",
    "colors": "colours",
    "organize": "organise",
    "organized": "organised",
    "organizing": "organising",
    "organization": "organisation",
    "organizations": "organisations",
    "recognize": "recognise",
    "recognized": "recognised",
    "recognizing": "recognising",
    "analyze": "analyse",
    "analyzed": "analysed",
    "analyzing": "analysing",
    "optimize": "optimise",
    "optimized": "optimised",
    "optimizing": "optimising",
    "specialize": "specialise",
    "specialized": "specialised",
    "prioritize": "prioritise",
    "prioritized": "prioritised",
    "customize": "customise",
    "customized": "customised",
    "favorite": "favourite",
    "behavior": "behaviour",
    "behaviors": "behaviours",
    "flavor": "flavour",
    "neighbor": "neighbour",
    "defense": "defence",
    "offense": "offence",
    "license": "licence",
    "center": "centre",
    "centers": "centres",
    "program": "programme",  # when not referring to software
}


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def find_banned_words(text: str) -> list[tuple[str, int]]:
    text_lower = text.lower()
    hits = []
    for word in BANNED_WORDS:
        if "-" in word or " " in word:
            count = text_lower.count(word)
        else:
            pattern = rf"\b{re.escape(word)}\b"
            count = len(re.findall(pattern, text_lower))
        if count > 0:
            hits.append((word, count))
    return hits


def find_superlatives(text: str) -> list[str]:
    text_lower = text.lower()
    hits = []
    for pattern, label in SUPERLATIVE_CLAIMS:
        if re.search(pattern, text_lower):
            hits.append(label)
    return hits


def find_em_dashes(text: str) -> tuple[int, list[str]]:
    clean = strip_code_blocks(text)
    lines = clean.splitlines()
    hits = []
    total = 0
    for i, line in enumerate(lines, 1):
        count = line.count("—")
        if count:
            total += count
            hits.append(f"  Line {i}: {count}× — \"{line.strip()[:80]}\"")
    return total, hits


def find_exclamation_marks(text: str) -> list[str]:
    clean = strip_code_blocks(text)
    lines = clean.splitlines()
    hits = []
    for i, line in enumerate(lines, 1):
        if "!" in line:
            hits.append(f"  Line {i}: \"{line.strip()[:80]}\"")
    return hits


def find_american_spellings(text: str) -> list[tuple[str, str]]:
    text_lower = text.lower()
    hits = []
    for american, british in AMERICAN_SPELLINGS.items():
        pattern = rf"\b{re.escape(american)}\b"
        if re.search(pattern, text_lower):
            hits.append((american, british))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Path to copy file. Omit to read stdin.")
    parser.add_argument("--count-only", action="store_true",
                        help="Print total violation count only, no detail")
    args = parser.parse_args()

    if args.path:
        try:
            text = Path(args.path).read_text()
        except OSError as e:
            print(f"ERROR: could not read {args.path}: {e}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("ERROR: empty input", file=sys.stderr)
        return 2

    banned_hits = find_banned_words(text)
    superlative_hits = find_superlatives(text)
    em_count, em_lines = find_em_dashes(text)
    exclamation_lines = find_exclamation_marks(text)
    american_hits = find_american_spellings(text)

    hard_fail_count = len(banned_hits) + len(superlative_hits) + (1 if em_count > 0 else 0)
    warn_count = (1 if exclamation_lines else 0) + len(american_hits)
    total_issues = hard_fail_count + warn_count

    if args.count_only:
        print(total_issues)
        return 0 if hard_fail_count == 0 else 1

    print("=" * 60)
    print("BOUCH VOICE CHECK")
    print("=" * 60)

    any_fail = False

    if banned_hits:
        any_fail = True
        print(f"\n[FAIL] BANNED LANGUAGE — {len(banned_hits)} phrase(s) found")
        for word, count in sorted(banned_hits, key=lambda x: -x[1]):
            print(f"  '{word}' × {count}")

    if superlative_hits:
        any_fail = True
        print(f"\n[FAIL] SUPERLATIVE CLAIMS — {len(superlative_hits)} found (never make 'the only'/'the first' claims without attribution)")
        for claim in superlative_hits:
            print(f"  '{claim}'")

    if em_count > 0:
        any_fail = True
        print(f"\n[FAIL] EM DASHES — {em_count} found (use commas, full stops, or restructure)")
        for line in em_lines[:5]:
            print(line)

    if exclamation_lines:
        print(f"\n[WARN] EXCLAMATION MARKS — {len(exclamation_lines)} line(s) (use only when genuinely warranted)")
        for line in exclamation_lines[:5]:
            print(line)

    if american_hits:
        print(f"\n[WARN] AMERICAN SPELLINGS — {len(american_hits)} found (British English required)")
        for american, british in american_hits:
            print(f"  '{american}' → '{british}'")

    print("\n" + "-" * 60)
    if not any_fail and not exclamation_lines and not american_hits:
        print("OVERALL: PASS")
        return 0
    elif not any_fail:
        print("OVERALL: PASS WITH WARNINGS — review before publishing")
        return 0
    else:
        print(f"OVERALL: FAIL — {hard_fail_count} violation(s) — rewrite before publishing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
