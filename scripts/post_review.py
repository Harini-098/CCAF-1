import json
import os

print("Repository:", os.environ.get("GITHUB_REPOSITORY"))
print("Event file:", os.environ.get("GITHUB_EVENT_PATH"))
print("GitHub Token Exists:", "Yes" if os.environ.get("GITHUB_TOKEN") else "No")