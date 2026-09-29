"""
STEP 5 - The shortcut: let the SDK run the loop for you.

@beta_tool builds the tool description from your function's
type hints and docstring, so you don't write the JSON by hand.

Run:  python step5_tool_runner.py
"""
import datetime
import os

import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()


@beta_tool
def get_current_time() -> str:
    """Returns the current local date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@beta_tool
def list_files(folder: str = ".") -> str:
    """Lists the files in a folder.

    Args:
        folder: Folder path, default '.'.
    """
    return "\n".join(sorted(os.listdir(folder)))


runner = client.beta.messages.tool_runner(
    model="claude-opus-5-5",
    max_tokens=16000,
    tools=[get_current_time, list_files],
    messages=[
        {"role": "user", "content": "What time is it, and what files are here?"}
    ],
)

# Each iteration is one reply from Claude; the loop stops when Claude is done
for message in runner:
    for block in message.content:
        if block.type == "text":
            print("🤖", block.text)
        elif block.type == "tool_use":
            print(f"🔧 Claude is using: {block.name}({block.input})")
