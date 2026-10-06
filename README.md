# new-project-

## Claude Code setup

This repo ships a Claude Code setup with:

- **claude-mem**: persistent memory across sessions.
- **Headroom**: compresses tool output, logs and JSON before it reaches the model.
- **task-observer**: watches your sessions for corrections and repeated workflows, and proposes skill improvements for you to review. Its log is in `~/.claude-observer/`.
- **Humanizer**: rewrites AI-sounding text so it reads naturally. Run `/humanizer` and paste text, or name a file.
- **Impeccable**: design commands for front-end work. Run `/impeccable init` once per project, then `audit`, `critique` and `polish`.
- **21st**: gives Claude a library of 10,000+ React/Tailwind UI components. Needs a free API key from [21st.dev/mcp](https://21st.dev/mcp); the script asks for it and saves it to `~/.config/claude-setup/21st.env`, readable only by you.
- **Perplexity**: live, cited web search and deep research inside Claude Code. Needs an API key from [console.perplexity.ai](https://console.perplexity.ai) (paid per use); the script saves it to `~/.config/claude-setup/perplexity.env`, readable only by you.
- **CLAUDE.md**: stable project rules Claude always reads.
- **.claude/settings.json**: auto-allows read-only git commands and blocks reading `.env` files.

On your own machine (Node 20+, Python 3.10+):

```bash
./setup-claude.sh           # install Claude Code, claude-mem, Headroom, task-observer and the plugins; add the `cc` alias
./setup-claude.sh --check   # report what's installed
```

Then open a new terminal and start Claude Code with `cc` (or `cc1m` to keep the
1M-context model). Check savings with `headroom dashboard`.

task-observer is installed in `~/.claude/skills/task-observer`. It's turned on
by a block added to `~/.claude/CLAUDE.md` (between the `task-observer` markers;
delete that block to turn it off). Set `OBSERVER_WORKSPACE` or `PROJECTS_ROOT`
before running the script to use different folders. Check it works in a *new*
session: ask "Any observations logged?" after a task.
