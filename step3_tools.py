"""
STEP 3 - Define a tool.

A tool has two parts:
  1) A real Python function (the "hands" - does the work)
  2) A description Claude reads (the "menu card" - says what the tool does)

This file does NOT call Claude. It only shows what a tool looks like.
Run:  python step3_tools.py
"""
import datetime


# 1) The real function
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# A tool that takes an input, for comparison
def greet(name):
    return f"Hello, {name}!"


# 2) The descriptions Claude reads
tools = [
    {
        "name": "get_current_time",
        "description": "Returns the current local date and time.",
        "input_schema": {"type": "object", "properties": {}},  # no inputs needed
    },
    {
        "name": "greet",
        "description": "Greets a person by their name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The person's name"}
            },
            "required": ["name"],  # Claude must always provide this
        },
    },
]


if __name__ == "__main__":
    # Try the functions yourself, just like the agent loop will later
    print(get_current_time())
    print(greet(name="Sameh"))
    print("Tools Claude will see:", [t["name"] for t in tools])
