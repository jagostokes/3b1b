"""Open rendered video with the system player."""

import subprocess
import sys
from pathlib import Path


def play_video(path: Path) -> None:
    """Open the video file with the default system player."""
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    elif sys.platform == "linux":
        subprocess.Popen(["xdg-open", str(path)])
    elif sys.platform == "win32":
        subprocess.Popen(["start", str(path)], shell=True)
    else:
        print(f"Video saved at: {path}")
