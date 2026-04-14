# Manim Visualizer Backend

This backend provides the async FastAPI + Redis + Supabase control plane for the `Manim Visualizer` page in the Jekyll site.

## What It Does

- Accepts render submissions from the static frontend.
- Stores job state in Supabase.
- Queues work in Redis.
- Runs Manim renders on a Docker-capable worker host with the vendored `manimTest.py` runtime.
- Uploads completed `.mp4` files to a private Supabase Storage bucket and serves them through short-lived signed URLs.
- Starts each render in a locked-down Docker container with no network access, dropped Linux capabilities, a read-only root filesystem, and a temp-only writable home/cache path.

## Local Setup

1. Create a Python environment and install dependencies:

```powershell
cd E:\jonnatay.github.io\backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your Supabase + Redis values.

3. Build the render runtime image on a Docker-capable host:

```powershell
docker build -t manim-visualizer-runtime E:\jonnatay.github.io\backend\manim_runtime
```

4. Start the API:

```powershell
cd E:\jonnatay.github.io\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Start the worker in a separate shell:

```powershell
cd E:\jonnatay.github.io\backend
python -m app.worker
```

## Dockerized Backend

This repo now includes dedicated Docker images for the API, worker, and Redis:

- `Dockerfile.api`
- `Dockerfile.worker`
- `Dockerfile.redis`
- `docker-compose.yml`

From `E:\jonnatay.github.io\backend`, the usual flow is:

```powershell
docker build -t manim-visualizer-runtime .\manim_runtime
docker compose up --build
```

The compose stack starts:

- `redis` on port `6379`
- `api` on port `8000`
- `worker` with `/var/run/docker.sock` mounted so it can launch isolated Manim render containers

Keep `REDIS_URL=redis://redis:6379/0` in `.env` when using this compose stack. The `worker` container does not run Docker-in-Docker; it uses the host Docker daemon through the mounted socket.

## Important Constraints

- The browser does **not** need Docker to play finished MP4 files.
- The worker host **does** need Docker installed to generate new renders.
- The copied `manim_runtime/Dockerfile` reflects the current attached prototype. If you need `Tex` or `MathTex`, you will need to add TeX packages back into that image.

## Supabase

Run the SQL in `supabase/manim_jobs.sql` to create the table and private bucket metadata for this feature.
