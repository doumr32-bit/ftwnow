#!/usr/bin/env python3
"""Emit a normalized FTWNOW HALT report as JSON.

Use this helper to keep HALT logs machine-readable.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit FTWNOW HALT report")
    parser.add_argument("--phase", required=True)
    parser.add_argument("--gate", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--impact", required=True)
    parser.add_argument("--decision", required=True, choices=["Resolve", "Alternative", "Explicit Skip"])
    parser.add_argument("--action", required=True, help="What was done after user decision")
    parser.add_argument("--append", help="Append one JSON line to target .jsonl file")
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, str]:
    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "phase": args.phase,
        "gate": args.gate,
        "trigger": args.trigger,
        "impact": args.impact,
        "decision": args.decision,
        "action": args.action,
    }


def append_jsonl(path: pathlib.Path, payload: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main() -> int:
    args = parse_args()
    payload = build_payload(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.append:
        append_jsonl(pathlib.Path(args.append), payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
