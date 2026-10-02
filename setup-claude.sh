#!/usr/bin/env bash
# Sets up Claude Code with claude-mem (persistent memory), Headroom
# (context compression) and task-observer (self-improving skills).
# Run this on your own machine, not in a cloud session.
#
#   ./setup-claude.sh            # install everything
#   ./setup-claude.sh --check    # only report what is installed
set -euo pipefail

CHECK_ONLY=false
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=true

info() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m ok\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m !!\033[0m %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

# --- prerequisites ----------------------------------------------------------
info "Checking prerequisites"
if have node; then
  node_major=$(node -p 'process.versions.node.split(".")[0]')
  if (( node_major >= 20 )); then ok "node $(node -v)"; else warn "node $(node -v) found, claude-mem needs 20+"; fi
else
  warn "node not found (needed for Claude Code and claude-mem): https://nodejs.org"
fi
have python3 && ok "python3 $(python3 -c 'import sys;print(".".join(map(str,sys.version_info[:2])))')" \
  || warn "python3 not found (Headroom needs 3.10+)"
have uv && ok "uv" || warn "uv not found; will fall back to pip for Headroom"

if $CHECK_ONLY; then
  have claude   && ok "claude $(claude --version 2>/dev/null || true)" || warn "claude not installed"
  have headroom && ok "headroom installed" || warn "headroom not installed"
  [[ -d "$HOME/.claude-mem" ]] && ok "claude-mem data dir exists" || warn "claude-mem not set up"
  [[ -f "$HOME/.claude/skills/task-observer/SKILL.md" ]] && ok "task-observer installed" || warn "task-observer not installed"
  exit 0
fi

# --- Claude Code ------------------------------------------------------------
if have claude; then
  ok "Claude Code already installed"
else
  info "Installing Claude Code"
  npm install -g @anthropic-ai/claude-code
fi

# --- claude-mem -------------------------------------------------------------
info "Installing claude-mem"
npx --yes claude-mem install

# --- Headroom ---------------------------------------------------------------
info "Installing Headroom"
if have uv; then
  uv tool install --python 3.13 "headroom-ai[all]"
else
  python3 -m pip install --user "headroom-ai[all]"
fi
headroom doctor || warn "headroom doctor reported problems; see output above"

# --- task-observer ----------------------------------------------------------
# Watches sessions for corrections and repeated workflows and proposes skill
# improvements. Installed globally; its log lives outside the skills folder.
OBSERVER_DIR="$HOME/.claude/skills/task-observer"
OBSERVER_WORKSPACE="${OBSERVER_WORKSPACE:-$HOME/.claude-observer}"
PROJECTS_ROOT="${PROJECTS_ROOT:-$HOME}"
info "Installing task-observer skill"
if [[ -d "$OBSERVER_DIR/.git" ]]; then
  git -C "$OBSERVER_DIR" pull -q --ff-only
else
  mkdir -p "$(dirname "$OBSERVER_DIR")"
  git clone -q --depth 1 https://github.com/rebelytics/one-skill-to-rule-them-all "$OBSERVER_DIR"
fi
mkdir -p "$OBSERVER_WORKSPACE/skill-observations/observation-log" "$OBSERVER_WORKSPACE/skill-updates"

# The skill only runs reliably when CLAUDE.md tells it to, so copy the
# activation block from its docs into the global CLAUDE.md with paths filled in.
global_md="$HOME/.claude/CLAUDE.md"
obs_begin="<!-- >>> task-observer >>> -->"
obs_end="<!-- <<< task-observer <<< -->"
if grep -qF "$obs_begin" "$global_md" 2>/dev/null; then
  ok "task-observer already activated in $global_md"
else
  info "Activating task-observer in $global_md"
  block=$(awk '/^### The activation block/{f=1} f&&/^```text/{p=1;next} p&&/^```/{exit} p' \
    "$OBSERVER_DIR/references/environments.md")
  if [[ -z "$block" ]]; then
    warn "Couldn't find the activation block; add it by hand from $OBSERVER_DIR/references/environments.md"
  else
    block=${block//"[ABSOLUTE PATH]"/$OBSERVER_WORKSPACE}
    block=${block//"[PROJECTS ROOT]"/$PROJECTS_ROOT}
    block=${block//"<skill directory>"/$OBSERVER_DIR}
    printf '\n%s\n%s\n%s\n' "$obs_begin" "$block" "$obs_end" >> "$global_md"
  fi
fi

# --- shell alias ------------------------------------------------------------
# `cc` starts Claude Code through the Headroom proxy. Headroom's own memory is
# left off so claude-mem stays the single memory system.
shell_rc="$HOME/.bashrc"
[[ "${SHELL:-}" == */zsh ]] && shell_rc="$HOME/.zshrc"
marker="# >>> claude setup >>>"
if ! grep -qF "$marker" "$shell_rc" 2>/dev/null; then
  info "Adding the 'cc' alias to $shell_rc"
  cat >> "$shell_rc" <<'RC'
# >>> claude setup >>>
export HEADROOM_BEACON=off            # no Headroom telemetry
alias cc='headroom wrap claude'       # Claude Code + compression
alias cc1m='headroom wrap claude --1m' # same, keeping the 1M context model
# <<< claude setup <<<
RC
else
  ok "'cc' alias already present in $shell_rc"
fi

info "Done. Open a new terminal and run: cc"
echo "    Memory viewer: see the URL printed by claude-mem above"
echo "    Savings:       headroom dashboard"
echo "    Observations:  $OBSERVER_WORKSPACE/skill-observations/observation-log/"
