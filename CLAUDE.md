# CLAUDE.md

Stable rules for this project. Changing history (what was tried, what broke,
what was decided) is kept by claude-mem, so don't copy it here.

## Project
- What it is: _one or two sentences_
- Stack: _language, framework, database_

## Commands
- Install: `_fill in_`
- Run: `_fill in_`
- Test: `_fill in_`
- Lint/format: `_fill in_`

## Conventions
- Keep changes small and focused; run the tests before committing.
- When making a design decision, state the choice and the reason in one
  sentence so claude-mem records it as a decision.
- Never print or commit secrets; wrap any sensitive text in `<private>` tags.

## Research
- For anything that may have changed recently (prices, releases, companies,
  job postings), use Perplexity instead of answering from memory, and cite the
  sources it returns.
- Pick the lightest tool: `perplexity_search` for links, `perplexity_ask` for a
  quick answer, `perplexity_reason` for comparisons, `perplexity_research` only
  for deep dives (slow and costs more).

## Token habits
- Prefer targeted searches (grep/glob) over reading whole directories.
- Before re-investigating something, search memory first
  ("search memory for ...").
