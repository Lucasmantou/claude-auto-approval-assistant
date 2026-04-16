@echo off
set PLUGIN_DIR=%~dp0..
python "%PLUGIN_DIR%\scripts\set_state.py" off
python "%PLUGIN_DIR%\scripts\stop_overlay.py"
