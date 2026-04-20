#!/usr/bin/env python3
"""
Validate pitch-research skill output against voice and length rules.

Reads the full skill output (brief + email) from stdin or a file path and
checks the email section for:
- Word count (target: under 150)
- Banned marketing words (voice rules)
- Em dashes (banned in copy)
- American spellings (warning only — British English required)

Exit codes:
  0 = PASS or PASS WITH WARNINGS
  1 = FAIL (banned word, over word count, em dash in email)
  2 = script error (no email section found, bad input)

Usage:
  python3 check-output.py path/to/output.md
  cat output.md | python3 check-output.py
  python3 check-output.py --email-only path/to/email.md
"""

import argparse
import re
import sys
from pathlib import Path

BANNED_WORDS = [
    "transform", "transformative", "transformation",
    "leverage", "leveraging", "leveraged",
    "ai-powered", "ai powered",
    "revolutionise", "revolutionize", "revolutionary",
    "cutting-edge", "cutting edge",
    "10x", "10 x",
    "disruptive", "disrupt", "disruption",
    "game-changing", "game changing", "game-changer",
    "paradigm",
    "unlock", "unlocks", "unlocking",
    "empower", "empowers", "empowering", "empowerment",
    "supercharge", "supercharged",
    "best-in-class", "world-class",
    "synergy", "synergies", "synergistic",
    "seamless", "seamlessly",
    "next-generation", "next gen",
    "ecosystem",
    "deep dive",
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
    "flavor": "flavour",
    "neighbor": "neighbour",
    "defense": "defence",
    "offense": "offence",
    "license": "licence",
    "practice": "practise",  # verb form only — flag as warning
}

EMAIL_WORD_CAP = 150

EMAIL_MARKERS = [
    r"^##\s+Draft\s+Email\s*$",
    r"^##\s+Email\s*$",
    r"^###\s+Email\s*$",
    r"^\*\*Subject:\*\*",
    r"^Subject:",
]

# Sign-off patterns — the email body ends at the sign-off line (inclusive of
# the signature name that follows, exclusive of any footer notes or
# annotations after it). See README or SKILL.md for the rationale.
SIGNOFF_PATTERNS = [
    r"^best,?\s*$",
    r"^best\s+regards,?\s*$",
    r"^kind\s+regards,?\s*$",
    r"^warm\s+regards,?\s*$",
    r"^regards,?\s*$",
    r"^thanks,?\s*$",
    r"^thank\s+you,?\s*$",
    r"^cheers,?\s*$",
    r"^sincerely,?\s*$",
    r"^yours\s+sincerely,?\s*$",
    r"^all\s+the\s+best,?\s*$",
    r"^speak\s+soon,?\s*$",
]


def extract_email(text: str) -> str | None:
    """Return the email section of the output, or None if not found."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        for marker in EMAIL_MARKERS:
            if re.match(marker, line.strip(), re.IGNORECASE):
                start = i
                break
        if start is not None:
            break

    if start is None:
        return None

    # Email runs until next ## header or end of file
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^##\s", lines[i]):
            end = i
            break

    return "\n".join(lines[start:end])


def find_signoff_index(lines: list[str]) -> int | None:
    """Find the line index of the sign-off (e.g. 'Best,', 'Kind regards,').

    Returns the index of the line AFTER the sign-off's signature line, which is
    typically the name. So an email ending with:

        Best,
        Paul

        *[Footer annotation]*

    will return the index of the blank line after 'Paul', meaning the body
    (Best, + Paul) is kept and everything after is excluded.
    """
    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        if not stripped:
            continue
        # Strip markdown bold/italic so "**Best,**" also matches
        cleaned = re.sub(r"[*_]+", "", stripped)
        for pattern in SIGNOFF_PATTERNS:
            if re.match(pattern, cleaned):
                # Keep this line (sign-off) + the next non-empty line (name)
                name_index = None
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        name_index = j
                        break
                if name_index is not None:
                    return name_index + 1
                return i + 1
    return None


def count_email_words(email_text: str) -> int:
    """Count words in the email body, excluding Subject: line and markdown.

    Cuts the body at the sign-off line so footer annotations, word-count
    notes, and other post-signature content don't inflate the count.
    """
    lines = email_text.splitlines()
    # Cut at sign-off if present
    signoff_end = find_signoff_index(lines)
    if signoff_end is not None:
        lines = lines[:signoff_end]

    body_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip headers, subject line, empty lines, and markdown bold markers
        if re.match(r"^#+\s", stripped):
            continue
        if re.match(r"^\*?\*?Subject:", stripped, re.IGNORECASE):
            continue
        if not stripped:
            continue
        # Strip markdown formatting
        cleaned = re.sub(r"\*+", "", stripped)
        body_lines.append(cleaned)

    body = " ".join(body_lines)
    words = body.split()
    return len(words)


def find_banned_words(text: str) -> list[tuple[str, int]]:
    """Return list of (word, count) for any banned words found."""
    text_lower = text.lower()
    hits = []
    for word in BANNED_WORDS:
        # Use word boundary matching for single words, substring for hyphenated
        if "-" in word or " " in word:
            count = text_lower.count(word)
        else:
            pattern = rf"\b{re.escape(word)}\b"
            count = len(re.findall(pattern, text_lower))
        if count > 0:
            hits.append((word, count))
    return hits


def find_em_dashes(text: str) -> int:
    """Count em dashes (—) in the text. Excludes code blocks."""
    # Strip code blocks first
    no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return no_code.count("—")


def find_american_spellings(text: str) -> list[tuple[str, str]]:
    """Return list of (american, british) spellings found."""
    text_lower = text.lower()
    hits = []
    for american, british in AMERICAN_SPELLINGS.items():
        pattern = rf"\b{re.escape(american)}\b"
        if re.search(pattern, text_lower):
            hits.append((american, british))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Path to output file. Omit to read stdin.")
    parser.add_argument("--email-only", action="store_true",
                        help="Input is just the email, skip brief extraction")
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

    if args.email_only:
        email = text
    else:
        email = extract_email(text)
        if email is None:
            print("ERROR: could not find email section. Expected a '## Draft Email' header or 'Subject:' line.", file=sys.stderr)
            return 2

    # Run checks
    word_count = count_email_words(email)
    word_pass = word_count <= EMAIL_WORD_CAP

    banned_in_output = find_banned_words(text)
    banned_in_email = find_banned_words(email)
    banned_pass = len(banned_in_email) == 0

    email_em_dashes = find_em_dashes(email)
    em_dash_pass = email_em_dashes == 0

    american_in_output = find_american_spellings(text)
    american_pass = len(american_in_output) == 0  # warning only

    # Print report
    print("=" * 60)
    print("PITCH-RESEARCH OUTPUT CHECK")
    print("=" * 60)

    status = "PASS" if word_pass else "FAIL"
    print(f"WORD COUNT (email): {word_count} / {EMAIL_WORD_CAP} [{status}]")

    if banned_in_email:
        print(f"BANNED WORDS (email): FAIL — {len(banned_in_email)} found")
        for word, count in banned_in_email:
            print(f"  - '{word}' ({count}x)")
    else:
        print("BANNED WORDS (email): PASS")

    if banned_in_output and not banned_in_email:
        print(f"BANNED WORDS (brief only): WARN — {len(banned_in_output)} found")
        for word, count in banned_in_output:
            print(f"  - '{word}' ({count}x)")

    status = "PASS" if em_dash_pass else "FAIL"
    print(f"EM DASHES (email): {email_em_dashes} [{status}]")

    if american_in_output:
        print(f"BRITISH SPELLING: WARN — {len(american_in_output)} American spellings found")
        for american, british in american_in_output:
            print(f"  - '{american}' → should be '{british}'")
    else:
        print("BRITISH SPELLING: PASS")

    print("-" * 60)

    hard_fail = not (word_pass and banned_pass and em_dash_pass)
    has_warnings = bool(american_in_output) or bool(banned_in_output and not banned_in_email)

    if hard_fail:
        print("OVERALL: FAIL — fix before sending")
        return 1
    elif has_warnings:
        print("OVERALL: PASS WITH WARNINGS — review before sending")
        return 0
    else:
        print("OVERALL: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
