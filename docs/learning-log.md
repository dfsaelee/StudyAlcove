# Learning log

## Milestone 0 — Node.js foundation

The project switched from the uncommitted Go foundation to Node.js 22 with plain JavaScript and ES modules. Node's built-in HTTP and test modules require no runtime dependencies. PostgreSQL is a separate local Compose service; neither endpoint checks it yet. A shutdown signal allows active HTTP requests five seconds to finish.

### Learner exercise (15–40 minutes)

In `apps/room-server/test/http.test.js`, add a test for `GET /readyz` using the existing mock response as an example. Verify status 200 and body `ready\n`, and check that a non-GET request is rejected. Run `npm test`. Explain when readiness could fail even though liveness still succeeds.
