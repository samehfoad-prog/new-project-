"""
STEP 7a - Your own MCP server.

MCP (Model Context Protocol) is a standard way to package tools so that
ANY AI app can use them: your agent, Claude Desktop, Claude Code, VS Code...

This file holds the same notes tools as step 6, but as an MCP server.
Notice there is no Claude code here and no JSON descriptions: the MCP library
builds the description from each function's name, type hints and docstring.

You don't run this file yourself - step7_mcp_agent.py starts it for you.
"""
import datetime

from mcp.server.mcpserver import MCPServer

NOTES_FILE = "notes.txt"

server = MCPServer("notes")


@server.tool()
def get_current_time() -> str:
    """Returns the current local date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@server.tool()
def save_note(text: str) -> str:
    """Saves a short note for the user to a notes file."""
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Note saved."


@server.tool()
def read_notes() -> str:
    """Reads all notes the user has saved."""
    try:
        with open(NOTES_FILE, encoding="utf-8") as f:
            return f.read() or "(no notes yet)"
    except FileNotFoundError:
        return "(no notes yet)"


@server.tool()
def clear_notes() -> str:
    """Deletes ALL of the user's saved notes."""
    open(NOTES_FILE, "w").close()
    return "All notes deleted."


if __name__ == "__main__":
    # "stdio" = talk to the agent through standard input/output
    server.run(transport="stdio")
