from __future__ import annotations

import json
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


state = read_state()
enabled = "开启" if state.get("enabled", True) else "关闭"
approve = "自动同意" if state.get("autoApprove", True) else "不自动同意"
translate = "记录中文提示" if state.get("translateNotifications", True) else "不记录中文提示"
print(f"approval-cn-helper 状态: {enabled} / {approve} / {translate}")
