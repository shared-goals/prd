# Shared Goals - MVP Implementation Contract

This document translates `ACCEPTANCE.md` into the first implementation-facing contract for `shared-goals/instance`. It is not a second PRD. If this file and `README.md` or `ACCEPTANCE.md` disagree, update the PRD/acceptance source first.

## Scope

Build the smallest FastAPI + SQLite backend that allows agents equipped with the `shared-goals` skill to:
- find or create a goal
- join a goal through a personal time contract
- log a commit against that contract
- request current-step advice or instructions
- read anonymous goal aggregates

Do not implement messenger-specific flows, proactive Goal Discovery, leaderboards, streaks, default reminders, competitive public goals, or a transactional standalone consumer UI in the MVP backend.

## Test Strategy

Implementation starts with backend acceptance tests. Unit tests can exist underneath, but the first green slice must prove agent-facing behavior through HTTP-level API tests.

Recommended first test files in `shared-goals/instance`:
- `tests/acceptance/test_agent_goal_flow.py`
- `tests/acceptance/test_contract_commit_flow.py`
- `tests/acceptance/test_advice_and_partner_flow.py`
- `tests/acceptance/test_anonymous_aggregates.py`

Use SQLite in a temporary database for tests. Use concrete fixture values from `ACCEPTANCE.md`, including `partner_goal_type = "computer_club"` until the real MVP partner is finalized.

## Acceptance Traceability

| Acceptance ID | Backend acceptance test intent | Minimal API surface | Out-of-scope guard |
|---|---|---|---|
| SG-MVP-001 | Agent can submit normalized goal/contract context derived from text without storing private source text in public data | `POST /api/v1/goals`, `POST /api/v1/goals/{goal_id}/contracts` | No raw Markdown workspace import in MVP backend |
| SG-MVP-002 | Agent can create a non-competitive goal and receive a machine-readable response | `POST /api/v1/goals` | No proactive deduplication or hierarchy |
| SG-MVP-003 | Agent can join a public goal through a personal contract and reduce time later | `POST /api/v1/goals/{goal_id}/contracts`, `PATCH /api/v1/contracts/{contract_id}` | No reminders, streaks, ranking, or channel-specific identity |
| SG-MVP-004 | Agent can log progress with time, done text, optional next step, skill tag, and happy moment flag | `POST /api/v1/contracts/{contract_id}/commits` | Public views remain anonymous by default |
| SG-MVP-005 | Agent can request advice for an active contract and receive recommendation-style guidance | `GET /api/v1/contracts/{contract_id}/advice` | Advice is not obligation or pressure |
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

### Goals

`GET /api/v1/goals?query=<text>`

Returns a simple catalog search over public goals. MVP search can be title/description substring matching.

`POST /api/v1/goals`

Request fields:
- `title: str`
- `description: str`
- `visibility: public | invite | personal`
- `instance_id: str = "default"`

Response fields:
- `goal_id`
- `title`
- `description`
- `visibility`
- `instance_id`
- `moderation_status`
- `created_at`

Public goals must pass the four humanistic criteria from `README.md`. For MVP tests, this can be a deterministic moderation function or stub with explicit pass/fail cases.

### Contracts

`POST /api/v1/goals/{goal_id}/contracts`

Request fields:
- `cadence: daily | weekly | monthly | occasionally`
- `time_minutes: int | null`

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

Reducing time mid-period must not invalidate later execution.

### Commits

`POST /api/v1/contracts/{contract_id}/commits`

Request fields:
- `time_minutes: int | null`
- `done: str | null`
- `next_step: str | null`
- `skill_tag: will | mind | feeling | faith | null`
- `is_happy_moment: bool = false`
- `is_public: bool = false`

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
- `source: platform | partner_stub | partner_service`
- `subscription_required: bool = false`

MVP can start with a partner stub for the chosen fixture category. The response must be framed as recommendation, not pressure.

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