# approval-cn-helper

这是一个本地 Claude Code 插件，用来做三件事：

1. 在插件开启时，使用 `PermissionRequest` hook 自动批准权限弹窗，减少你手动按 `Yes`。
2. 把一部分权限相关英文通知写成中文摘要，并在桌面悬浮窗里实时显示。
3. 把每一次自动同意记录到文本日志和结构化历史日志，方便回顾。

## 使用方法

### 0. 最省事的双击入口

在 `D:\AAAkaifa\Claude助手` 根目录里，直接双击这个 BAT 即可：

- `启动Claude助手.bat`

启动后会默认打开悬浮窗，悬浮窗里直接提供：

- 自动同意开启 / 关闭按钮
- 当前状态显示
- 最近审批历史

### 1. 带插件启动 Claude

```bat
D:\AAAkaifa\Claude助手\bin\start-claude-with-helper.cmd
```

这个启动脚本会自动：

- 开启自动同意
- 启动桌面悬浮窗
- 用插件目录启动 Claude

### 2. 关闭自动同意

```bat
D:\AAAkaifa\Claude助手\bin\approval-helper-off.cmd
```

### 3. 重新开启

```bat
D:\AAAkaifa\Claude助手\bin\approval-helper-on.cmd
```

### 4. 查看当前状态

```bat
D:\AAAkaifa\Claude助手\bin\approval-helper-status.cmd
```

## 能力边界

- 这个插件能“自动批准”权限框，因为 Claude Code 官方 hooks 支持 `PermissionRequest` 决策。
- 这个插件不能稳定拿到权限框里展示的所有原始英文 UI 文本，所以不能保证逐字翻译屏幕上看到的每一行英文。
- 它当前做的是：对常见权限通知和 Bash 场景写中文摘要到日志文件和悬浮窗。

## 日志位置

```text
D:\AAAkaifa\Claude助手\approval-events.log
D:\AAAkaifa\Claude助手\approval-events.jsonl
```
