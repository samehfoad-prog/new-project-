# new-project-

## Claude Code setup

This repo ships a Claude Code setup with:

- **claude-mem**: persistent memory across sessions.
- **Headroom**: compresses tool output, logs and JSON before it reaches the model.
- **task-observer**: watches your sessions for corrections and repeated workflows, and proposes skill improvements for you to review. Its log is in `~/.claude-observer/`.
- **CLAUDE.md**: stable project rules Claude always reads.
- **.claude/settings.json**: auto-allows read-only git commands and blocks reading `.env` files.

On your own machine (Node 20+, Python 3.10+):

```bash
./setup-claude.sh           # install Claude Code, claude-mem, Headroom, task-observer; add the `cc` alias
./setup-claude.sh --check   # report what's installed
```

Then open a new terminal and start Claude Code with `cc` (or `cc1m` to keep the
1M-context model). Check savings with `headroom dashboard`.

task-observer is installed in `~/.claude/skills/task-observer`. It's turned on
by a block added to `~/.claude/CLAUDE.md` (between the `task-observer` markers;
delete that block to turn it off). Set `OBSERVER_WORKSPACE` or `PROJECTS_ROOT`
before running the script to use different folders. Check it works in a *new*
session: ask "Any observations logged?" after a task.
