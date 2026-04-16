from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


def plugin_root() -> Path:
    return Path(__file__).resolve().parent.parent


ROOT = plugin_root()
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


def write_event(payload: dict, summary: str, action: str) -> None:
    state = read_state()
    if not state.get("logEvents", True):
        return

    tool_input = payload.get("tool_input") or {}
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event": "permission_request",
        "action": action,
        "tool_name": payload.get("tool_name", ""),
        "description": tool_input.get("description", ""),
        "command": tool_input.get("command", ""),
        "summary_zh": summary,
        "cwd": payload.get("cwd", ""),
    }
    with JSONL_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def chinese_summary(payload: dict) -> str:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input") or {}
    command = str(tool_input.get("command", ""))
    description = str(tool_input.get("description", ""))

    if tool_name == "Bash":
        if "\n#" in command or "\n #" in command:
            return "已自动同意 Bash 命令。检测到命令里有换行和注释，Claude 原本担心显示内容与实际执行内容不一致。"
        if any(token in command for token in ("&&", "||", ";")):
            return "已自动同意 Bash 命令。检测到这是一个复合命令，Claude 原本会要求你确认。"
        return f"已自动同意 Bash 命令。说明：{description} 命令：{command}"
    if tool_name == "Read":
        return "已自动同意读取文件。"
    if tool_name == "Write":
        return "已自动同意写入文件。"
    if tool_name == "Edit":
        return "已自动同意编辑文件。"
    if tool_name == "MultiEdit":
        return "已自动同意批量编辑文件。"
    return f"已自动同意工具调用。工具：{tool_name}"


def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        return 0

    payload = json.loads(raw)
    state = read_state()
    if not state.get("enabled", True) or not state.get("autoApprove", True):
        summary = f"插件已关闭，保留原始审批框。工具: {payload.get('tool_name', '')}"
        write_log(summary)
        write_event(payload, summary, "pass_through")
        return 0

    summary = chinese_summary(payload)
    write_log(summary)
    write_event(payload, summary, "auto_allow")

    result = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "allow",
            },
        }
    }
    sys.stdout.write(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
