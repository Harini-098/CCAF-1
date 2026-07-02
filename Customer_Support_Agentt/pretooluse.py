#day 8 

#day 7 
#create verify_eligibility subagent 





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
        "amount": 300
       
    },
    "ORD002": {
        "status": "delivered",
        "amount": 501
        
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

#verify_eligibility function
# verify_eligibility subagent

def verify_eligibility(order_id):

    if order_id in order_data:
        return {
            "eligible": True,
            "reason": "Order found and eligible for refund"
        }

    return {
        "eligible": False,
        "reason": "Order not found"
    }

#Hook Function for process_refund over $500
def refund_gate_hook(order_id):

    order = order_data.get(order_id)

    if not order:
        return False

    if order["amount"] > 500:
        return False

    return True


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

# Tool definition for verify_eligibility

verify_eligibility_tool = {
    "name": "verify_eligibility",
    "description": "Check whether an order is eligible for refund before processing refunds",
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



# Conversation history
messages = [
    {
        "role": "user",
        "content":"I want a refund for order ORD002"
    }
]

# Agent loop
while True:

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
         system="""
            Before using process_refund,
            always call verify_eligibility first.

            If eligible is false,
            use escalate_to_human.

            Never call process_refund directly.
            """,

        tools=[
            get_customer_tool,
            look_up_order_tool,
            process_refund_tool,
            escalate_to_human_tool,
            verify_eligibility_tool
        ],
        messages=messages
       
    )

    print("Stop Reason:", response.stop_reason)
    print(response.content)

    # Claude wants a tool
    # Claude wants a tool
    if response.stop_reason == "tool_use":

    # Extract tool use request (tool_use contains id, tool name, input)
        # Find tool_use block

        tool_use = None

        for block in response.content:

            print("Content Type:", block.type)

            if block.type == "tool_use":
                tool_use = block
                break

        # No tool found

        if tool_use is None:

            print("No tool call found")

            for block in response.content:
                if block.type == "text":
                    print(block.text)

            break

        # Tool found

        tool_name = tool_use.name

        print("Selected Tool:", tool_name)

       

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

            # PreToolUse Hook

            if not refund_gate_hook(order_id):

                print("HOOK BLOCKED REFUND")

                result = escalate_to_human()

            else:

                result = process_refund(order_id)
        
        elif tool_name == "verify_eligibility":

            order_id = tool_use.input["order_id"]

            # runs python function to verify refund eligibility
            result = verify_eligibility(order_id)

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

