#day 3

import os
from anthropic import Anthropic

# Connect to Claude using API key
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Define the tool
tools = [
    {
        "name": "get_customer",
        "description": "Get customer details using a customer ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string"
                }
            },
            "required": ["customer_id"]
        }
    }
]

# send user message
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=10,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "Get details of customer with ID 12345"
        }
    ],
    #force tool usage by specifying the tool choice
    tool_choice={
        "type": "tool",
        "name": "get_customer"
    }
)

# Print full response
print(response)


