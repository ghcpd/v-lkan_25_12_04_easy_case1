#!/usr/bin/env python3
import json
import argparse
from pathlib import Path


def group_jsonl_by_repo(input_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    groups = {}
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                # skip invalid JSON lines
                continue
            repo = obj.get("repo") or "__unknown__"
            if isinstance(repo, str):
                repo = repo.strip()
            groups.setdefault(repo, []).append(line)

    for repo, lines in groups.items():
        # sanitize repo -> safe filename (replace path separators and common unsafe chars)
        safe_name = (repo.replace("/", "__")
                     .replace("\\", "__")
                     .replace(" ", "_")
                     .replace(":", "_")
                     .replace("@", "_") )
        out_file = output_dir / f"{safe_name}.jsonl"
        with out_file.open("w", encoding="utf-8") as wf:
            for l in lines:
                wf.write(l + "\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Group JSONL records by repo field")
    p.add_argument("input", type=Path, help="Path to repo_metadata.jsonl")
    p.add_argument("--out", type=Path, default=Path("grouped"), help="Output directory")
    args = p.parse_args()
    group_jsonl_by_repo(args.input, args.out)
