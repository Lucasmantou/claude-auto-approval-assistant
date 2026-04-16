from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
JSONL_LOG_PATH = ROOT / "approval-events.jsonl"


def main() -> int:
    if not JSONL_LOG_PATH.exists():
        print("暂无审批历史。")
        return 0

    records = []
    for line in JSONL_LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if not records:
        print("暂无审批历史。")
        return 0

    for record in records[-30:]:
        stamp = record.get("timestamp", "")
        action = record.get("action", "")
        summary = record.get("summary_zh", "")
        tool_name = record.get("tool_name", "")
        description = record.get("description", "")
        command = record.get("command", "")

        print(f"[{stamp}] {action} {summary}")
        if tool_name:
            print(f"  工具: {tool_name}")
        if description:
            print(f"  说明: {description}")
        if command:
            print(f"  命令: {command}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
