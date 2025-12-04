import json
import sys
from pathlib import Path
import subprocess
import tempfile

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "group_by_repo.py"


def test_grouping_creates_expected_files(tmp_path: Path):
    input_file = tmp_path / "repo_metadata.jsonl"
    out_dir = tmp_path / "out"

    records = [
        {"repo": "a/b", "value": 1},
        {"repo": "a/b", "value": 2},
        {"repo": "c/d", "value": 3},
        {"value": 4},
    ]
    with input_file.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    # run the script
    res = subprocess.run([sys.executable, str(SCRIPT), str(input_file), "--out", str(out_dir)], check=False)
    assert res.returncode == 0

    # check files
    file_ab = out_dir / "a__b.jsonl"
    file_cd = out_dir / "c__d.jsonl"
    file_unknown = out_dir / "__unknown__.jsonl"

    assert file_ab.exists()
    assert file_cd.exists()
    assert file_unknown.exists()

    with file_ab.open() as f:
        lines = f.read().strip().splitlines()
        assert len(lines) == 2
        objs = [json.loads(l) for l in lines]
        assert objs[0]["value"] == 1
        assert objs[1]["value"] == 2

    with file_cd.open() as f:
        lines = f.read().strip().splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["value"] == 3

    with file_unknown.open() as f:
        lines = f.read().strip().splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["value"] == 4
