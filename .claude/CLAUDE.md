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
- NEVER extract secrets from `.env` in shell commands:
  - BAD: `VAR="$(grep VAR .env | cut ...)" python3 script.py`
  - GOOD: use `load_dotenv()` or `os.environ.get("KEY")` inside the application

## Output control

Show code modifications and diffs.

Prefer:
- modified code only
- unified diffs
- changed functions/classes only
- summaries for unchanged areas

Avoid:
- reprinting entire files
- repeating unchanged code
- exhaustive logs
- long generated reports

For analysis tasks:
- show top findings first
- summarize remaining items

When editing files:
- show only changed sections
- never output full files unless explicitly requested

## Command execution

When executing shell commands:

- Assume shell metacharacters trigger approval prompts — optimize commands to avoid them. Steer clear of pipes `|`, globs `*`/`?`, redirections `>`/`<`, command substitution `$()`, chaining `;`/`&&`, background `&`, and brace/glob expansion. Prefer a single tool invocation (rg, fd, a dedicated tool, or a `/tmp` script) over any pipeline.
- Prefer single-line commands whenever possible.
- Avoid multiline Bash blocks, heredocs, loops and inline scripts because they trigger confirmation prompts.
- Avoid command chaining with `;` — prefer separate commands:
  - BAD: `pkill -f "dotnet run" ; echo "killed"`
  - GOOD: `pkill -f "dotnet run"`
- Avoid multiline inline Python commands:
  - BAD: `python3 -c "import json; ..."`
  - GOOD: write `/tmp/script.py` then run `python3 /tmp/script.py`
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
- Never chain git state-changing commands (stash, checkout, reset, rebase):
  - BAD: `git stash && make check && git stash pop`
  - GOOD: run each command separately
- Avoid command substitution `$()` — prefer sequential commands:
  - BAD: `kill $(lsof -ti:8000)`
  - GOOD: `lsof -ti:8000` then `pkill -f serve.py`
- Prefer explicit interpreter paths over shell substitution:
  - BAD: `mypy src --python-executable $(uv run which python)`
  - GOOD: `mypy src --python-executable .venv/bin/python`
- Prefer one command per execution request — avoid chaining unrelated commands in a single Bash call
- Avoid `cd ... && command` — prefer passing explicit paths to commands (a stray `cd` also leaks into the persistent shell cwd and breaks later commands):
  - BAD: `cd path && rg pattern`
  - GOOD: `rg pattern path`
  - Do not combine `cd` with redirections, pipes, semicolons, or chained commands — run separate commands instead
- Prefer `uv pip install` over `pip install` for installing Python packages:
  - BAD: `pip install package`
  - GOOD: `uv pip install package`
- Avoid shell input redirection for scripts:
  - BAD: `node --input-type=module < /tmp/script.mjs`
  - GOOD: `node /tmp/script.mjs`
- Prefer foreground execution for local servers — avoid `nohup`, `>`, and background jobs (`&`)

## Python execution

Never use inline script execution. Always write to a file first.

Avoid:
- `python3 -c "..."` — even single-line
- `node -e "..."`
- heredocs (`cat <<EOF`)
- stdin piping (`echo "..." | python3`)
- shell loops (`for`, `while`)

Good:
- Write `/tmp/script.py` then run `python3 /tmp/script.py`
- Write `/tmp/script.mjs` then run `node /tmp/script.mjs`
