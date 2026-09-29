"""
STEP 6 - A chat agent you can talk to, with memory and a safety check.

New ideas in this step:
  - A `while True` chat loop that keeps `messages` between turns,
    so the agent remembers the whole conversation.
  - A tool that CHANGES something (save_note). Before running it,
    we ask you to approve it.

Run:  python step6_chat_agent.py      (type 'quit' to exit)
"""
import datetime

import anthropic

client = anthropic.Anthropic()

NOTES_FILE = "notes.txt"


# ---------- TOOLS ----------
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_note(text):
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Note saved."


def read_notes():
    try:
        with open(NOTES_FILE, encoding="utf-8") as f:
            return f.read() or "(no notes yet)"
    except FileNotFoundError:
        return "(no notes yet)"


TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "save_note": save_note,
    "read_notes": read_notes,
}

# Tools that change something need your approval first
NEEDS_APPROVAL = {"save_note"}

tools = [
    {
        "name": "get_current_time",
        "description": "Returns the current local date and time.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "save_note",
        "description": "Saves a short note for the user to a notes file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The note to save"}
            },
            "required": ["text"],
        },
    },
    {
        "name": "read_notes",
        "description": "Reads all notes the user has saved.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

SYSTEM_PROMPT = (
    "You are a friendly personal assistant. You can tell the time and "
    "save and read notes for the user. Keep answers short."
)


def run_tool(block):
    """Run one tool Claude asked for and return a tool_result."""
    if block.name in NEEDS_APPROVAL:
        answer = input(f"⚠️  Allow {block.name}({block.input})? [y/n] ")
        if answer.strip().lower() != "y":
            return {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": "The user declined this action.",
                "is_error": True,
            }
    try:
        result = TOOL_FUNCTIONS[block.name](**block.input)
        return {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
    except Exception as e:
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": f"Error: {e}",
            "is_error": True,
        }


def main():
    messages = []  # lives OUTSIDE the chat loop -> the agent remembers everything
    print("Chat with your agent. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            break
        if not user_input:
            continue
        messages.append({"role": "user", "content": user_input})

        # The same agent loop as step 4
        while True:
            response = client.messages.create(
                model="claude-opus-5-5",
                max_tokens=16000,
                system=SYSTEM_PROMPT,
                tools=tools,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                break

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 {block.name}({block.input})")
                    tool_results.append(run_tool(block))
            messages.append({"role": "user", "content": tool_results})

        for block in response.content:
            if block.type == "text":
                print("🤖", block.text, "\n")


if __name__ == "__main__":
    main()
