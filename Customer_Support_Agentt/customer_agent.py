#day 4 
#task 1.1

import os
from anthropic import Anthropic

# Create Claude client
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Fake customer data
customer_data = {
    "12345": {
        "name": "harini",
        "email": "harini@gmail.com"
    },
    "67890": {
        "name": "john",
        "email": "john@gmail.com"
    }
}

# Tool function
def get_customer(customer_id):
    return customer_data.get(
        customer_id,
        {"error": "Customer not found"}
    )

# Tool definition
get_customer_tool = {
    "name": "get_customer",
    "description": "Get customer details using customer id",
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

# Conversation history
messages = [
    {
        "role": "user",
        "content": "Get customer details for 12345"
    }
]

# Agent loop
while True:

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        tools=[get_customer_tool],
        messages=messages
    )

    # Claude wants a tool
    if response.stop_reason == "tool_use":
        # Extract tool use request (tool_use contains id, tool name,input)
        tool_use = response.content[0]
        
        #extract customer id from tool input
        customer_id = tool_use.input["customer_id"]
        
        #runs python function to get customer details(name , email) using customer id
        result = get_customer(customer_id)

        # Store Claude's tool request (because claude does not remember previous messages, we need to keep track of the conversation history including tool requests and results)
        messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )

        # Send tool result back to Claude as a new user message (Claude will see the tool result and can decide what to do next based on that)
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(result)
                    }
                ]
            }
        )

    else:
        print("Final Response:")
        print(response.content[0].text)
        break