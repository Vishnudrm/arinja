# Copilot Instructions for `arinja`

This project is a terminal-first, AI-powered news bot for global and Indian news, with PostgreSQL storage, semantic search, bookmarking, PDF export, and chat—all from the terminal.

## Key Structure
- Main CLI code: `arinja/`
- Config and secrets: `config/` (see `config.example.env`)
- Tests: `tests/`
- Scripts/utilities: `scripts/`
- Project metadata: `pyproject.toml`

## Core Conventions
- Use Typer for CLI commands and subcommands (see `arinja/` for entrypoints).
- Use PostgreSQL for all persistent storage (no SQLite).
- Store API keys and DB credentials in `.env` (never commit real secrets).
- Output must use matrix-style (green/black) via `rich`.
- All fetches and updates deduplicate news by title+source+date.
- Bookmarks, highlights, and notes are stored per user, with tags and optional star rating.
- PDF exports are minimalist, text-only, and for personal use only.
- All AI summarization and chat must use OpenAI/Anthropic, and only send article text when user requests details.
- Support both CLI and TUI (`arinja tui`).
- Default timezone is IST; allow override via config or CLI flag.

## Developer Workflows
- Install dependencies with Poetry: `poetry install`
- Run CLI: `poetry run arinja <command>`
- Set up DB: use `POSTGRES_URI` from `.env` (see `config.example.env`)
- Add a cron job for daily fetch: `0 10 * * * poetry run arinja fetch`
- Run tests: `poetry run pytest`

## Examples
- `arinja fetch` — fetches and indexes news
- `arinja today --category technology --limit 20`
- `arinja search --query "quantum dot" --from 2025-10-01 --to 2025-10-19`
- `arinja open <id>`
- `arinja star <id> --tags "ai,policy" --note "solid analysis"`
- `arinja export pdf --stars --from 2025-10-01 --to 2025-10-19 --outfile ~/news.pdf`
- `arinja chat`

## Patterns
- Use dependency injection for DB and config.
- Use FTS and embeddings for search.
- All user-facing errors must be styled with `rich` and be actionable.
- Never expose API keys or secrets in logs or errors.

See `README.md` and `config.example.env` for more details.