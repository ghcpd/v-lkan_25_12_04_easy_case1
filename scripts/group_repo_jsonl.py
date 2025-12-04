#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'repo_metadata.jsonl'
OUT_DIR = ROOT

if not INPUT.exists():
    print(f'Input file not found: {INPUT}')
    raise SystemExit(1)

counts = {}
with INPUT.open('r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print('Failed to parse line as JSON:', e)
            print('Line:', line[:200])
            continue
        repo = obj.get('repo')
        if not repo:
            print('No repo field for object, skipping')
            continue
        dir_name = repo.replace('/', '__')
        target_dir = OUT_DIR / dir_name
        target_dir.mkdir(parents=True, exist_ok=True)
        out_file = target_dir / 'grouped.jsonl'
        with out_file.open('a', encoding='utf-8') as outfh:
            json.dump(obj, outfh, ensure_ascii=False)
            outfh.write('\n')
        counts.setdefault(repo, 0)
        counts[repo] += 1

print('Written grouped JSONL files for repos:')
for repo, n in counts.items():
    print(f' - {repo} -> {n} records')

print('\nCreated files:')
for repo in counts:
    p = OUT_DIR / repo.replace('/', '__') / 'grouped.jsonl'
    print('  {}'.format(p))
