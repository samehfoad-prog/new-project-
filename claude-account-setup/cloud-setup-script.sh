#!/bin/bash
# Claude Code cloud environment setup script.
# Installs Humanizer + Impeccable as user-level skills and the 21st MCP
# at the start of every cloud session. Paste into: environment menu -> Edit -> Setup script.
# For 21st, add API_KEY_21ST=<your key from 21st.dev/mcp> under Environment variables.

tmp=$(mktemp -d)
mkdir -p ~/.claude/skills

# Humanizer (writing)
if git clone -q --depth 1 https://github.com/blader/humanizer "$tmp/humanizer"; then
  mkdir -p ~/.claude/skills/humanizer
  cp "$tmp/humanizer/SKILL.md" ~/.claude/skills/humanizer/
fi

# Impeccable (design)
if git clone -q --depth 1 https://github.com/pbakaus/impeccable "$tmp/impeccable"; then
  rm -rf ~/.claude/skills/impeccable
  cp -r "$tmp/impeccable/plugin/skills/impeccable" ~/.claude/skills/
fi

# 21st.dev MCP (components)
if [ -n "$API_KEY_21ST" ] && command -v claude >/dev/null 2>&1; then
  claude mcp remove --scope user 21st >/dev/null 2>&1 || true
  claude mcp add --scope user --transport http 21st https://21st.dev/api/mcp \
    --header "x-api-key: $API_KEY_21ST" || true
fi

rm -rf "$tmp"
exit 0
