"""
STEP 4 - The agent loop (the most important step).

The loop:
  1. Ask Claude what to do next
  2. Save Claude's reply in the conversation history
  3. If Claude is not asking for a tool -> it's finished
  4. Otherwise run the tool(s) Claude asked for
  5. Send the results back and go to 1

Run:  python step4_agent.py
"""
import datetime
import os

import anthropic

client = anthropic.Anthropic()


# ---------- TOOLS: plain Python functions ----------
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def list_files(folder="."):
    return "\n".join(sorted(os.listdir(folder)))


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()[:5000]  # keep it short


# Map tool names -> functions, so we can run them by name
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "list_files": list_files,
    "read_file": read_file,
}

# ---------- TOOL DESCRIPTIONS: what Claude sees ----------
tools = [
    {
        "name": "get_current_time",
        "description": "Returns the current local date and time.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "list_files",
        "description": "Lists the files in a folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "folder": {"type": "string", "description": "Folder path, default '.'"}
            },
        },
    },
    {
        "name": "read_file",
        "description": "Reads a text file and returns its contents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path of the file to read"}
            },
            "required": ["path"],
        },
    },
]


# ---------- THE AGENT LOOP ----------
def run_agent(user_request):
    messages = [{"role": "user", "content": user_request}]

    while True:
        # 1. Ask Claude what to do next
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=16000,
            system="You are a helpful assistant. Use tools when they help.",
            tools=tools,
            messages=messages,
        )

        # 2. Save Claude's reply in the conversation history
        messages.append({"role": "assistant", "content": response.content})

        # 3. If Claude isn't asking for a tool, it's finished
        if response.stop_reason != "tool_use":
            break

        # 4. Run every tool Claude asked for
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"🔧 Claude is using: {block.name}({block.input})")
                try:
                    result = TOOL_FUNCTIONS[block.name](**block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        }
                    )
                except Exception as e:
                    # Tell Claude about the error so it can try something else
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True,
                        }
                    )

        # 5. Send ALL results back together in ONE message, then loop again
        messages.append({"role": "user", "content": tool_results})

    # Print Claude's final answer
    for block in response.content:
        if block.type == "text":
            print("\n🤖", block.text)


if __name__ == "__main__":
    run_agent(
        "What time is it? Also, what files are in this folder, "
        "and what does README.md say?"
    )
