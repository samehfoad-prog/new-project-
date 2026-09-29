"""
STEP 7b - An agent that gets its tools from an MCP server.

What changes compared to step 6:
  - We do NOT write the tools here. We start an MCP server
    (step7_mcp_server.py) and ASK it which tools it has.
  - When Claude wants a tool, we ask the MCP server to run it.
The agent loop itself is exactly the same as in steps 4 and 6.

Run:  python step7_mcp_agent.py      (type 'quit' to exit)
"""
import asyncio
import sys

import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = anthropic.AsyncAnthropic()

# How to start the MCP server: "python step7_mcp_server.py"
SERVER = StdioServerParameters(command=sys.executable, args=["step7_mcp_server.py"])

# Tools that change something need your approval first
NEEDS_APPROVAL = {"save_note", "clear_notes"}

SYSTEM_PROMPT = (
    "You are a friendly personal assistant. Use your tools to help the user. "
    "Keep answers short."
)


async def run_tool(session, block):
    """Ask the MCP server to run one tool and return a tool_result."""
    if block.name in NEEDS_APPROVAL:
        answer = input(f"⚠️  Allow {block.name}({block.input})? [y/n] ")
        if answer.strip().lower() != "y":
            return {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": "The user declined this action.",
                "is_error": True,
            }

    result = await session.call_tool(block.name, block.input)
    text = "\n".join(item.text for item in result.content if item.type == "text")
    return {
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": text or "(no output)",
        "is_error": result.is_error,
    }


async def main():
    # 1. Start the MCP server and connect to it
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. Ask the server which tools it has, and turn them into
            #    the same {"name", "description", "input_schema"} format as step 4
            listed = await session.list_tools()
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.input_schema,
                }
                for tool in listed.tools
            ]
            print("🔌 Connected to MCP server. Tools:", [t["name"] for t in tools])
            print("Chat with your agent. Type 'quit' to exit.\n")

            # 3. The same chat + agent loop as step 6
            messages = []
            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in {"quit", "exit"}:
                    break
                if not user_input:
                    continue
                messages.append({"role": "user", "content": user_input})

                while True:
                    response = await client.messages.create(
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
                            print(f"🔧 {block.name}({block.input})  [via MCP]")
                            tool_results.append(await run_tool(session, block))
                    messages.append({"role": "user", "content": tool_results})

                for block in response.content:
                    if block.type == "text":
                        print("🤖", block.text, "\n")


if __name__ == "__main__":
    asyncio.run(main())
