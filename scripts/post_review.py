import json
import os
from pathlib import Path
import requests

# Read review.json
with open("review.json", "r", encoding="utf-8") as f:
    response = json.load(f)

findings = json.loads(response["result"])

if isinstance(findings, dict):
    findings = [findings]

# GitHub info
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]

with open(os.environ["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
    event = json.load(f)

owner, repo_name = repo.split("/")
pr_number = event["pull_request"]["number"]
commit_sha = event["pull_request"]["head"]["sha"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

for finding in findings:

    payload = {
        "body": f"""### {finding['severity'].upper()}

**Finding**
{finding['finding']}

**Suggested Fix**
{finding['suggested_fix']}
""",
        "commit_id": commit_sha,
        "path": finding["file"],
        "line": finding["line"],
        "side": "RIGHT"
    }

    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/comments"

    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
    print(response.text)