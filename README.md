# new-project-

## Claude Code setup

This repo ships a Claude Code setup with:

- **claude-mem**: persistent memory across sessions.
- **Headroom**: compresses tool output, logs and JSON before it reaches the model.
- **CLAUDE.md**: stable project rules Claude always reads.
- **.claude/settings.json**: auto-allows read-only git commands and blocks reading `.env` files.

On your own machine (Node 20+, Python 3.10+):

```bash
./setup-claude.sh           # install Claude Code, claude-mem, Headroom; add the `cc` alias
./setup-claude.sh --check   # report what's installed
```

Then open a new terminal and start Claude Code with `cc` (or `cc1m` to keep the
1M-context model). Check savings with `headroom dashboard`.
