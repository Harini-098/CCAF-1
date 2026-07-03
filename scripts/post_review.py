import json
from pathlib import Path

review_file = Path("review.json")

print("Review file exists:", review_file.exists())

with open(review_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Type:", type(data))

if isinstance(data, list):
    print("Length:", len(data))
    print("First item:")
    print(data[0])

elif isinstance(data, dict):
    print("Keys:")
    print(data.keys())