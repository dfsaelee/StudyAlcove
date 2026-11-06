
# StudyAlcove — Agent Instructions

These instructions apply to coding agents working in the StudyAlcove repository. Read `docs/roadmap.md` for the full roadmap. Follow the current milestone only.

## Two-thread workflow

- **Orchestration / planning thread:** Owns the roadmap, architecture decisions, milestone scope, tradeoffs, sequencing, and acceptance criteria. Use Plan Mode frequently here. This thread decides **what** to build and **why**, not every implementation detail.
- **Implementation thread (Luna 6 / coding agent):** Owns one approved, narrowly scoped milestone or task at a time. It inspects the repo, proposes a concrete implementation plan, makes changes after the plan is accepted, runs checks, and reports findings. It does **not** independently expand the roadmap.
- Decisions made in chat are not automatically shared across threads. Record agreed decisions in the repository, preferably `docs/decisions/` or `docs/learning-log.md`, so both threads can read the same source of truth.
- If instructions conflict, prioritize explicit user directions, then this `AGENTS.md`, then the master plan. Surface material conflicts before changing architecture.

## Plan before implementation

1. Start substantial work in **Plan Mode**. Inspect relevant code and the active milestone first.
2. Present a short plan covering the goal, why it matters, files to change, design choices, data flow, tests, and one learner-owned task.
3. Prefer the smallest maintainable solution; do not add frameworks or infrastructure just because they are on the future roadmap.
4. Execute only the agreed scope. Stop after the milestone for review; don't silently proceed.
5. If a small local decision is needed, choose a sensible option and document it. Escalate decisions that change APIs, data models, service boundaries, or deployment architecture.

## Readable, human-scale code

- Write code for a human teammate: clear, direct, idiomatic Go, with understandable names and straightforward control flow.
- **Neither overly verbose nor overly compact:** avoid unnecessary helper layers and boilerplate, but don't compress logic into clever one-liners or dense abstractions.
- Prefer a small number of focused functions and packages with explicit responsibilities. Keep abstractions tied to actual needs rather than hypothetical future flexibility.
- Use comments to explain *why*, invariants, concurrency assumptions, and non-obvious behavior. Don't narrate obvious code.
- Handle errors explicitly. For concurrent code, make ownership, synchronization, cancellation, and shutdown behavior easy to reason about.
- Keep third-party dependencies limited and justified. Match existing repository style; format Go code with `gofmt`.
- Avoid unnecessary refactors, speculative features, and sweeping rewrites while implementing a milestone.

## AI acceleration without losing understanding

- Let the agent generate scaffolding, wiring, test fixtures, configuration, and repetitive code.
- Explain the purpose of each important component and how a request/event moves through it, with a concrete example.
- Leave 1–2 worthwhile, bounded implementation or test TODOs for the learner where practical. Specify inputs, expected behavior, and edge cases; don't withhold essential scaffolding.
- When reviewing learner code, provide hints and reasoning before a completed solution unless explicitly asked for the solution.
- Keep explanations concise by default; expand on goroutines, channels, mutexes, WebSockets, gRPC, persistence, and failure handling when introduced.
- Never claim a feature, performance target, or test is working without verifying it.

## Definition of done for each milestone

- The feature works through a runnable, demonstrable scenario.
- Relevant automated checks were executed; report exact commands and results, including any checks not run.
- Changes are narrowly scoped, formatted, and understandable.
- Document important decisions and remaining limitations.
- Finish with: changed files, brief architecture/data-flow explanation, learner TODO(s), validation commands/results, 2–3 comprehension questions, and the next proposed milestone **without implementing it**.

## Architecture boundaries

- Backend-first, starting as a modular Go application. Keep room state server-authoritative.
- WebSockets are for real-time ephemeral presence and movement; PostgreSQL is the source of truth for durable study sessions.
- Introduce gRPC, Redis, Kafka, observability, and Kubernetes when their planned milestones justify them—not all at once.
- A logical study room is not a Kubernetes pod. Multiple logical rooms can live in a room-server instance.
- Prefer an affordable AWS deployment path before considering managed Kubernetes infrastructure.
