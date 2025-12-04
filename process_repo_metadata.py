import json
import os
from pathlib import Path
from collections import defaultdict

# Read the JSONL file
input_file = "repo_metadata.jsonl"
output_dir = "repo_groups"

# Create output directory if it doesn't exist
Path(output_dir).mkdir(exist_ok=True)

# Dictionary to group records by repo
repo_groups = defaultdict(list)

# Read the JSONL file line by line
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            record = json.loads(line)
            repo = record.get("repo")
            if repo:
                repo_groups[repo].append(record)

# Write each repo's records to a separate JSONL file
for repo, records in repo_groups.items():
    # Replace "/" with "__" for the filename
    safe_filename = repo.replace("/", "__")
    output_file = os.path.join(output_dir, f"{safe_filename}.jsonl")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for record in records:
            json.dump(record, f)
            f.write('\n')
    
    print(f"Created {output_file} with {len(records)} record(s)")

print(f"\nTotal repositories processed: {len(repo_groups)}")
