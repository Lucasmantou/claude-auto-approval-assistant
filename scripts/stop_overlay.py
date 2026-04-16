from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = ROOT / ".runtime"
PID_PATH = RUNTIME_DIR / "overlay-process.pid"
LEGACY_PID_PATH = ROOT / "overlay-process.pid"


def main() -> int:
    LEGACY_PID_PATH.unlink(missing_ok=True)
    if not PID_PATH.exists():
        print("悬浮窗未运行。")
        return 0

    try:
        pid = int(PID_PATH.read_text(encoding="utf-8").strip())
    except ValueError:
        PID_PATH.unlink(missing_ok=True)
        print("悬浮窗 PID 文件无效，已清理。")
        return 0

    subprocess.run(
        ["taskkill", "/PID", str(pid), "/T", "/F"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    PID_PATH.unlink(missing_ok=True)
    try:
        RUNTIME_DIR.rmdir()
    except OSError:
        pass
    print("悬浮窗已停止。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
