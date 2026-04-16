from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "state.json"
LOG_PATH = ROOT / "approval-events.log"
JSONL_LOG_PATH = ROOT / "approval-events.jsonl"

DEFAULT_STATE = {
    "enabled": True,
    "autoApprove": True,
    "translateNotifications": True,
    "logEvents": True,
}


def read_state() -> dict:
    if not STATE_PATH.exists():
        STATE_PATH.write_text(
            json.dumps(DEFAULT_STATE, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return DEFAULT_STATE.copy()
    raw = STATE_PATH.read_text(encoding="utf-8").strip()
    if not raw:
        return DEFAULT_STATE.copy()
    state = json.loads(raw)
    merged = DEFAULT_STATE.copy()
    merged.update(state)
    return merged


def write_log(line: str) -> None:
    state = read_state()
    if not state.get("logEvents", True):
        return
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"[{stamp}] {line}\n")


def write_event(message: str, translated: str) -> None:
    state = read_state()
    if not state.get("logEvents", True):
        return
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event": "notification",
        "action": "translated",
        "message": message,
        "summary_zh": translated,
    }
    with JSONL_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def translate_message(message: str) -> str:
    if "Claude needs your permission to use Bash" in message:
        return "Claude 需要你的授权才能执行 Bash 命令。"
    if "Claude needs your permission" in message:
        return "Claude 需要你的授权才能继续执行工具。"
    if not message.strip():
        return ""
    return f"原始通知（未做完整机器翻译）: {message}"


def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        return 0
    payload = json.loads(raw)
    state = read_state()
    if not state.get("enabled", True) or not state.get("translateNotifications", True):
        return 0

    translated = translate_message(str(payload.get("message", "")))
    if translated:
        write_log(f"中文提示: {translated}")
        write_event(str(payload.get("message", "")), translated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
