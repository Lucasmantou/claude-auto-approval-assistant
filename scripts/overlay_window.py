from __future__ import annotations

import json
import subprocess
import sys
import tkinter as tk
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "state.json"
JSONL_LOG_PATH = ROOT / "approval-events.jsonl"
SET_STATE_SCRIPT = ROOT / "scripts" / "set_state.py"


def read_state() -> dict:
    if not STATE_PATH.exists():
        return {
            "enabled": True,
            "autoApprove": True,
            "translateNotifications": True,
            "logEvents": True,
        }
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


class OverlayApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Claude 自动同意提示")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)
        self.root.configure(bg="#101418")
        self.root.geometry(self._initial_geometry())
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.minsize(392, 340)

        frame = tk.Frame(self.root, bg="#101418", padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Claude 自动同意助手",
            fg="#f5f7fa",
            bg="#101418",
            font=("Microsoft YaHei UI", 12, "bold"),
            anchor="w",
        )
        title.pack(fill="x")

        self.status_var = tk.StringVar(value="状态加载中...")
        status = tk.Label(
            frame,
            textvariable=self.status_var,
            fg="#9ccfd8",
            bg="#101418",
            font=("Microsoft YaHei UI", 9),
            anchor="w",
        )
        status.pack(fill="x", pady=(6, 8))

        self.toggle_button = tk.Button(
            frame,
            text="切换中...",
            command=self.toggle_enabled,
            bg="#2e6f95",
            fg="white",
            relief="flat",
            font=("Microsoft YaHei UI", 9),
            padx=10,
            pady=4,
        )
        self.toggle_button.pack(anchor="w", pady=(0, 8))

        self.latest_var = tk.StringVar(value="等待新的自动同意记录...")
        latest = tk.Label(
            frame,
            textvariable=self.latest_var,
            fg="#ffffff",
            bg="#1b222b",
            justify="left",
            wraplength=356,
            padx=10,
            pady=10,
            font=("Microsoft YaHei UI", 10),
            anchor="nw",
        )
        latest.pack(fill="x")

        history_label = tk.Label(
            frame,
            text="最近记录",
            fg="#f5f7fa",
            bg="#101418",
            font=("Microsoft YaHei UI", 10, "bold"),
            anchor="w",
        )
        history_label.pack(fill="x", pady=(10, 4))

        self.history_text = tk.Text(
            frame,
            height=8,
            width=48,
            bg="#11161d",
            fg="#d8dee9",
            relief="flat",
            wrap="word",
            font=("Microsoft YaHei UI", 9),
        )
        self.history_text.pack(fill="both", expand=True)
        self.history_text.configure(state="disabled")

        button_row = tk.Frame(frame, bg="#101418")
        button_row.pack(fill="x", pady=(8, 0))

        refresh_btn = tk.Button(
            button_row,
            text="刷新",
            command=self.refresh,
            bg="#2e6f95",
            fg="white",
            relief="flat",
            font=("Microsoft YaHei UI", 9),
        )
        refresh_btn.pack(side="left")

        self.refresh()

    def _initial_geometry(self) -> str:
        width = 392
        height = 320
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max(screen_w - width - 28, 0)
        y = max(screen_h - height - 80, 0)
        return f"{width}x{height}+{x}+{y}"

    def load_records(self) -> list[dict]:
        if not JSONL_LOG_PATH.exists():
            return []
        lines = JSONL_LOG_PATH.read_text(encoding="utf-8").splitlines()
        records: list[dict] = []
        for line in lines[-80:]:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return records

    def refresh(self) -> None:
        state = read_state()
        mode = "开启" if state.get("enabled", True) else "关闭"
        approve = "自动同意中" if state.get("autoApprove", True) else "手动审批"
        self.status_var.set(f"插件状态：{mode} / {approve}")
        if state.get("enabled", True):
            self.toggle_button.configure(text="关闭自动同意", bg="#6b2d38")
        else:
            self.toggle_button.configure(text="开启自动同意", bg="#2e6f95")

        records = self.load_records()
        latest_text = "等待新的自动同意记录..."
        history_lines: list[str] = []

        for record in reversed(records):
            summary = record.get("summary_zh", "")
            stamp = record.get("timestamp", "")
            action = record.get("action", "")
            if summary and latest_text == "等待新的自动同意记录...":
                latest_text = f"{stamp}\n{summary}"
            tool_name = record.get("tool_name", "")
            description = record.get("description", "")
            suffix = f" | {tool_name}" if tool_name else ""
            if description:
                suffix += f" | {description}"
            history_lines.append(f"[{stamp}] {summary}{suffix}")
            if len(history_lines) >= 8:
                break

        self.latest_var.set(latest_text)
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.insert("1.0", "\n\n".join(history_lines) if history_lines else "暂无历史记录。")
        self.history_text.configure(state="disabled")

        self.root.after(1800, self.refresh)

    def toggle_enabled(self) -> None:
        state = read_state()
        target = "off" if state.get("enabled", True) else "on"
        subprocess.run(
            [sys.executable, str(SET_STATE_SCRIPT), target],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        self.refresh()

    def close(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    OverlayApp().run()
