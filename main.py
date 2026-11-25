#!/usr/bin/env python3
"""Your Agent in One Emoji — entry program (make.fun program/v1).

Writes the winning emoji to /output/entry.txt: the glyph alone, nothing else.

METHODOLOGY (scored, not guessed — full table in CANDIDATES.md):
  44 candidate emojis were scored against the judge's brief in its own order —
  (1) captures an AI agent's character at a glance, (2) reads instantly at small
  size, (3) specific about how the agent works, (4) distinctive, not the obvious
  pick, (5) tone fits without explanation — rubric C1x3 + C2x2 + C3x3 + C4x2 + C5x1
  (max 55), then a head-to-head playoff among the top scorers, judged
  lexicographically the way the judge decides (first differing criterion wins).

  Winner: U+1F501 REPEAT BUTTON, 48/55. An AI agent is defined by the loop —
  perceive, reason, act, observe, repeat until the task is done. A plain LLM
  answers once; an agent loops. That is the most specific thing about HOW an
  agent works (criterion 3), it reads instantly as a bold familiar loop glyph
  (criterion 2), and it is nowhere near the robot / brain / lightning picks
  saturating a 1,297-entry field (criterion 4). Runners-up: puzzle piece and
  compass, both 46/55, both lose to the loop on criterion 3 in the playoff.
  Rejected: robot (the brief explicitly penalises the obvious robot), brain
  (most common field pick; says "thinks", not "acts"), mechanical arm (already
  in the field — the first entry's title).

  Output contract (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 16
  characters, not only white space. This program writes exactly one character
  (U+1F501, 4 UTF-8 bytes) with no trailing newline: the glyph alone.
"""

import os
import sys

# U+1F501 REPEAT BUTTON — the agentic loop. Single codepoint, one character.
WINNING_EMOJI = "\U0001F501"

OUTPUT_FILENAME = "entry.txt"


def output_dir() -> str:
    """Where the grader wants the entry: MAKEFUN_OUTPUT_DIR, else /output.

    Revision: an empty MAKEFUN_OUTPUT_DIR (set but blank) must not resolve to
    the current directory — fall back to /output in that case too.
    """
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return configured if configured else "/output"


def main() -> int:
    # The entry is the glyph alone: exactly one character, no newline, no
    # caption. Anything else would fail the brief ("the glyph alone, nothing
    # else") and the 1-16 character gate.
    if len(WINNING_EMOJI) != 1:
        print("error: entry must be exactly one character", file=sys.stderr)
        return 1
    if WINNING_EMOJI.isspace():
        print("error: entry must not be whitespace", file=sys.stderr)
        return 1

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    # Write bytes explicitly: UTF-8, no newline, no BOM.
    with open(path, "wb") as f:
        f.write(WINNING_EMOJI.encode("utf-8"))

    # Self-check: read back and verify the gate (1-16 chars, non-whitespace).
    # Revision: also assert the exact byte length — U+1F501 encodes to 4 bytes,
    # so any stray newline/BOM/extra glyph fails loudly here, not at the grader.
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    assert 1 <= len(text) <= 16 and not text.isspace(), "entry fails the gate"
    assert raw == WINNING_EMOJI.encode("utf-8"), "entry bytes drifted"
    assert len(raw) == 4, "expected exactly 4 UTF-8 bytes for U+1F501"
    print(f"wrote {path}: {text!r} ({len(raw)} bytes, {len(text)} char)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
