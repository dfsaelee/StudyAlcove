# StudyAlcove — Agent Instructions

These instructions apply to coding agents in this repository. Read [the roadmap](docs/roadmap.md) and work only on the current, approved milestone. If instructions conflict, follow explicit user directions, then this file, then the roadmap. Surface material conflicts before changing architecture.

## Working together

- **Planning thread:** owns the roadmap, scope, architecture, tradeoffs, sequencing and acceptance criteria. Use Plan Mode frequently to decide what to build and why.
- **Implementation thread:** owns one approved, narrow task at a time. Inspect the relevant code, propose a concrete plan, implement after it is accepted, run checks and report findings. Do not independently expand the roadmap.
- Chat decisions are not automatically shared across threads. Record agreed decisions in the repository, preferably in `docs/decisions/` or `docs/learning-log.md`.

## Plan and scope

1. Start substantial work in Plan Mode. Inspect the code and active milestone first.
2. Present a short plan covering the goal, why it matters, files, design choices, data flow, tests and one learner-owned task.
3. Choose the smallest maintainable solution. Do not introduce infrastructure or frameworks simply because they appear later in the roadmap.
4. Execute only the agreed scope and stop after the milestone for review. Document sensible local decisions; escalate changes to APIs, data models, service boundaries or deployment architecture.

## Code and learning

- Write clear, idiomatic, human-scale Go with straightforward control flow and focused responsibilities. Avoid speculative abstractions, sweeping refactors and clever compression.
- Explain why and document invariants, concurrency assumptions and non-obvious behavior; do not narrate obvious code. Handle errors explicitly and make ownership, synchronization, cancellation and shutdown understandable.
- Keep dependencies limited and justified, match repository style and run `gofmt`.
- Use AI for scaffolding, wiring, fixtures, configuration and repetitive work. Explain important components and trace a concrete request or event through them.
- Where practical, leave 1–2 bounded learner implementation or test TODOs with inputs, expected behavior and edge cases. Do not withhold essential scaffolding.
- When reviewing learner code, give hints and reasoning before a complete solution unless the user asks for one. Explain concurrency, WebSockets, gRPC, persistence and failure handling in more depth when introduced.
- Never claim a feature, performance target or test works without verification.

## Milestone completion

Deliver a runnable, demonstrable scenario with focused, formatted changes. Document important decisions and limitations. Run relevant checks and report exact commands and results, including checks not run.

Finish with changed files, a brief architecture and data-flow explanation, learner TODOs, validation results, 2–3 comprehension questions and the next proposed milestone. Do not implement the next milestone without review.

## Architecture boundaries

- Start backend-first with a modular Go application and server-authoritative room state.
- Use WebSockets for ephemeral presence and movement; PostgreSQL is the source of truth for durable study sessions.
- Introduce gRPC, Redis, Kafka, observability and Kubernetes only when their planned milestones justify them.
- A logical room is not a Kubernetes pod; one room-server instance can host multiple logical rooms.
- Prefer an affordable AWS deployment path before considering managed Kubernetes.
