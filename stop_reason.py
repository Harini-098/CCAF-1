#day 2

import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude!"
        }
    ]
)

print(response)
print("Stop reason:", response.stop_reason)