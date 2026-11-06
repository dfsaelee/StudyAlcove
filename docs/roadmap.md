# StudyAlcove — Coding Agent Master Plan

## Project identity
- **Product name:** StudyAlcove (final working name; replaces StudyTown and StudyNook).
- **Repository name:** `studyalcove` (proposed).
- **Domain:** Not selected or availability-verified. Previous StudyNook domain ideas are not automatically carried over.
- **Tagline (optional):** A little place to focus, together.

## Project brief
StudyAlcove is a cozy browser-based multiplayer study room. Players join a room under a guest identity, move an avatar around, take a seat, start a focus timer, see other users' presence, and accumulate verified study-session history. Prioritize a working, understandable backend over a beautiful frontend. Build in small testable slices, not one giant code generation pass.

**Learning contract:** You are simultaneously a senior engineer, implementation assistant, and tutor. Generate boilerplate and repetitive code quickly, but stop at the end of EACH milestone. Explain architectural decisions; never silently introduce new dependencies, services, or patterns. Let the learner implement targeted TODOs, then review and test them. Do not proceed automatically.

**Agent workflow:** See `AGENTS.md` for the two-thread Plan Mode / implementation workflow, human-readable code conventions, and milestone handoff rules.

## Guiding principles
1. Backend first. First build HTTP APIs and a Go WebSocket server testable with scripts; frontend comes after the core room behavior works.
2. Start as a modular monolith (`room-server`) and PostgreSQL; extract a session service once there is a meaningful service boundary.
3. Real-time position updates are ephemeral; completed study sessions are durable.
4. Use one logical room per room ID; one backend process may host many rooms. One Kubernetes pod per room is NOT the starting architecture.
5. Make the server authoritative for room membership, movement constraints, timer start/end timestamps, and study credit.
6. Every milestone must have passing tests, run instructions, and explicit acceptance criteria.
7. Use pinned stable dependency versions compatible with the environment. Prefer `net/http`, `github.com/coder/websocket`, `pgx`, Go's testing package; use Redis/Kafka/Kubernetes only in the milestones that require them.
8. Avoid GraphQL, complex auth, microservice proliferation, and premature infrastructure. They are future optional experiments, not MVP blockers.
9. Avoid hard-coded secrets and unbounded memory/queues. Validate inputs, authenticate connection identities, use origin allowlists and request limits, keep basic observability.
10. Never claim scale or latency improvements unless measured with scripts and recorded results.

## What counts as MVP
- A user opens the app, receives an anonymous guest ID (server-issued, signed or securely random session token), chooses a display name, and joins an existing room using a room code.
- A room contains multiple active connections; new arrivals see a complete initial snapshot; existing participants receive join/move/leave messages.
- Avatar movement is bounded by the room and validated by the server. A disconnect removes ephemeral presence; reconnect restores identity but not stale position unless explicitly designed.
- A user starts a focus session and eventually completes it. Server-authoritative timing prevents client-only credit fabrication. A completed session is written once to PostgreSQL even if completion requests are retried.
- A minimal 2D browser scene shows at least two concurrent clients, a desk and focus timer, and recent completed study time.
- Two-browser demo, backend integration tests, graceful shutdown and Docker Compose startup instructions all work.

## Initial stack
- Backend: Go, `net/http`, `github.com/coder/websocket`, `context.Context`, structured logging, `go test -race`.
- Storage: PostgreSQL, SQL migrations, `pgx` connection pool. In-memory room state until distributed milestone.
- Frontend (later): React + TypeScript + Vite + PixiJS, minimal art placeholders.
- Local ops: Docker Compose for PostgreSQL, Go dev process. Dockerize later.
- Later: Protobuf/gRPC between room-server and session-service; Redis pub/sub + presence lease; Kafka for durable events; OpenTelemetry + Prometheus + Grafana; kind for Kubernetes; AWS EC2 + Docker Compose first.

## Suggested repository layout
```
studyalcove/
  README.md
  AGENTS.md
  docs/
    architecture.md
    decisions/
    learning-log.md
    protocols.md
    runbooks/
  apps/
    room-server/
      cmd/server/main.go
      internal/config/
      internal/httpapi/
      internal/ws/
      internal/room/
      internal/session/
      internal/storage/
    session-service/           # add only at Milestone 6
    web/                       # add only at Milestone 5
  proto/                       # add only at Milestone 6
  db/migrations/
  deploy/
    compose/
    k8s/                      # add only at Milestone 10
  scripts/
    ws-smoke-test/
    load-test/
  .github/workflows/
```
Use clear Go package boundaries without forced abstractions. Folder structure is a proposal; adapt if simpler.

## API and WebSocket contract (initial proposal)
REST:
- `GET /healthz` — process alive (no dependency check)
- `GET /readyz` — process ready to accept traffic; check needed dependencies when applicable
- `POST /api/guests` — returns secure guest credential and guest ID
- `POST /api/rooms` — create a room, returns non-guessable or safely generated room code
- `GET /api/rooms/{id}` — room metadata; don't disclose private participant data
- Later `GET /api/me/sessions` — authenticated completed sessions

WebSocket: `GET /ws?roomId=...` with authenticated guest identity (prefer a short-lived HttpOnly cookie or short-lived token; do not log credentials). Production origins explicitly allowlisted. Message envelope:
```
{ "type": "player.move", "requestId": "...", "payload": { "x": 4, "y": 7 } }
```
Server messages include `room.snapshot`, `player.joined`, `player.moved`, `player.left`, `focus.started`, `focus.completed`, `error`. Define canonical schemas in `docs/protocols.md`, including validation, event IDs, versioning and sample messages. Prefer grid/tile-based movement and modest update rates. New members receive authoritative snapshot before incremental events; document any ordering guarantees and overflow policy. Avoid exposing auth tokens in URLs where possible.

Data model v1:
- `guests(id, display_name, created_at)` — optional persistent anonymous identities, tied to a secure credential
- `rooms(id, name, created_at)`
- `focus_sessions(id, guest_id, room_id, started_at, ends_at, completed_at, status, duration_seconds, idempotency_key)`
Use proper foreign keys, constraints, uniqueness of idempotency keys scoped to the guest/action, timestamps in UTC, and migration rollback documentation. Credit computed from trusted server time; handle cancellations, disconnects and duplicate completes explicitly. Do not pretend a client timer alone makes study sessions cheat-proof.

## Milestone 0 — Foundation
**Agent builds:** Go module, minimal HTTP service, config/env validation, logging, graceful shutdown, README, Makefile/task commands, one unit test, Docker Compose for PostgreSQL (DB needn't be connected yet), CI for formatting/vet/tests.
**Learner TODO:** Implement or explain the difference between `/healthz` and `/readyz`; add a graceful shutdown timeout.
**Tests:** `go test ./...`, `go vet ./...`, `curl localhost:8080/healthz`; ctrl-C exits cleanly.
**Teach:** Go module, handlers, contexts, signal handling, dependency lifecycle.
**Stop:** request approval before milestone 1.

## Milestone 1 — Room HTTP API
**Agent builds:** guest creation flow, room creation and metadata, input validation, error responses, in-memory repository interfaces (or DB if integration is simple), unit tests, request examples.
**Learner TODO:** Implement room code generation and validation; review why secure randomness matters.
**Tests:** valid create/read; invalid names, duplicate IDs, room not found; input bounds; concurrent room creation.
**Teach:** REST semantics, IDs, data races, interfaces, errors.
**Stop.**

## Milestone 2 — WebSocket presence
**Agent builds:** authenticated WS handshake, room hub with join/leave, one per-connection read loop, safe outbound write approach, bounded outbound queues, heartbeat/ping or read deadlines, snapshot on join, smoke-test CLI with two clients.
**Learner TODO:** Implement player leave cleanup and bounded-queue overflow behavior; understand why network writes must not block room-wide coordination.
**Tests:** two clients see same room, leave broadcasts, invalid origin/credential rejected, slow client handling, race detector.
**Teach:** goroutines, channels, mutexes, backpressure, cancellation, WebSocket handshake.
**Stop.**

## Milestone 3 — Authoritative room state
**Agent builds:** tile-based movement command validation, avatar positions, basic occupied desk state, snapshot sequencing; implement serialized room command processing or a clearly synchronized state model.
**Learner TODO:** Implement bounds checks and reject movement that exceeds configured speed/distance; write tests.
**Tests:** concurrent move/join/leave under `-race`; out-of-bounds rejects; snapshot state matches later broadcasts; duplicate moves handled appropriately.
**Teach:** ownership of mutable state, event loops vs mutexes, consistency models, client prediction vs authority.
**Stop.**

## Milestone 4 — Persistent focus sessions
**Agent builds:** SQL migrations, repository, start/cancel/complete endpoints or WS actions, server-controlled timestamps, PostgreSQL integration tests, retry-safe idempotent completion, durable read API.
**Learner TODO:** Add uniqueness constraint for idempotency and demonstrate a retry doesn't double-credit; design disconnect semantics.
**Tests:** two completions with same key result in one row; crash/restart preserves completed sessions; DB failure returns actionable error; transaction rollback.
**Teach:** SQL constraints, transactions, exactly-once effects vs at-least-once requests, timestamps.
**Stop.**

## Milestone 5 — Minimal playable frontend
**Agent builds:** React/TS/Vite/PixiJS scene, temporary tile/art placeholders, room join, two-browser movement, desk interaction, focus timer UI, optimistic UI cautiously reconciled to authoritative server state, reconnect state.
**Learner TODO:** Implement one rendered player state or desk interaction and trace the message all the way to backend.
**Tests:** two browsers show each other's avatars, refresh/reconnect, focus session persists, error states visible.
**Teach:** client/server state, rendering loops, interpolation, WebSocket reconnect.
**Stop. This is the first public demo candidate.**

## Milestone 6 — Meaningful gRPC boundary
**Agent builds:** extract `session-service` into separate Go process, Protobuf service for Start/Complete/GetSession; room-server calls it with deadlines and meaningful error mapping; keep PostgreSQL owned by session-service. Provide grpc health checks and local Compose networking.
**Learner TODO:** Add deadline handling and one integration test simulating session-service timeout.
**Tests:** session service down -> room movement still works, session completion gives explicit retryable error, no duplicate credit, protobuf generation repeatable.
**Teach:** network boundaries, contract evolution, deadlines, partial failures.
**Stop.**

## Milestone 7 — Multiple room servers and Redis
**Agent builds:** run two room-server instances; introduce room ownership/routing strategy (e.g., deterministic room-to-instance assignment with a small gateway or router). Use Redis for presence leases and coordination as necessary, not as a magical fix for shared state. Ensure one authoritative owner per room at a time, or deliberately implement cross-instance pub/sub semantics with proper snapshot/reconnect behavior. Document tradeoffs.
**Learner TODO:** Explain why a single WebSocket connection stays with a backend process and how room affinity and migration work; implement a reconnect test.
**Tests:** users join same room consistently, restart owner and reconnect, expiring ghost presence, graceful draining on shutdown, repeated recovery tests.
**Teach:** distributed ownership, leases, pub/sub delivery, failure recovery, split brain.
**Stop.**

## Milestone 8 — Kafka durable events
**Agent builds:** create `focus.completed` event publication after DB commit via transactional outbox, a background publisher, Kafka-compatible local broker (Kafka/Redpanda), analytics consumer, idempotent consumer upsert, and replay strategy. Never publish client movement into Kafka as a requirement.
**Learner TODO:** Implement idempotent analytics update and a test that replays duplicate completion events.
**Tests:** database commit before publish survives process restart, consumer restart/replay preserves totals, producer outage keeps outbox events pending, poison message policy documented.
**Teach:** transaction outbox, consumer offsets, at-least-once delivery, materialized views.
**Stop.**

## Milestone 9 — Operability
**Agent builds:** OpenTelemetry traces/metrics (active WS connections, room count, accepted/rejected commands, focus session completions, DB latency, gRPC errors/deadlines, outbox lag, consumer lag), Prometheus/Grafana local setup, structured logs with trace identifiers, load script and benchmark document.
**Learner TODO:** Create a dashboard panel and explain one full event trace; inject a downstream timeout and capture trace.
**Tests:** load tests record p50/p95/p99 broadcast latency, sustained connections, CPU/memory, failures; compare configurations honestly. Do not claim specific numbers in advance.
**Teach:** SLIs, cardinality, tracing, bottlenecks, chaos testing.
**Stop.**

## Milestone 10 — AWS + Kubernetes
**Path A (earliest deploy):** AWS EC2 running Docker Compose, reverse proxy with TLS, DNS, persistent PostgreSQL volume or managed DB, locked-down security groups, backups, health checks, automatic deployment via GitHub Actions, budgets/cost alarms. For public launch, ensure secure auth/origin configuration, resource limits and basic abuse controls.
**Path B (Kubernetes learning):** local `kind` cluster; `Deployment` for room-server replicas, `Service`, Ingress/controller, readiness/liveness, resource requests/limits, rolling deployments and graceful connection drain. Use managed PostgreSQL or a separate safe stateful strategy in real deployments. Document network routing and affinity. Optional AWS EKS only after verifying costs and explicit desire; do not require EKS for the app.
**Learner TODO:** explain how SIGTERM and readiness affect WebSocket clients; demonstrate rolling update and reconnection.
**Tests:** health checks, deploy/rollback, restart server while clients reconnect, backup restore drill, smoke tests against deployment.
**Teach:** containers, orchestration, autoscaling caveats for long-lived sockets, AWS networking/costs.
**Stop.**

## Agent execution protocol — mandatory at each milestone
Before writing code output:
1. **Goal in 2–3 sentences.**
2. **Why now** and how it advances the architecture.
3. **Design options:** at least two when there is a significant decision; pick the simplest.
4. **Files to create/edit** with responsibility for each.
5. **Event/data flow** with a concrete example.
6. **Learner TODO (15–40 min):** leave 1–2 meaningful, clearly scoped functions/tests to implement; do not block trivial tool setup.
7. **Acceptance tests and exact commands** to run.
Then implement ONLY that milestone; run tests and report actual results/errors. End with:
- Changed files + concise explanation
- Why each new dependency was needed
- Concepts learned + one example trace through code
- 3 knowledge-check questions with answers hidden until asked
- Observed tests and outputs (no unverified claims)
- Known limitations, risks, and next milestone (do not implement it)
- Commit message suggestion

**Code review protocol:** When the learner supplies a solution to a TODO, review correctness, edge cases, race safety, error handling, and clarity. Offer hints before writing the full answer unless asked for it. Keep a `docs/learning-log.md` with concise summaries, decision records, and questions.

## Starter prompt to paste into a coding agent
You are my senior Go backend engineer and technical tutor. Read `docs/roadmap.md` in full and follow it as the project source of truth. I want to use AI for speed but understand every architectural decision. Start with Milestone 0 ONLY, backend-first. Before coding, show the proposed folder structure, components, data flow, acceptance tests, and one scoped learner TODO. Then implement the milestone, actually run available checks, and stop. Do not build the frontend, gRPC, Redis, Kafka, Kubernetes or AWS infrastructure yet. If the plan has ambiguity, make the simplest reasonable choice and document it. Do not claim passing tests that were not executed. Give me a concise tutorial on the important code and 3 check-for-understanding questions at the end. Wait for my review before proceeding to Milestone 1.

## Resume/portfolio evidence to collect
- 60-second two-browser demo video and architecture diagram.
- Public demo URL, reproducible local dev instructions, annotated protocol schema.
- Load test script, measured p95 latencies and concurrency with hardware/conditions noted.
- Failure demo: kill a room process, observe reconnect/recovery; kill session-service and validate graceful degradation.
- One detailed architecture decision record (why WebSockets, why Redis, why Kafka only for durable events, why gRPC extraction).
- CI tests, race detection, deploy workflow and a short operations runbook.
