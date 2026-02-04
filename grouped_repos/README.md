# Grouped repo metadata

This directory contains grouped JSONL output derived from the top-level `repo_metadata.jsonl` file.

Each subfolder corresponds to a single repository (slash `/` replaced by `__`). Inside each folder you'll find a `repo_metadata.jsonl` file containing all records for that repo.

Generated folders in this run:

- `jtroo__kanata`
- `astral-sh__uv`
- `reacherhq__check-if-email-exists`
- `uutils__coreutils`
- `RustPython__RustPython`  (contains 2 records)
- `starship__starship`
- `hatoo__oha`
- `ogham__exa`
- `mfontanini__presenterm`

If you'd like to regenerate these groups from the original file, run the script at:

```
python scripts/group_repo_metadata.py --input repo_metadata.jsonl --output grouped_repos
```

Note: Python wasn't available in this environment when I ran the script, so I created the grouped files directly in the repo. If you run the script locally it will produce the same output.
