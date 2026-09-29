# new-project-

Learn to build an AI agent in Python, step by step, with Claude and the
[Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python).

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
2. Install the SDK:

   ```bash
   pip install -r requirements.txt
   ```

3. Create an API key at [console.anthropic.com](https://console.anthropic.com) → **API Keys**.
4. Put the key in your terminal (never in your code, and never commit it):

   ```bash
   # Mac / Linux
   export ANTHROPIC_API_KEY="sk-ant-..."

   # Windows PowerShell
   $env:ANTHROPIC_API_KEY="sk-ant-..."
   ```

## The steps

Run each file in order, and read the comments inside it as you go.

| File | What you learn | Calls Claude? |
|---|---|---|
| [`step2_chat.py`](step2_chat.py) | Send a message and print the reply | Yes |
| [`step3_tools.py`](step3_tools.py) | What a tool is: a function plus a description | No |
| [`step4_agent.py`](step4_agent.py) | **The agent loop.** Claude uses tools until it's done | Yes |
| [`step5_tool_runner.py`](step5_tool_runner.py) | The shortcut: the SDK runs the loop for you | Yes |
| [`step6_chat_agent.py`](step6_chat_agent.py) | A chat agent with memory that asks before acting | Yes |
| [`step7_mcp_server.py`](step7_mcp_server.py) | Your own **MCP server** that packages the notes tools | No (started by 7b) |
| [`step7_mcp_agent.py`](step7_mcp_agent.py) | An agent that gets its tools **from the MCP server** | Yes |

```bash
python step2_chat.py
python step3_tools.py
python step4_agent.py
python step5_tool_runner.py
python step6_chat_agent.py
python step7_mcp_agent.py
```

## How the agent loop works (`step4_agent.py`)

| # | What happens |
|---|---|
| 1 | Send the conversation and the tool list to Claude |
| 2 | Add Claude's reply to `messages`, so it remembers what it did |
| 3 | If `stop_reason` is not `"tool_use"`, Claude is done, so stop |
| 4 | Otherwise **your code** runs each tool Claude asked for |
| 5 | Send all the results back in **one** message, then go to 1 |

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
(for example `count_notes`). Restart the agent and it will find the new tool
automatically, with no changes to `step7_mcp_agent.py`.

## Common beginner mistakes

- Forgetting to append Claude's reply to `messages`. The agent then loses track of what it did.
- Sending tool results in separate messages instead of putting them all in **one** user message.
- A `tool_use_id` that doesn't match the `id` of the tool call it answers.
- Letting a tool crash the program. Return the error with `"is_error": True` instead, and Claude will try another way.
- Vague tool descriptions. Claude decides *when* to use a tool from its description.

## Ideas for what to build next

- Add your own tools: a weather API, a calculator, sending an email, a database query.
- Write a stronger `system` prompt to give the agent a job and some rules.
- Add Anthropic's built-in web search tool, which runs on Anthropic's servers, so there's no function to write:

  ```python
  tools.append({"type": "web_search_20260209", "name": "web_search"})
  ```
