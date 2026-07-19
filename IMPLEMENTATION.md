# Shared Goals - MVP Implementation Contract

This document translates `ACCEPTANCE.md` into the first implementation-facing contract for `shared-goals/instance`. It is not a second PRD. If this file and `README.md` or `ACCEPTANCE.md` disagree, update the PRD/acceptance source first.

## Scope

Build the smallest FastAPI + SQLite backend that allows agents equipped with the `shared-goals` skill to:
- find or create a goal
- join a goal through a personal time contract
- list the user's active joined goals/contracts for `Compass.md`
- log a commit against that contract
- request current-step advice or instructions
- read anonymous goal aggregates

Do not implement messenger-specific flows, proactive Goal Discovery, leaderboards, streaks, default reminders, competitive public goals, or a transactional standalone consumer UI in the MVP backend.

`Compass.md` parsing belongs in the local agent/skill layer, not in the backend. MVP parser contract:
- the filename is the caption; no top-level `# Compass` heading is required
- `## Next steps` is the single editable checklist where each task lives once
- `#sg-*` tags are the primary locator and normalize to platform `goal_id` values without the `#` prefix
- `## Goal IDs` and `## Notes` are reference sections, not task source sections
- generated views may group tasks by joined goal or by the four psychologies, but those views are derived from the DRY source

## Test Strategy

Implementation starts with backend acceptance tests. Unit tests can exist underneath, but the first green slice must prove agent-facing behavior through HTTP-level API tests.

Recommended first test files in `shared-goals/instance`:
- `tests/acceptance/test_agent_goal_flow.py`
- `tests/acceptance/test_contract_commit_flow.py`
- `tests/acceptance/test_compass_planning_flow.py`
- `tests/acceptance/test_advice_and_partner_flow.py`
- `tests/acceptance/test_anonymous_aggregates.py`

Use SQLite in a temporary database for tests. Use concrete fixture values from `ACCEPTANCE.md`, including `partner_goal_type = "computer_club"` until the real MVP partner is finalized.

## Acceptance Traceability

| Acceptance ID | Backend acceptance test intent | Minimal API surface | Out-of-scope guard |
|---|---|---|---|
| SG-MVP-001 | Agent can use `Compass.md` tags to resolve joined goals/contracts and sync normalized planning context without storing private source text | `GET /api/v1/contracts`, `GET /api/v1/contracts/{contract_id}/advice`, `POST /api/v1/contracts/{contract_id}/commits` | No raw Markdown workspace import in MVP backend |
| SG-MVP-002 | Agent can create a non-competitive goal with optional human-readable `goal_id` and receive a machine-readable response | `POST /api/v1/goals` | No proactive deduplication or hierarchy |
| SG-MVP-003 | Agent can join a public goal through a personal contract and reduce time later | `POST /api/v1/goals/{goal_id}/contracts`, `PATCH /api/v1/contracts/{contract_id}` | No reminders, streaks, ranking, or channel-specific identity |
| SG-MVP-004 | Agent can propose a commit from a completed Compass item and, after user approval, log progress with time, done text, optional next step, skill tag, and happy moment flag | `POST /api/v1/contracts/{contract_id}/commits` | Public views remain anonymous by default; no unapproved CUD |
| SG-MVP-005 | Agent can request advice for an active contract and receive recommendation-style `next_step` ideas suitable for Compass insertion | `GET /api/v1/contracts/{contract_id}/advice` | Advice is not obligation or pressure; no unapproved CUD |
| SG-MVP-006 | Partner-driven goal can route guidance through a partner instruction provider stub | `GET /api/v1/contracts/{contract_id}/advice` | No full partner methodology or paid-service workflow required |
| SG-MVP-007 | Backend can return anonymous Social Capital, active participants, happy moments, and activity freshness | `GET /api/v1/goals/{goal_id}/summary` | No personal rankings or named comparisons |

## Minimal Agent API

All MVP endpoints are JSON REST endpoints under `/api/v1`. Responses must be usable by an agent without scraping HTML.

Authentication model:
- `agent_key_id` identifies an API key or credential scoped to `user_id`
- `user_id` is the platform participant
- agent keys authenticate access but never become participants
- MVP tests may use a fixed test key resolved to a fixture `user_id`

Common response rules:
- return stable IDs for created resources
- return validation errors as structured JSON
- include enough state for the agent to decide the next action
- never expose private source text in public aggregate responses
- create, update, and delete requests include `user_approved: true` in MVP acceptance tests; the flag represents explicit user approval collected by the agent

### Goals

`GET /api/v1/goals?query=<text>`

Returns a simple catalog search over public goals. MVP search can be title/description substring matching.

`POST /api/v1/goals`

Request fields:
- `goal_id: str | null` (optional stable human-readable ID, normalized without Markdown `#` prefix)
- `title: str`
- `description: str`
- `visibility: public | invite | personal`
- `instance_id: str = "default"`
- `user_approved: bool`

Response fields:
- `goal_id`
- `title`
- `description`
- `visibility`
- `instance_id`
- `moderation_status`
- `created_at`

Public goals must pass the four humanistic criteria from `README.md`. For MVP tests, this can be a deterministic moderation function or stub with explicit pass/fail cases.

Human-readable goal IDs such as `sg-music` or `sg-oss-coding` are allowed for trusted MVP agent-created goals. In `Compass.md`, the corresponding Markdown tags are written as `#sg-music` or `#sg-oss-coding`.

### Contracts

`POST /api/v1/goals/{goal_id}/contracts`

Request fields:
- `cadence: daily | weekly | monthly | occasionally`
- `time_minutes: int | null`
- `user_approved: bool`

Response fields:
- `contract_id`
- `goal_id`
- `user_id`
- `cadence`
- `time_minutes`
- `is_active`
- `created_at`

`PATCH /api/v1/contracts/{contract_id}`

Supports:
- reducing `time_minutes`
- setting `is_active = false` to pause or exit
- `user_approved: bool`

Reducing time mid-period must not invalidate later execution.

`GET /api/v1/contracts`

Returns the authenticated user's active joined goals/contracts for agent planning and `Compass.md` synchronization.

Response fields:
- `contracts: list`
- each item includes `contract_id`, `goal_id`, `goal_tag`, `goal_title`, `cadence`, `time_minutes`, `is_active`, `latest_next_step`

### Commits

`POST /api/v1/contracts/{contract_id}/commits`

Request fields:
- `time_minutes: int | null`
- `done: str | null`
- `next_step: str | null`
- `skill_tag: will | mind | feeling | faith | null`
- `is_happy_moment: bool = false`
- `is_public: bool = false`
- `user_approved: bool`
- `source_ref: str | null` (optional private agent reference, e.g. `Compass.md` item identity; not exposed in public aggregates)

If `done` is omitted and the previous commit has `next_step`, the backend may use that previous `next_step` as `done`.

Response fields:
- `commit_id`
- `contract_id`
- `time_minutes`
- `done`
- `next_step`
- `skill_tag`
- `is_happy_moment`
- `is_public`
- `created_at`

### Advice

`GET /api/v1/contracts/{contract_id}/advice`

Returns current-step instructions for the active contract.

Response fields:
- `contract_id`
- `goal_id`
- `partner_id: str | null`
- `advice_text`
- `recommended_next_steps: list`
- `source: platform | partner_stub | partner_service`
- `subscription_required: bool = false`

MVP can start with a partner stub for the chosen fixture category. The response must be framed as recommendation, not pressure. Recommended next steps should be suitable for agent insertion into `Compass.md` after user approval. When enough data exists, ordering can prefer ideas that historically lead to more happy-moment commits.

### Anonymous Summary

`GET /api/v1/goals/{goal_id}/summary`

Response fields:
- `goal_id`
- `social_capital_minutes`
- `active_participants_count`
- `happy_moment_count`
- `activity_freshness_text`

The summary must not include participant names, rankings, or user-level comparisons.

## First Backend Slice

1. Create data models for `Goal`, `Contract`, `Commit`, and `Instruction` with SQLite persistence.
2. Add HTTP acceptance tests for creating/finding goals, joining contracts, logging commits, requesting advice, and reading anonymous summaries.
3. Implement only the route behavior required to make those tests pass.
4. Add a deterministic partner instruction stub for the first fixture category.
5. Keep web UI read-only for MVP statistics until an acceptance scenario changes that scope.

## Change Control

Before adding backend behavior:
- map it to an `ACCEPTANCE.md` scenario
- update `ACCEPTANCE.md` first if no scenario covers it
- update this document only after the behavior belongs in MVP
- retain accepted status changes into Hindsight with tags `project:sg` and `scope:dev`