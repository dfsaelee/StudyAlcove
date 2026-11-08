# StudyAlcove

StudyAlcove is a cozy browser-based multiplayer study space where people can join a pixel-art room, find a desk, and focus together.

## Getting started

Requirements: Node.js 22 and npm. Docker with Compose is needed for the local database. The commands below work directly in Windows PowerShell.

```powershell
npm start
```

The server runs at `http://127.0.0.1:8080`. Press Ctrl-C to stop it.

To start the local database in PowerShell, create a local env file and change the example password:

```powershell
Copy-Item deploy/compose/.env.example deploy/compose/.env
# Edit deploy/compose/.env and choose a local password.
docker compose --env-file deploy/compose/.env -f deploy/compose/compose.yaml up -d
```

If port 5432 is unavailable, add `POSTGRES_PORT=55432` to the env file.

To stop it, replace `up -d` with `down`. Database data is retained in a Docker volume.

## Checks

```powershell
npm run check
```

The check runs syntax validation, basic whitespace checks, and tests.

StudyAlcove is in development; the multiplayer experience is not yet available.
