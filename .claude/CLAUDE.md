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

Show only what changed: unified diffs, modified functions/classes, summaries for unchanged areas. Never reprint entire files (unless explicitly requested), unchanged code, or exhaustive logs. For analysis tasks, show top findings first and summarize the rest.

## Command execution

Optimize commands to avoid approval prompts — shell metacharacters trigger them.

- **No metacharacters**: avoid pipes `|`, redirections `>`/`<`, command substitution `$()`, chaining `;`/`&&`, background `&`, globs, and brace expansion. Prefer a single tool invocation (rg, fd, a dedicated tool) over a pipeline.
- **One command per call**: never chain unrelated commands, and never chain git state-changing commands (stash, checkout, reset, rebase) — run each separately.
- **No `cd ... && cmd`**: pass explicit paths instead (`rg pattern path`, not `cd path && rg pattern`). A stray `cd` leaks into the persistent shell cwd.
- **No inline scripts**: never `python3 -c`, `node -e`, heredocs (`cat <<EOF`), stdin piping (`echo ... | python3`), or shell loops (`for`/`while`). Write `/tmp/script.py` (or `/tmp/script.mjs`) and run it.
- **Explicit interpreters/installers**: prefer `.venv/bin/python` over `$(uv run which python)`; prefer `uv pip install` over `pip install`.
- **Local servers**: run in the foreground — no `nohup`, `&`, or output redirection.
- **Dependency inspection**: never use `cd`, pipes, `grep`, `sort`, or other shell filtering to inspect dependencies. Read the manifests directly (`requirements.txt`, `pyproject.toml`, `uv.lock`, `package.json`, lock files). If a command is genuinely required, run one at a time.
- **Single-line commands**: never split a shell command across multiple lines — every command must be a single line.
- **Never pass `-r` to ripgrep**: in `rg`, `-r` is `--replace`, NOT recursive (rg is recursive by default). `rg -rln "x" path` parses as `--replace=ln` and rewrites matches in the output. Use `rg -n`/`rg -l`/`rg -ln`. If rg output seems to swap the search term for a stray word, suspect this flag first, not the harness.
