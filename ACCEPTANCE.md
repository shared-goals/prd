# Shared Goals - MVP Acceptance Specification

This document is the TDD-first acceptance layer for the Shared Goals MVP. It turns the PRD plan into testable use cases before platform implementation starts.

## Scope

These scenarios cover the MVP only:
- humans interact through agents equipped with the `shared-goals` skill
- agents create or join goals, create contracts, log commits, and request advice
- agents may use a human's ordinary Markdown/text workspace as context
- partner-driven goals can return specialized instructions and subscription-backed advice

Out of scope for MVP acceptance:
- messenger-specific integrations
- proactive Goal Discovery and deduplication
- standalone consumer UI as the primary interaction surface

Permanent platform anti-goals:
- leaderboards and personal rankings
- streak mechanics
- default reminders or pressure mechanics
- competitive public goals

## Test Data Baseline

Use one concrete MVP partner goal type when running acceptance tests. Until the partner is finalized, use a named fixture such as `partner_goal_type = "computer_club"` or `partner_goal_type = "water_activity"`; the behavior must be concrete even if the real partner name changes.

Minimum domain fixtures:
- `user_id`: platform participant; internal UUID, no channel identifier
- `goal_id`: shared goal visible in the MVP instance
- `contract_id`: active personal time contract for the user and goal
- `commit_id`: logged progress item against the contract
- `partner_id`: instruction provider for the partner-driven goal

Authentication fixture when needed:
- `agent_key_id`: API key or credential assigned to an agent and scoped to `user_id`; it identifies access, not a platform participant. One user may have many keys for different agents.

## Product Acceptance Scenarios

### SG-MVP-001 - Human Text-base Flow

**Given** a user works with an agent using Markdown-like files with tags and structure
**When** the user asks the agent to connect current planning context to Shared Goals
**Then** the agent can identify candidate goal context without requiring a separate manual UI
**And** the platform stores only the normalized goal/contract/commit data needed for the MVP
**And** private source text remains outside public aggregates by default

### SG-MVP-002 - Create Goal Through Agent

**Given** the user expresses a concrete non-competitive goal through an agent
**When** the agent calls the platform to create the goal
**Then** the platform creates a goal with title, description, visibility, and `instance_id`
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
**When** the agent logs progress on the user's behalf
**Then** the platform records `time_minutes`, `done`, optional `next_step`, `skill_tag`, and `is_happy_moment`
**And** `done` can be derived from a previous `next_step` when appropriate
**And** the commit is anonymous by default in public views

### SG-MVP-005 - Request Advice Or Instructions

**Given** the user has an active contract for a goal with instructions
**When** the agent asks the platform for the next useful recommendation
**Then** the platform returns current-moment advice or instructions for that goal
**And** the response is suitable for the agent to explain or act on
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

## Review Checklist

- Every MVP implementation task maps to at least one acceptance scenario above.
- Every new scenario states what is intentionally out of scope.
- Agent-first interaction remains the primary surface.
- Platform participant identity remains `user_id`; agent keys authenticate access but do not become participants.
- Partner behavior is concrete enough to test.
- Goal Discovery remains post-MVP unless this PRD explicitly changes scope.