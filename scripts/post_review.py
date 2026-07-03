import json
import os
from pathlib import Path

# -----------------------------
# Read review.json
# -----------------------------
project_root = Path(__file__).resolve().parent.parent
review_file = project_root / "review.json"

if not review_file.exists():
    raise FileNotFoundError(f"{review_file} not found")

with open(review_file, "r", encoding="utf-8") as f:
    findings = json.load(f)

print(f"Found {len(findings)} finding(s)\n")

# -----------------------------
# GitHub Environment
# -----------------------------
repository = os.getenv("GITHUB_REPOSITORY")
event_path = os.getenv("GITHUB_EVENT_PATH")
token = os.getenv("GITHUB_TOKEN")

print("Repository:", repository)
print("Event File:", event_path)
print("GitHub Token:", "Available" if token else "Missing")

# -----------------------------
# Read Pull Request information
# -----------------------------
if event_path and Path(event_path).exists():
    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    pr_number = event["pull_request"]["number"]
    commit_sha = event["pull_request"]["head"]["sha"]

    print("PR Number :", pr_number)
    print("Commit SHA:", commit_sha)
else:
    print("\nRunning locally (no GitHub event).")
    pr_number = None
    commit_sha = None

# -----------------------------
# Prepare payloads
# -----------------------------
print("\nPreparing GitHub Review Comments...\n")

for finding in findings:

    payload = {
        "body": (
            f"### {finding['severity'].upper()} Severity\n\n"
            f"**Finding:**\n{finding['finding']}\n\n"
            f"**Suggested Fix:**\n{finding['suggested_fix']}"
        ),
        "commit_id": commit_sha,
        "path": finding["file"],
        "line": finding["line"],
        "side": "RIGHT"
    }

    print(json.dumps(payload, indent=4))
    print("-" * 80)