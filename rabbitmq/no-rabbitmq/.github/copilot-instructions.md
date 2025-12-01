## Quick context

This repository implements a small Telegram bot + worker system using Pyrogram, RabbitMQ (pika) and ffmpeg.
Key runtime pieces:
- `bot` (entry `bot.py`) — Pyrogram bot that receives updates and enqueues tasks.
- `worker` (entry `worker.py`) — consumes RabbitMQ tasks and uses ffmpeg to process media.
- `workmanager` (`workmanager.py`) — in-process producer/consumer helper used for local task management.
- `session/` — Pyrogram session files (e.g. `bot2.session`, `myapp.session`).

Files you will likely touch: `bot.py`, `worker.py`, `workmanager.py`, `task.py`, `util.py`, `myhandler.py`, `config.py`, `compose.yaml`, `Containerfile.client`, `Containerfile.worker`, `env.ini`, `requirements.txt`.

## Big-picture architecture (what to know)

- Message flow: the bot creates tasks (Task objects) that are serialized (dill) and published to a RabbitMQ queue (`Keys.TASKS_QUEUE` in `util.py`). The `worker` process consumes that queue and performs ffmpeg work, then uses the bot session to send results back to users.
- Configuration: `config.AppConfig` reads `env.ini` when run locally. When running in containers it expects environment variables (the code treats presence of `api_id` env var as "container mode").
- Sessions: Pyrogram session files live in `session/`. `bot.py` calls `cache.clear_all_sessions()` at startup — be careful when modifying session handling.
- Containers: `Containerfile.client` runs `python bot.py`; `Containerfile.worker` runs `python worker.py`. Both create a venv at `/home/appuser/venv` and set `USER appuser` (UID/GID controlled via `env.ini` build keys `UID`/`GID`).

## How to run & debug (concrete commands & notes)

- Local dev (non-container): populate `env.ini` (see `env.ini.example`), then run:
  - `python3 -m pip install -r requirements.txt`
  - `python bot.py` or `python worker.py`

- Using Compose (builds Containerfiles): the repo contains `compose.yaml`. To run with Docker:
  - `docker compose up --build` (or with Podman: `podman-compose up --build` if you use podman-compose)
  - Note: volume mounts in `compose.yaml` are commented out. Uncomment the `volumes:` lines to mount local code into the containers during development.

- Debugging: `bot.py` imports `debugpy` and calls `debugpy.listen(('localhost', 5678))`. When debugging inside a container you must:
  - Expose or forward port 5678 from the container to the host (compose currently does not expose it).
  - Alternatively, run `bot.py` locally with the same env values so debugpy listens on your localhost.

## Project-specific conventions & pitfalls

- Container detection: `AppConfig` sets `container = True` iff the `api_id` environment variable exists. When running tests or containers, prefer setting env vars rather than relying on `env.ini`.
- Env key names: RabbitMQ keys are expected as `RABBITMQ_DEFAULT_USER`, `RABBITMQ_DEFAULT_PASS`, `RABBITMQ_DEFAULT_HOST`, `RABBITMQ_DEFAULT_VHOST` in the `[rabbitmq]` section (see `env.ini`). `config.AppConfig` maps these to `rabbitmq_user`, `rabbitmq_password`, `rabbitmq_host`, `rabbitmq_vhost`.
- UID/GID: Containerfiles create an `appuser` and set ownership using `--chown=appuser:appuser` when copying files. If you mount sources from the host, ensure UID/GID in `env.ini` matches your host user to avoid permission issues.
- Sessions: `session/` files are binary and should not be accidentally removed — bot startup clears sessions via `cache.clear_all_sessions()`; review `cache.py` before changing session logic.

## Integration points

- RabbitMQ: code uses `pika.BlockingConnection` and `pika.ConnectionParameters` in `worker.py` and `workmanager.py`. Queue name uses `Keys.TASKS_QUEUE` from `util.py`.
- Telegram API: `pyrogram.Client` instances are created in both `bot.py` and `worker.py` to send/receive messages. `worker.py` uses a bot session `session/bot2` to download/upload media.

## Examples (copy-paste snippets)

- Run worker locally using `env.ini` values:
  - `python worker.py`

- Build and run both services with Docker Compose (rebuild images):
  - `docker compose up --build --remove-orphans`

## Where to look next

- If you need message queue constants and task shape, inspect `task.py` and `util.py` (they define `TaskType` and `Keys`).
- For request handlers, open `myhandler.py` to see how updates and callback queries are converted into tasks.

If any of the above assumptions are incorrect or you'd like me to include extra development tips (for example, explicit port-forward examples for `debugpy`, or a recommended `docker compose` snippet for dev), tell me which items to expand and I'll iterate.
