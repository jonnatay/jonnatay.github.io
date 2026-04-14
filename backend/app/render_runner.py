from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from app.config import Settings


@dataclass
class RenderResult:
    success: bool
    workspace: Path
    output_path: Path | None
    stdout_log: str
    stderr_log: str
    error_message: str | None
    runtime_ms: int
    output_bytes: int | None


def _find_rendered_video(workspace: Path) -> Path | None:
    candidates = sorted(workspace.rglob("*.mp4"))
    return candidates[0] if candidates else None


def _cleanup_workspace(workspace: Path) -> None:
    shutil.rmtree(workspace, ignore_errors=True)


def run_render_job(job_id: str, source_code: str, settings: Settings) -> RenderResult:
    workspace = Path(tempfile.mkdtemp(prefix=f"manim-render-{job_id[:8]}-"))
    source_path = workspace / "user_scene.py"
    source_path.write_text(source_code, encoding="utf-8")

    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges=true",
        "--memory",
        f"{settings.render_memory_mb}m",
        "--cpus",
        str(settings.render_cpus),
        "--read-only",
        "--tmpfs",
        "/tmp:rw,size=64m",
        "-e",
        "HOME=/tmp",
        "-e",
        "XDG_CACHE_HOME=/tmp/.cache",
        "-e",
        "MPLCONFIGDIR=/tmp/matplotlib",
        "-v",
        f"{workspace}:/workspace",
        "-w",
        "/workspace",
        settings.manim_runtime_image,
        "manim",
        f"-{settings.manim_render_quality}",
        "--resolution",
        settings.manim_render_resolution,
        "/app/manimTest.py",
        "-o",
        "output",
        "--",
        "--mainScene",
        "/workspace/user_scene.py",
    ]

    start_time = time.perf_counter()

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=settings.render_timeout_seconds,
            check=False,
        )
    except FileNotFoundError:
        runtime_ms = int((time.perf_counter() - start_time) * 1000)
        return RenderResult(
            success=False,
            workspace=workspace,
            output_path=None,
            stdout_log="",
            stderr_log="",
            error_message="Docker is not installed or is not available on this worker host.",
            runtime_ms=runtime_ms,
            output_bytes=None,
        )
    except subprocess.TimeoutExpired as error:
        runtime_ms = int((time.perf_counter() - start_time) * 1000)
        return RenderResult(
            success=False,
            workspace=workspace,
            output_path=None,
            stdout_log=error.stdout or "",
            stderr_log=error.stderr or "",
            error_message=f"Render timed out after {settings.render_timeout_seconds} seconds.",
            runtime_ms=runtime_ms,
            output_bytes=None,
        )

    runtime_ms = int((time.perf_counter() - start_time) * 1000)
    output_path = _find_rendered_video(workspace)

    if completed.returncode != 0:
        return RenderResult(
            success=False,
            workspace=workspace,
            output_path=output_path,
            stdout_log=completed.stdout,
            stderr_log=completed.stderr,
            error_message="The render container exited with a non-zero status.",
            runtime_ms=runtime_ms,
            output_bytes=output_path.stat().st_size if output_path and output_path.exists() else None,
        )

    if not output_path:
        return RenderResult(
            success=False,
            workspace=workspace,
            output_path=None,
            stdout_log=completed.stdout,
            stderr_log=completed.stderr,
            error_message="The render finished without producing an MP4 file.",
            runtime_ms=runtime_ms,
            output_bytes=None,
        )

    return RenderResult(
        success=True,
        workspace=workspace,
        output_path=output_path,
        stdout_log=completed.stdout,
        stderr_log=completed.stderr,
        error_message=None,
        runtime_ms=runtime_ms,
        output_bytes=output_path.stat().st_size,
    )


def cleanup_render_result(result: RenderResult) -> None:
    _cleanup_workspace(result.workspace)
