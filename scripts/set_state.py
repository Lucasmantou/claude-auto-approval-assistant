from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "state.json"

DEFAULT_STATE = {
    "enabled": True,
    "autoApprove": True,
    "translateNotifications": True,
    "logEvents": True,
}


def read_state() -> dict:
    if not STATE_PATH.exists():
        return DEFAULT_STATE.copy()
    raw = STATE_PATH.read_text(encoding="utf-8").strip()
    if not raw:
        return DEFAULT_STATE.copy()
    state = json.loads(raw)
    merged = DEFAULT_STATE.copy()
    merged.update(state)
    return merged


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"on", "off"}:
        print("用法: python set_state.py [on|off]")
        return 1

    enabled = sys.argv[1] == "on"
    state = read_state()
    state["enabled"] = enabled
    state["autoApprove"] = enabled
    state["translateNotifications"] = enabled

    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("approval-cn-helper 已开启。" if enabled else "approval-cn-helper 已关闭。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
