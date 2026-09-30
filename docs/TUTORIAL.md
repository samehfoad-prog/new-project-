# Tutorial: build an AI agent step by step

A beginner-friendly path from a single API call to an MCP-powered agent.
Each step is one runnable file in the repository root. Read the comments inside
each file as you go.

← Back to the [README](../README.md)

## What is an agent?

A chatbot answers once. An **agent** can also **use tools** (Python functions
you give it), and it keeps going until the job is done:

```
You ask → Claude thinks → "I need a tool" → your code runs it → result goes back to Claude
                        → "I'm done"      → final answer
```

Every agent has three parts:

1. **A model** – the brain (Claude)
2. **Tools** – Python functions Claude may ask you to run
3. **A loop** – keeps sending tool results back until Claude is finished

## Step 1 – Set up

1. Install Python 3.10 or newer from [python.org](https://www.python.org/).
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create an API key at [console.anthropic.com](https://console.anthropic.com) → **API Keys**.
4. Put the key in your terminal (never in your code, and never commit it):

   ```bash
   # Mac / Linux / Codespaces
   export ANTHROPIC_API_KEY="sk-ant-..."

   # Windows PowerShell
   $env:ANTHROPIC_API_KEY="sk-ant-..."
   ```

## The steps

| File | What you learn | Calls Claude? |
|---|---|---|
| [`step2_chat.py`](../step2_chat.py) | Send a message and print the reply | Yes |
| [`step3_tools.py`](../step3_tools.py) | What a tool is: a function plus a description | No |
| [`step4_agent.py`](../step4_agent.py) | **The agent loop.** Claude uses tools until it's done | Yes |
| [`step5_tool_runner.py`](../step5_tool_runner.py) | The shortcut: the SDK runs the loop for you | Yes |
| [`step6_chat_agent.py`](../step6_chat_agent.py) | A chat agent with memory that asks before acting | Yes |
| [`step7_mcp_server.py`](../step7_mcp_server.py) | Your own **MCP server** that packages the notes tools | No (started by 7b) |
| [`step7_mcp_agent.py`](../step7_mcp_agent.py) | An agent that gets its tools **from the MCP server** | Yes |
| [`step8_gmail_auth.py`](../step8_gmail_auth.py) | Log in to Google once | No |
| [`step8_gmail_agent.py`](../step8_gmail_agent.py) | An agent that **wakes up on new email** | Yes |

```bash
python step2_chat.py
python step3_tools.py
python step4_agent.py
python step5_tool_runner.py
python step6_chat_agent.py
python step7_mcp_agent.py
```

Step 8 needs a one-time Google Cloud setup first: see [GMAIL_SETUP.md](GMAIL_SETUP.md).

## How the agent loop works (`step4_agent.py`)

| # | What happens |
|---|---|
| 1 | Send the conversation and the tool list to Claude |
| 2 | Add Claude's reply to `messages`, so it remembers what it did |
| 3 | If `stop_reason` is not `"tool_use"`, Claude is done, so stop |
| 4 | Otherwise **your code** runs each tool Claude asked for |
| 5 | Send all the results back in **one** message, then go to 1 |

## Step 6: memory and approvals

`step6_chat_agent.py` keeps the `messages` list between turns, so the agent
remembers the whole conversation. Tools that change something (`save_note`)
are listed in `NEEDS_APPROVAL`: the agent asks `Allow ...? [y/n]` before running them.

**Exercise:** add a `clear_notes` tool. It needs three things: a function, an
entry in `TOOL_FUNCTIONS`, and a description in `tools`. Add it to
`NEEDS_APPROVAL` too, because deleting is risky.

## Step 7: MCP (Model Context Protocol)

In steps 4–6, the tools live **inside** the agent file. MCP moves them into a
separate program called an **MCP server**, which any AI app can connect to.
Once you've written an MCP server, your agent, Claude Desktop, Claude Code and
VS Code can all use the same tools.

```
step7_mcp_agent.py  (MCP client)             step7_mcp_server.py  (MCP server)
  1. starts the server               ─────▶   get_current_time
  2. "which tools do you have?"      ◀─────   save_note, read_notes, clear_notes
  3. sends the tool list to Claude
  4. Claude asks for save_note
  5. "please run save_note"          ─────▶   runs the function
  6. sends the result back to Claude ◀─────   "Note saved."
```

What changes compared to step 6:

- **Server:** `@server.tool()` turns a normal function into an MCP tool. The
  description comes from the docstring and type hints, so you don't write any JSON.
- **Agent:** `session.list_tools()` asks the server for its tools, and
  `session.call_tool(name, input)` asks the server to run one. The agent loop
  itself is unchanged.

Try it with `python step7_mcp_agent.py`, then ask *"Save a note: learn MCP"* and
*"What are my notes?"*. The 🔧 lines say `[via MCP]`.

**Exercise:** add a new `@server.tool()` function to `step7_mcp_server.py`
(for example `count_notes`). Restart the agent and it finds the new tool
automatically, with no changes to `step7_mcp_agent.py`.

## Step 8: react to new email

See [GMAIL_SETUP.md](GMAIL_SETUP.md).

## Common beginner mistakes

- Pasting Python code into the terminal. Python code goes **in a `.py` file**; the terminal runs commands like `python file.py`.
- Forgetting to save the file (**Ctrl + S**) before running it.
- Forgetting to append Claude's reply to `messages`. The agent then loses track of what it did.
- Sending tool results in separate messages instead of putting them all in **one** user message.
- A `tool_use_id` that doesn't match the `id` of the tool call it answers.
- Letting a tool crash the program. Return the error with `"is_error": True` instead, and Claude will try another way.
- Vague tool descriptions. Claude decides *when* to use a tool from its description.

## Ideas for what to build next

- Add your own tools: a weather API, a calculator, a database query.
- Write a stronger `system` prompt to give the agent a job and some rules.
- Add Anthropic's built-in web search tool, which runs on Anthropic's servers, so there's no function to write:

  ```python
  tools.append({"type": "web_search_20260209", "name": "web_search"})
  ```
