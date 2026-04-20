#!/usr/bin/env python3
"""
Scan text for AI writing patterns and report violations.

Checks for the 10 AI patterns documented in references/ai-patterns.md:
em dash overuse, AI vocabulary, rule of three, promotional inflation,
soulless structure signals, conjunctive phrases, negative parallelism,
vague attribution, filler openings, and fake enthusiasm.

Exit codes:
  0 = CLEAN (no patterns found)
  1 = PATTERNS FOUND (list printed to stdout)
  2 = script error (empty input, bad file)

Usage:
  python3 check_patterns.py path/to/text.md
  cat output.md | python3 check_patterns.py
  python3 check_patterns.py --count-only path/to/text.md
"""

import argparse
import re
import sys
from pathlib import Path


AI_VOCABULARY = [
    "delve", "delves", "delving", "delved",
    "tapestry",
    "bustling",
    "vibrant",
    "realm",
    "paradigm", "paradigms",
    "multifaceted",
    "comprehensive",
    "robust",
    "streamline", "streamlines", "streamlined", "streamlining",
    "foster", "fosters", "fostered", "fostering",
    "leverage", "leverages", "leveraged", "leveraging",
    "harness", "harnesses", "harnessed", "harnessing",
    "utilise", "utilises", "utilised", "utilising",
    "utilize", "utilizes", "utilized", "utilizing",
    "facilitate", "facilitates", "facilitated", "facilitating",
    "spearhead", "spearheads", "spearheaded", "spearheading",
    "underscore", "underscores", "underscored", "underscoring",
    "bolster", "bolsters", "bolstered", "bolstering",
    "elevate", "elevates", "elevated", "elevating",
    "innovative", "innovation",
    "game-changing", "game changing", "game-changer",
    "groundbreaking", "ground-breaking",
    "cutting-edge", "cutting edge",
    "state-of-the-art",
    "synergy", "synergies", "synergistic",
    "holistic",
    "deep dive", "deep-dive",
    "unpack", "unpacks", "unpacking",
    "double down", "doubling down",
    "move the needle",
    "landscape",  # metaphorical use — may have false positives
]

CONJUNCTIVE_PHRASES = [
    "moreover,",
    "furthermore,",
    "additionally,",
    "in addition,",
    "it's worth noting that",
    "it is worth noting that",
    "interestingly,",
    "importantly,",
    "notably,",
]

VAGUE_ATTRIBUTIONS = [
    "experts say",
    "experts believe",
    "studies show",
    "studies suggest",
    "research shows",
    "research indicates",
    "research suggests",
    "many believe",
    "many argue",
    "some argue",
    "it is widely believed",
    "it has been shown",
]

FILLER_OPENINGS = [
    "in today's fast-paced world",
    "in today's rapidly changing",
    "in an era of",
    "in the age of",
    "when it comes to",
    "it goes without saying",
    "needless to say",
    "as we all know",
    "in the modern world",
    "in this day and age",
]

NEGATIVE_PARALLELISM = [
    r"not just .{0,40} but ",
    r"not merely .{0,40} but ",
    r"not only .{0,40} but ",
    r"not a .{0,40} but a ",
]

FAKE_ENTHUSIASM = [
    r"!\s",  # exclamation mark followed by space (sentence-level)
    r"!$",   # exclamation mark at end of line
    r"\bexcited\b",
    r"\bthrilled\b",
    r"\bpassionate about\b",
    r"\bdelighted to\b",
]

PROMOTIONAL = [
    "remarkable",
    "transformative",
    "revolutionise", "revolutionize", "revolutionary",
    "unprecedented",
    "exceptional",
    "outstanding",
    "world-class",
    "best-in-class",
    "industry-leading",
    "market-leading",
]


def count_em_dashes(text: str) -> tuple[int, list[str]]:
    lines = text.splitlines()
    hits = []
    total = 0
    for i, line in enumerate(lines, 1):
        count = line.count("—")
        if count:
            total += count
            hits.append(f"  Line {i}: {count}× — \"{line.strip()[:80]}\"")
    return total, hits


def count_words(text: str) -> int:
    return len(text.split())


def check_vocabulary(text: str) -> list[tuple[str, int]]:
    text_lower = text.lower()
    hits = []
    for word in AI_VOCABULARY:
        if " " in word or "-" in word:
            count = text_lower.count(word)
        else:
            pattern = rf"\b{re.escape(word)}\b"
            count = len(re.findall(pattern, text_lower))
        if count:
            hits.append((word, count))
    return hits


def check_rule_of_three(text: str) -> list[str]:
    # Look for comma-separated lists of exactly three items (common AI pattern)
    pattern = r"\b\w+(?:\s+\w+)?,\s+\w+(?:\s+\w+)?,\s+and\s+\w+(?:\s+\w+)?\b"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [m[:80] for m in matches[:5]]  # cap at 5 examples


def check_conjunctives(text: str) -> list[tuple[str, int]]:
    text_lower = text.lower()
    hits = []
    for phrase in CONJUNCTIVE_PHRASES:
        count = text_lower.count(phrase)
        if count:
            hits.append((phrase, count))
    return hits


def check_vague_attribution(text: str) -> list[tuple[str, int]]:
    text_lower = text.lower()
    hits = []
    for phrase in VAGUE_ATTRIBUTIONS:
        count = text_lower.count(phrase)
        if count:
            hits.append((phrase, count))
    return hits


def check_filler_openings(text: str) -> list[str]:
    text_lower = text.lower()
    hits = []
    for phrase in FILLER_OPENINGS:
        if phrase in text_lower:
            hits.append(phrase)
    return hits


def check_negative_parallelism(text: str) -> list[str]:
    hits = []
    for pattern in NEGATIVE_PARALLELISM:
        matches = re.findall(pattern, text, re.IGNORECASE)
        hits.extend(m[:80] for m in matches[:3])
    return hits


def check_promotional(text: str) -> list[tuple[str, int]]:
    text_lower = text.lower()
    hits = []
    for word in PROMOTIONAL:
        if " " in word or "-" in word:
            count = text_lower.count(word)
        else:
            pattern = rf"\b{re.escape(word)}\b"
            count = len(re.findall(pattern, text_lower))
        if count:
            hits.append((word, count))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Path to text file. Omit to read stdin.")
    parser.add_argument("--count-only", action="store_true",
                        help="Print total pattern count only, no detail")
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

    word_count = count_words(text)

    # Run all checks
    em_count, em_lines = count_em_dashes(text)
    em_per_500 = em_count / max(word_count / 500, 1)
    em_flag = em_per_500 > 1

    vocab_hits = check_vocabulary(text)
    three_hits = check_rule_of_three(text)
    conjunctive_hits = check_conjunctives(text)
    attribution_hits = check_vague_attribution(text)
    filler_hits = check_filler_openings(text)
    parallel_hits = check_negative_parallelism(text)
    promo_hits = check_promotional(text)

    total_patterns = (
        (1 if em_flag else 0)
        + len(vocab_hits)
        + (1 if len(three_hits) > 1 else 0)
        + len(conjunctive_hits)
        + len(attribution_hits)
        + len(filler_hits)
        + len(parallel_hits)
        + len(promo_hits)
    )

    if args.count_only:
        print(total_patterns)
        return 0 if total_patterns == 0 else 1

    print("=" * 60)
    print("HUMANISER PATTERN CHECK")
    print(f"Words: {word_count}  |  Patterns found: {total_patterns}")
    print("=" * 60)

    any_found = False

    if em_flag:
        any_found = True
        print(f"\n[FAIL] 1. EM DASH OVERUSE — {em_count} em dashes ({em_per_500:.1f} per 500 words, threshold: 1)")
        for line in em_lines[:5]:
            print(line)

    if vocab_hits:
        any_found = True
        print(f"\n[FAIL] 2. AI VOCABULARY — {len(vocab_hits)} word(s) found")
        for word, count in sorted(vocab_hits, key=lambda x: -x[1]):
            print(f"  '{word}' × {count}")

    if len(three_hits) > 1:
        any_found = True
        print(f"\n[WARN] 3. RULE OF THREE — {len(three_hits)} three-item lists found")
        for example in three_hits[:3]:
            print(f"  \"{example}\"")

    if conjunctive_hits:
        any_found = True
        print(f"\n[FAIL] 6. CONJUNCTIVE PHRASES — {len(conjunctive_hits)} found")
        for phrase, count in conjunctive_hits:
            print(f"  '{phrase}' × {count}")

    if attribution_hits:
        any_found = True
        print(f"\n[FAIL] 8. VAGUE ATTRIBUTION — {len(attribution_hits)} found")
        for phrase, count in attribution_hits:
            print(f"  '{phrase}' × {count}")

    if filler_hits:
        any_found = True
        print(f"\n[FAIL] 9. FILLER OPENINGS — {len(filler_hits)} found")
        for phrase in filler_hits:
            print(f"  '{phrase}'")

    if parallel_hits:
        any_found = True
        print(f"\n[WARN] 7. NEGATIVE PARALLELISM — {len(parallel_hits)} found")
        for example in parallel_hits:
            print(f"  \"{example}\"")

    if promo_hits:
        any_found = True
        print(f"\n[FAIL] 4. PROMOTIONAL INFLATION — {len(promo_hits)} word(s) found")
        for word, count in sorted(promo_hits, key=lambda x: -x[1]):
            print(f"  '{word}' × {count}")

    print("\n" + "-" * 60)
    if not any_found:
        print("OVERALL: CLEAN — no AI patterns detected")
        return 0
    else:
        print(f"OVERALL: {total_patterns} pattern(s) found — rewrite before presenting")
        return 1


if __name__ == "__main__":
    sys.exit(main())
