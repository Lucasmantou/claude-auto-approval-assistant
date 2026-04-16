# Claude Auto Approval Assistant

A local Claude Code assistant that reduces repetitive approval prompts, shows Chinese summaries in a floating desktop window, and keeps an approval history you can review later.

## What problem this solves

When you use Claude Code for multi-step work, repeated `Yes / No` confirmations can break your flow:

- frequent Bash approval prompts interrupt batch work
- English safety messages are easy to skim past or misunderstand
- after auto-handling a request, it is hard to remember what was approved

This project packages those needs into one local helper:

- auto-approve normal Claude Code permission requests
- translate common approval-related notifications into Chinese
- show the current status and recent history in a desktop floating window
- keep a local approval log for later review

## Why this is implemented as a plugin

This project uses Claude Code hooks instead of UI automation.

That choice is intentional:

- it works at the event layer, not by clicking screen coordinates
- it is more stable than simulating mouse or keyboard actions
- it can inspect request metadata and write meaningful logs
- it can be turned on or off without patching Claude itself

The core auto-approval path is implemented through the official `PermissionRequest` hook.

## Main features

### 1. One-click startup

Double-click:

```bat
启动Claude助手.bat
```

This launches Claude with the helper enabled and opens the floating window by default.

### 2. Floating desktop window

The floating window stays on top and shows:

- whether auto-approval is currently enabled
- a button to turn auto-approval on or off
- the latest approval-related Chinese summary
- recent approval history

### 3. Auto-approval for normal permission requests

For standard Claude Code permission requests, the plugin returns `allow` automatically.

### 4. Chinese summaries

Common approval-related notifications and Bash request summaries are converted into Chinese so you can quickly understand what happened.

### 5. Approval history

The helper writes both:

- a plain text log
- a structured JSONL history file

This makes it easier to review what was auto-approved later.

## Current limitations

- Some high-priority Bash safety prompts still require manual confirmation.
- The helper cannot reliably translate every raw UI line shown inside Claude Code dialogs.
- It is designed for local Windows usage and the current launcher is Windows-first.

## Project structure

```text
.claude-plugin/
bin/
hooks/
scripts/
启动Claude助手.bat
```

## Local files not committed

These runtime and personal files are ignored by Git:

- `.runtime/`
- `approval-events.log`
- `approval-events.jsonl`
- `state.json`
- `.claude/`

## Log locations

```text
approval-events.log
approval-events.jsonl
```

## Typical usage

1. Double-click `启动Claude助手.bat`
2. Claude starts with the helper enabled
3. The floating window appears automatically
4. Use the floating window button to toggle auto-approval if needed
5. Review recent approval history directly in the floating window

## Notes

This is a local helper project, not an official Anthropic product.
