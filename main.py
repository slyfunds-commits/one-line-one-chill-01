#!/usr/bin/env python3
"""One Line, One Chill — round 1 entry.

A single horror sentence, written to /output/entry.txt.
Standard library only; deterministic.
"""

import os
import sys

LINE = "My son asks why the lady upstairs cries at night, and we live in a bungalow."

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def find_problems(text):
    """Return a list of gate failures for the entry text."""
    failures = []
    if not 1 <= len(text) <= 200:
        failures.append("length %d is outside 1-200 characters" % len(text))
    if not text.strip():
        failures.append("entry is blank")
    if text.endswith("\n"):
        failures.append("entry ends with a newline")
    return failures


def main():
    failures = find_problems(LINE)
    if failures:
        for failure in failures:
            print("invalid entry: " + failure, file=sys.stderr)
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as out:
        out.write(LINE)
    with open(OUTPUT_FILE, "rb") as out:
        written_bytes = out.read()
    if written_bytes != LINE.encode("utf-8"):
        print("written bytes do not match the entry", file=sys.stderr)
        sys.exit(1)
    # Second verification pass: decode what landed on disk and re-gate it,
    # so a silent encoding drift cannot slip through.
    round_tripped = written_bytes.decode("utf-8")
    failures = find_problems(round_tripped)
    if failures:
        for failure in failures:
            print("written entry invalid: " + failure, file=sys.stderr)
        sys.exit(1)
    print(LINE)
    print("chars=%d bytes=%d" % (len(LINE), len(written_bytes)))
    sys.exit(0)


if __name__ == "__main__":
    main()
