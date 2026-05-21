## Language

Respond in French by default, unless the project's CLAUDE.md specifies otherwise.
Code, comments, and commit messages follow the conventions of each project.

## Plan before implementation

Always propose a minimal plan and wait for explicit user approval before writing any code.

Applies without exception when a task involves:
- creating or modifying multiple files
- an architectural choice (new component, new API route, new DB schema…)
- a refactor or redesign
- a feature whose exact scope is not fully specified

Plan format (a few lines):
1. **What will be created / modified** — list of affected files
2. **The chosen approach** — one sentence per point
3. **What is out of scope** — what the task will NOT do

No plan required for: single-file bug fix, isolated unit test, config value change, lint/typing fix with no logic change.

When scope is ambiguous, ask one targeted question before proposing a plan.

## Git conventions

- **Atomic commits**: one commit = one logical intent; the project must be in a consistent state after each commit
- **Conventional format**: `feat:`, `fix:`, `refactor:`, `test:`, `ci:`, `chore:`
- **Never push spontaneously** — only push when explicitly asked

## Quality baseline

After generating or modifying code:
- Run the project's lint + type check command (usually `make check`)
- Run the project's test suite (usually `make test`)

## Security baseline

- NEVER log passwords, tokens, API keys, or PII — log IDs and correlation IDs only
- NEVER hardcode secrets — always read from environment/config
- Validate and sanitise input at system boundaries only (HTTP handler, CLI entrypoint)

## Command execution

When executing shell commands:

- Prefer single-line commands whenever possible.
- Avoid multiline Bash blocks, heredocs, loops and inline scripts because they trigger confirmation prompts.
- Prefer creating temporary scripts then executing them:
  - Python: write `/tmp/script.py` then run `python3 /tmp/script.py`
  - Shell: write `/tmp/script.sh` then execute it
- Prefer language scripts over complex shell pipelines.
- Avoid `for`, `while`, `cat <<EOF`, inline Python blocks and long chained commands.
- Keep commands approval-friendly.
- Prefer rg / fd instead of find + xargs pipelines
- Prefer simple commands over shell pipelines
- Avoid xargs when possible
- Prefer Python for data extraction/transformation
- Prefer git commands individually instead of chained commands
