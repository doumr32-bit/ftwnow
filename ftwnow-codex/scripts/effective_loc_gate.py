#!/usr/bin/env python3
"""Enforce FTWNOW effective line-count gates.

Exit codes:
0: all files <= warn limit
1: at least one file > warn limit and <= halt limit
2: at least one file > halt limit
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from dataclasses import dataclass

DEFAULT_EXTS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".py",
}


@dataclass
class GateResult:
    path: pathlib.Path
    effective_lines: int
    status: str


def iter_candidate_files(paths: list[pathlib.Path], exts: set[str]) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in exts:
            files.append(path)
            continue
        if path.is_dir():
            files.extend(
                p
                for p in path.rglob("*")
                if p.is_file() and p.suffix.lower() in exts and ".git" not in p.parts
            )
    return sorted(set(files))


def is_effective_line(raw_line: str) -> bool:
    line = raw_line.strip()
    if not line:
        return False
    if line.startswith("//"):
        return False
    if line.startswith("#"):
        return False
    return True


def count_effective_lines(path: pathlib.Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return sum(1 for line in text.splitlines() if is_effective_line(line))


def evaluate_file(path: pathlib.Path, warn_limit: int, halt_limit: int) -> GateResult:
    effective = count_effective_lines(path)
    if effective > halt_limit:
        return GateResult(path=path, effective_lines=effective, status="HALT")
    if effective > warn_limit:
        return GateResult(path=path, effective_lines=effective, status="WARN")
    return GateResult(path=path, effective_lines=effective, status="PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check effective LOC gate for FTWNOW projects")
    parser.add_argument("paths", nargs="+", help="Files or directories to check")
    parser.add_argument("--warn-limit", type=int, default=300)
    parser.add_argument("--halt-limit", type=int, default=400)
    parser.add_argument("--ext", action="append", default=[], help="Additional extension, e.g. --ext .go")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    extra_exts = {e if e.startswith(".") else f".{e}" for e in args.ext}
    extensions = DEFAULT_EXTS | {e.lower() for e in extra_exts}

    paths = [pathlib.Path(p).resolve() for p in args.paths]
    candidates = iter_candidate_files(paths, extensions)
    if not candidates:
        print("No candidate files found.")
        return 0

    results = [evaluate_file(path, args.warn_limit, args.halt_limit) for path in candidates]

    print("status\teffective_lines\tfile")
    for result in results:
        print(f"{result.status}\t{result.effective_lines}\t{result.path}")

    halt_count = sum(1 for r in results if r.status == "HALT")
    warn_count = sum(1 for r in results if r.status == "WARN")
    print(f"summary\tHALT={halt_count}\tWARN={warn_count}\tPASS={len(results) - halt_count - warn_count}")

    if halt_count:
        return 2
    if warn_count:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
