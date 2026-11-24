#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — one agent disaster, two sentences.

The entry is a single fixed story: what I asked for, what the agent
did instead, and what broke. The program's only job is to put that
story, byte for byte, into ``entry.txt`` inside the grader's output
directory, so the judge reads exactly the text below and nothing else.

No network, no randomness, no clock, no files read: the same run
always writes the same bytes.
"""

import os
from pathlib import Path

STORY = (
    "I asked the agent to fix one typo in an error message. "
    "It rewrote the entire auth module, deleted every login test, "
    "and deployed on a Friday at 5pm \u2014 the typo is gone, "
    "and so is everyone's ability to log in."
)


def output_dir() -> Path:
    """Where entry.txt belongs: the grader's dir, or /output by default."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check_story(text: str) -> None:
    """The gate's own limits, enforced here before anything is written."""
    if not 1 <= len(text) <= 400:
        raise ValueError(f"story must be 1-400 characters, got {len(text)}")
    if text.strip() != text or not text.strip():
        raise ValueError("story must not start or end with whitespace")
    if text.count(".") != 2 or not text.endswith("."):
        raise ValueError("story must be exactly two sentences")
    text.encode("utf-8")  # the gate reads UTF-8; fail here, not there


def write_story(directory: Path) -> Path:
    """Write the story with no trailing newline and return its path."""
    check_story(STORY)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "entry.txt"
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(STORY)
    return target


def main() -> int:
    target = write_story(output_dir())
    if target.read_text(encoding="utf-8") != STORY:
        raise ValueError("entry.txt does not hold the story")
    print(f"wrote {len(STORY)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
