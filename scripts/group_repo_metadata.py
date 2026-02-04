#!/usr/bin/env python3
"""
Group records in repo_metadata.jsonl by the `repo` field.

For each unique repo value, a directory will be created under the output
directory using the repo name with `/` replaced by `__`. Inside that
directory a file named `repo_metadata.jsonl` will contain only the records
for that repo (one JSON object per line).

Usage:
  python scripts/group_repo_metadata.py 
  python scripts/group_repo_metadata.py --input repo_metadata.jsonl --output grouped

The script is robust to empty lines and will skip invalid JSON lines with a
warning printed to stderr.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List


def safe_dir_name(repo_name: str) -> str:
    """Replace filesystem-unfriendly characters in a repo name.

    The user specifically asked to replace '/' with '__'. We also strip
    surrounding whitespace.
    """
    return repo_name.strip().replace("/", "__")


def group_by_repo(input_path: str) -> Dict[str, List[dict]]:
    groups: Dict[str, List[dict]] = {}

    with open(input_path, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, start=1):
            line = line.rstrip("\n")
            if not line.strip():
                # skip empty lines
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"warning: skipping invalid json on line {n}: {exc}", file=sys.stderr)
                continue

            repo = obj.get("repo")
            if not repo:
                print(f"warning: skipping record without 'repo' field on line {n}", file=sys.stderr)
                continue

            groups.setdefault(repo, []).append(obj)

    return groups


def write_groups(groups: Dict[str, List[dict]], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)

    for repo, records in groups.items():
        dir_name = safe_dir_name(repo)
        repo_dir = os.path.join(out_dir, dir_name)
        os.makedirs(repo_dir, exist_ok=True)
        out_file = os.path.join(repo_dir, "repo_metadata.jsonl")

        with open(out_file, "w", encoding="utf-8") as fh:
            for rec in records:
                json.dump(rec, fh, ensure_ascii=False)
                fh.write("\n")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Group repo metadata JSONL by repo")
    parser.add_argument("--input", "-i", default="repo_metadata.jsonl", help="input JSONL file")
    parser.add_argument("--output", "-o", default="grouped_repos", help="output base directory")

    args = parser.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"error: input file does not exist: {args.input}", file=sys.stderr)
        return 2

    groups = group_by_repo(args.input)

    if not groups:
        print("no records found to group", file=sys.stderr)
        return 0

    write_groups(groups, args.output)

    print(f"wrote {len(groups)} repo groups into '{args.output}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
