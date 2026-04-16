@echo off
set PLUGIN_DIR=%~dp0..
python "%PLUGIN_DIR%\scripts\set_state.py" on
python "%PLUGIN_DIR%\scripts\start_overlay.py"
