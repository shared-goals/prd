# Shared Goals PRD Agent Instructions

This repository is the source of truth for Shared Goals MVP product decisions, acceptance criteria, backlog, history, and research.

## Development Principles

- Follow KISS, DRY, and YAGNI.
- Update PRD/acceptance docs before implementation decisions.
- Keep repository files and git history authoritative; memory is only a recall layer.

## Hindsight Memory Workflow

For Shared Goals development tasks, use Hindsight memory when it is configured and available.

For MCP-enabled Copilot sessions, the Hindsight tools are `recall`, `retain`, and `reflect`. Use `recall` before acting and `retain` only for accepted decisions or status changes.

Before acting:
- Recall project memory with tags `project:sg` and `scope:dev`.
- Verify recalled facts against repository files before changing anything.

After accepted decisions or status changes:
- Retain one concise durable memory with tags `project:sg` and `scope:dev`.
- Put kind, phase, status, source file, commit hash, PR link, and rationale in memory content or context, not tags.

Never retain:
- secrets or credentials
- raw private notes
- routine logs or telemetry
- noisy terminal output

When memory conflicts with this repository, the repository wins. Correct memory only after verifying the repository state.