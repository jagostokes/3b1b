"""Write generated scene files and render them with manimgl."""

import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = REPO_ROOT / "videos"


@dataclass
class RenderResult:
    success: bool
    video_path: Path | None
    error_msg: str


class Renderer:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_plan(self, plan: str) -> Path:
        """Save the LLM plan to the output folder."""
        plan_file = self.output_dir / "plan.txt"
        plan_file.write_text(plan)
        return plan_file

    def write_scene(self, code: str, attempt: int) -> Path:
        """Save generated code to the output folder."""
        scene_file = self.output_dir / f"scene_v{attempt}.py"
        scene_file.write_text(code)
        return scene_file

    def render(self, scene_file: Path) -> RenderResult:
        """Run manimgl on the scene file and return the result."""
        # Record time before render so we only pick up NEW videos
        before_render = time.time()

        cmd = ["manimgl", str(scene_file), "GeneratedScene", "-w"]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=REPO_ROOT,
            )
        except subprocess.TimeoutExpired:
            return RenderResult(
                success=False,
                video_path=None,
                error_msg="Render timed out after 300 seconds.",
            )

        if proc.returncode != 0:
            error = proc.stderr or proc.stdout
            if len(error) > 3000:
                error = error[:1500] + "\n...[truncated]...\n" + error[-1500:]
            return RenderResult(
                success=False,
                video_path=None,
                error_msg=error,
            )

        video = self._find_and_move_video(before_render)
        if video:
            return RenderResult(success=True, video_path=video, error_msg="")
        else:
            return RenderResult(
                success=False,
                video_path=None,
                error_msg=(
                    "Render exited with code 0 but no new .mp4 found in videos/.\n"
                    f"stdout: {proc.stdout[-500:] if proc.stdout else '(empty)'}\n"
                    f"stderr: {proc.stderr[-500:] if proc.stderr else '(empty)'}"
                ),
            )

    def _find_and_move_video(self, created_after: float) -> Path | None:
        """Find an .mp4 in videos/ created after the given timestamp and move it."""
        if not VIDEOS_DIR.exists():
            return None
        # Only consider files created/modified AFTER the render started
        mp4s = [
            p for p in VIDEOS_DIR.glob("**/*.mp4")
            if p.stat().st_mtime > created_after
        ]
        if not mp4s:
            return None
        mp4s.sort(key=lambda p: p.stat().st_mtime)
        source = mp4s[-1]
        dest = self.output_dir / "video.mp4"
        shutil.move(str(source), str(dest))
        return dest
