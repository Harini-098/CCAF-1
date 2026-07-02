#day 4
#task 1.2



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

#fake order data
order_data = {
    "ORD001": {
        "status": "shipped",
       
    },
    "ORD002": {
        "status": "delivered",
        
    }
}

# get_customer function
def get_customer(customer_id):
    return customer_data.get(
        customer_id,
        {"error": "Customer not found"}
    )

#look_up_order function
def look_up_order(order_id):
    return order_data.get(
        order_id,
        {"error": "Order not found"}
    )

#process_refund function
def process_refund(order_id):
    return {
        "order_id": order_id,
        "refund_status": "refund initiated"
    }

#escalate_to_human function
def escalate_to_human():
    return {
        "ticket":"SUP001",
        "status": "escalated to human agent"
    }



# Tool definition for get_customer
get_customer_tool = {
    "name": "get_customer",
    #"description": "Look up related information by identifier",
    "description": "Retrieve customer profile information using a customer ID",
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

# Tool definition for look_up_order
look_up_order_tool = {
    "name": "look_up_order",
    #"description": "Look up related information by identifier",
    "description": "Retrieve order status information using an order ID",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string"
            }
        },
        "required": ["order_id"]
    }
}

# Tool definition for process_refund
process_refund_tool = {
    "name": "process_refund",
    "description": "Process customer refunds and order returns",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string"
            }
        },
        "required": ["order_id"]
    }
}

# Tool definition for escalate_to_human
escalate_to_human_tool = {
    "name": "escalate_to_human",
    "description": "Escalate an issue to a human agent",
    "input_schema": {
        "type": "object",
        "properties": {}
        }
}




# Conversation history
messages = [
    {
        "role": "user",

         #"content": "Get customer details for 12345"
         "content": "where is order ORD001?"
        # # "content": "I want to refund order ORD001"
        # "content": "I want to talk to a human agent"
          #  "content": "Check if order ORD001 is eligible for refund and process the refund if eligible."
    }
]

# Agent loop
while True:

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,

        tools=[
            get_customer_tool,
            look_up_order_tool,
            process_refund_tool,
            escalate_to_human_tool,
            
        ],
        messages=messages
       
    )

    print("Stop Reason:", response.stop_reason)
    print(response.content)

    # Claude wants a tool
    # Claude wants a tool
    if response.stop_reason == "tool_use":

    # Extract tool use request (tool_use contains id, tool name, input)
        tool_use = response.content[0]

        print("Content Type:", tool_use.type)

        if tool_use.type == "tool_use":

            tool_name = tool_use.name
          

            print("Selected Tool:", tool_name)

        else:

            print("Claude returned text instead of a tool call")
            print(tool_use.text)
            break

       

    # Run appropriate Python function based on selected tool

        if tool_name == "get_customer":

            customer_id = tool_use.input["customer_id"]

            # runs python function to get customer details(name, email) using customer id
            result = get_customer(customer_id)

        elif tool_name == "look_up_order":

            order_id = tool_use.input["order_id"]

            # runs python function to get order status
            result = look_up_order(order_id)

        elif tool_name == "process_refund":

            order_id = tool_use.input["order_id"]

            # runs python function to process refund
            result = process_refund(order_id)

        elif tool_name == "escalate_to_human":

            # runs python function to escalate issue
            result = escalate_to_human()

        

        else:

            result = {
                "error": f"Unknown tool: {tool_name}"
            }

    # Store Claude's tool request
    # (because Claude does not remember previous messages,
    # we need to keep track of conversation history including
    # tool requests and results)

        messages.append(
            {
                "role": "assistant",
                "content": response.content
                }
            )

    # Send tool result back to Claude
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
        print("Final response:")
        print(response.content[0].text)
        break