import json
from pathlib import Path

review_file = Path("review.json")

with open(review_file, "r", encoding="utf-8") as f:
    response = json.load(f)

# Claude stores the actual JSON inside the "result" field
result = response["result"]

# Convert the JSON string into a Python object
findings = json.loads(result)

# If Claude returned only one finding, convert it to a list
if isinstance(findings, dict):
    findings = [findings]

print(f"Found {len(findings)} finding(s)\n")

for finding in findings:
    print(f"File      : {finding['file']}")
    print(f"Line      : {finding['line']}")
    print(f"Severity  : {finding['severity']}")
    print(f"Finding   : {finding['finding']}")
    print(f"Suggested : {finding['suggested_fix']}")
    print("-" * 60)