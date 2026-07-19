# Shared Goals - MVP Acceptance Specification

This document is the TDD-first acceptance layer for the Shared Goals MVP. It turns the PRD plan into testable use cases before platform implementation starts.

## Scope

These scenarios cover the MVP only:
- humans interact through agents equipped with the `shared-goals` skill
- agents create or join goals, create contracts, log commits, and request advice
- agents may use `Compass.md` as a DRY human-readable planning base indexed by `#sg-*` tags
- psychology views (`faith`, `will`, `feeling`, `mind`) are generated from Compass tasks, goals, commits, and advice instead of hand-maintained as source sections
- partner-driven goals can return specialized instructions and subscription-backed advice

Out of scope for MVP acceptance:
- messenger-specific integrations
- proactive Goal Discovery and deduplication
- standalone consumer UI as the primary interaction surface
- backend parsing of private Markdown files as a storage/import feature

Permanent platform anti-goals:
- leaderboards and personal rankings
- streak mechanics
- default reminders or pressure mechanics
- competitive public goals

## Test Data Baseline

Use one concrete MVP partner goal type when running acceptance tests. Until the partner is finalized, use a named fixture such as `partner_goal_type = "computer_club"` or `partner_goal_type = "water_activity"`; the behavior must be concrete even if the real partner name changes.

Minimum domain fixtures:
- `user_id`: platform participant; internal UUID, no channel identifier
- `goal_id`: shared goal visible in the MVP instance; may be human-readable, such as `sg-music` or `sg-oss-coding`
- `contract_id`: active personal time contract for the user and goal
- `commit_id`: logged progress item against the contract
- `partner_id`: instruction provider for the partner-driven goal
- `compass_file_name`: `Compass.md`
- `compass_next_steps_heading`: `## Next steps`
- `compass_goal_ids_heading`: `## Goal IDs`
- `markdown_goal_tag`: human-readable Markdown tag such as `#sg-music`; normalized to `goal_id = "sg-music"`

Authentication fixture when needed:
- `agent_key_id`: API key or credential assigned to an agent and scoped to `user_id`; it identifies access, not a platform participant. One user may have many keys for different agents.

Development memory fixtures when needed:
- `memory_bank_id`: Hindsight-compatible bank or tagged scope used for Shared Goals development memory
- `memory_tags`: canonical tags from the taxonomy below

## Shared Development Memory Tags

All Shared Goals development memories must use a tiny controlled tag set. Tags are for recall filtering only; kind, phase, status, source links, commit hashes, and rationale belong in the retained content or context.

Required on every retained Shared Goals development memory:
- `project:sg`
- `scope:dev`

Tag rules:
- use lowercase kebab-case only
- start recall with `project:sg` + `scope:dev`
- put kind, phase, status, source file, commit hash, PR link, and rationale in memory content/context, not tags
- do not create tags from private names, secrets, credentials, raw note titles, or temporary terminal/session ids
- prefer updating the same durable memory document when a decision changes instead of adding near-duplicates

## Product Acceptance Scenarios

### SG-MVP-001 - Compass Planning-base Flow

**Given** a user works with an agent using `Compass.md` as a Markdown planning base
**And** the file uses its filename as caption, with no required top-level `# Compass` heading
**And** each task lives once in a `## Next steps` checklist
**And** the planning base contains human-readable Shared Goals tags such as `#sg-music` or `#sg-oss-coding`
**When** the user asks the agent to connect current planning context to Shared Goals
**Then** the agent can resolve the tags to joined goals/contracts without requiring a separate manual UI
**And** Compass items can represent `next_step` recommendations from joined Shared Goals
**And** the platform can return an agent-facing `next_step` feed for active joined contracts
**And** generated views can group the same items by goal or by psychology without duplicating source tasks
**And** the platform stores only the normalized goal/contract/commit data needed for the MVP
**And** private source text remains outside public aggregates by default
**And** create, update, and delete operations are proposed to the user before the agent calls the platform

### SG-MVP-002 - Create Goal Through Agent

**Given** the user expresses a concrete non-competitive goal through an agent
**When** the agent calls the platform to create the goal
**Then** the platform creates a goal with title, description, visibility, and `instance_id`
**And** trusted agent-created MVP goals may use a human-readable `goal_id`, such as `sg-oss-coding`
**And** public goals pass the four humanistic criteria check
**And** the response is usable by the agent without human UI steps

### SG-MVP-003 - Join Goal Through Contract

**Given** an existing public goal is available through simple catalog lookup or direct link
**When** the agent helps the user join it with cadence and optional time commitment
**Then** the platform creates an active contract for `user_id` and `goal_id`
**And** the contract can be reduced mid-period without invalidating execution
**And** platform anti-goals are preserved: no default reminder, streak, leaderboard, or ranking is created

### SG-MVP-004 - Log Commit Autonomously

**Given** the user has an active contract
**And** `Compass.md` contains a completed item tagged to the contract's joined goal
**When** the agent proposes a commit and the user approves it
**Then** the platform records `time_minutes`, `done`, optional `next_step`, `skill_tag`, and `is_happy_moment`
**And** `done` can be derived from a previous `next_step` when appropriate
**And** the commit is anonymous by default in public views

### SG-MVP-005 - Request Advice Or Instructions

**Given** the user has an active contract for a goal with instructions
**When** the agent asks the platform for the next useful recommendation
**Then** the platform returns current-moment advice, instructions, or recommended `next_step` items for that goal
**And** the response is suitable for the agent to explain or act on
**And** recommended `next_step` items can be inserted into `Compass.md` after user approval
**And** recommendations can be prioritized by historical `is_happy_moment` outcomes when enough data exists
**And** advice is framed as a recommendation, not obligation or pressure

### SG-MVP-006 - Partner-driven Goal Instructions

**Given** a goal belongs to the first MVP partner category
**When** the agent requests guidance for a participant's current contract state
**Then** the platform can route the request to the partner instruction provider
**And** the response can include subscription-backed advice when applicable
**And** partner know-how is exposed as current-step recommendations, not full internal methodology

### SG-MVP-007 - Anonymous Aggregates

**Given** multiple users log commits against the same goal
**When** the platform renders MVP statistics
**Then** it can show Social Capital, active participant count, happy moment count, and activity freshness
**And** it does not expose personal rankings or named public comparisons

## Development Maintenance Scenarios

### SG-DEV-001 - PRD Diff-first Upkeep

**Given** the source Text changes after the last processed commit
**When** the `sg-prd` workflow processes the diff
**Then** it classifies changes into README, BACKLOG, HISTORY, and RESEARCH updates
**And** it advances `references/last-processed-commit.txt` only after applying the accepted PRD changes
**And** it does not own product runtime execution

### SG-DEV-002 - Acceptance-first Change Control

**Given** a proposed MVP behavior change
**When** development starts on that behavior
**Then** this acceptance spec is updated before implementation
**And** the PRD README stays aligned with the acceptance scenario
**And** implementation work is limited to the smallest behavior needed to satisfy the scenario

### SG-DEV-003 - Shared Development Memory Sync

**Given** an accepted PRD change, architecture decision, MVP status update, blocker, or partner-scope decision
**When** the change is finalized in the PRD repo or development workflow
**Then** a durable summary is retained into the shared development memory bank or tagged project scope
**And** the memory includes required tags `project:sg` and `scope:dev`
**And** the memory includes enough context to support future RAG recall: decision, reason, date, source file or commit when available, and current status
**And** secrets, credentials, raw private notes, routine logs, and noisy terminal output are not retained

### SG-DEV-004 - Shared Development Memory Recall

**Given** an agent starts a Shared Goals PRD, acceptance-test, or implementation task
**When** the agent recalls project memory
**Then** it can retrieve current MVP phase, accepted scope, recent decisions, blockers, and relevant partner-status context
**And** recall starts with tags `project:sg` and `scope:dev`
**And** the agent treats repository files as source of truth when memory and repo content conflict
**And** any discovered memory conflict is corrected by retaining an updated fact after the repo state is verified

## Review Checklist

- Every MVP implementation task maps to at least one acceptance scenario above.
- Every new scenario states what is intentionally out of scope.
- Agent-first interaction remains the primary surface.
- Platform participant identity remains `user_id`; agent keys authenticate access but do not become participants.
- Shared development memory is a RAG coordination layer, not the source of truth.
- Shared development memory uses only canonical tags from this document.
- Partner behavior is concrete enough to test.
- Goal Discovery remains post-MVP unless this PRD explicitly changes scope.