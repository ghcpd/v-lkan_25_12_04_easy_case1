import json
from pathlib import Path

root = Path(__file__).parent
src = root / 'repo_metadata.jsonl'
if not src.exists():
    print('Source file not found:', src)
    raise SystemExit(1)

with src.open('r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception as e:
            print(f'Failed to parse JSON on line {i}:', e)
            continue
        repo = obj.get('repo')
        if not repo:
            print(f'No repo field on line {i}, skipping')
            continue
        folder_name = repo.replace('/', '__')
        out_dir = root / folder_name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / 'records.jsonl'
        # append the original line
        with out_file.open('a', encoding='utf-8') as outf:
            outf.write(line + '\n')

print('Grouping complete')
