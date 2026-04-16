from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OVERLAY_SCRIPT = ROOT / "scripts" / "overlay_window.py"
RUNTIME_DIR = ROOT / ".runtime"
PID_PATH = RUNTIME_DIR / "overlay-process.pid"
LEGACY_PID_PATH = ROOT / "overlay-process.pid"


def is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    result = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    return str(pid) in result.stdout


def main() -> int:
    LEGACY_PID_PATH.unlink(missing_ok=True)
    RUNTIME_DIR.mkdir(exist_ok=True)
    subprocess.run(
        ["attrib", "+h", str(RUNTIME_DIR)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    if PID_PATH.exists():
        try:
            existing = int(PID_PATH.read_text(encoding="utf-8").strip())
            if is_running(existing):
                print("悬浮窗已在运行。")
                return 0
        except ValueError:
            pass

    creationflags = 0x08000000
    process = subprocess.Popen(
        [sys.executable, str(OVERLAY_SCRIPT)],
        cwd=str(ROOT),
        creationflags=creationflags,
    )
    PID_PATH.write_text(str(process.pid), encoding="utf-8")
    print(f"悬浮窗已启动，PID={process.pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
