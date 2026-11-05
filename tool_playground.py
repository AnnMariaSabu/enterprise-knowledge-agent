import ollama

import config


def add_numbers(a, b):
    return a + b


add_tool = {
    "type": "function",
    "function": {
        "name": "add_numbers",
        "description": "Add two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number"},
                "b": {"type": "number", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
}

messages = [{"role": "user", "content": "What is 1234 plus 5678?"}]

response = ollama.chat(
    model=config.CHAT_MODEL,
    messages=messages,
    tools=[add_tool],
    options={"temperature": 0},
)

messages.append(response.message)

for call in response.message.tool_calls:
    name = call.function.name
    args = call.function.arguments
    print("1. AI asked for:", name, args)

    if name == "add_numbers":
        result = add_numbers(float(args["a"]), float(args["b"]))
        print("2. Our code ran it ->", result)
        messages.append({"role": "tool", "content": str(result)})

final = ollama.chat(
    model=config.CHAT_MODEL,
    messages=messages,
    tools=[add_tool],
    options={"temperature": 0},
)

print("3. Final answer:", final.message.content)