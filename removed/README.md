# Archived / Removed Files Index

This directory archives obsolete, disabled, backup, scratch, and unrelated files previously located in the root repository. They have been preserved here for historical reference without cluttering the active codebase.

## Directory Structure

### 1. `backup_files/`
Safety copies generated during previous maintenance cycles:
- `bot.py.bak`: Historical backup of the main orchestrator script.
- `launcher.py.bak`: Backup of the launcher plugin prior to Start Menu shortcut enhancements.
- `touchpad.py.bak`: Earlier version of touchpad/streaming plugin before scaling logic refinement.

### 2. `disabled_plugins/`
Plugins that were disabled via `.disabled` extension or superseded by other implementations:
- `swarm.py.disabled`: Old HTTP client plugin attempting to communicate with external SwarmSystem on port 5010.
- `syzygy_agent.py.disabled`: Experimental plugin for triggering external LangGraph loop (`SYZYGY_MAXX`).
- `vision.py.disabled`: Tesseract-based OCR plugin; superseded by `plugins/easy_ocr.py`.

### 3. `legacy_docs/`
Fragmented early markdown notes (May 2026) that have now been completely synthesized and updated in `PROJECT_MANUAL.md` and `README.md`:
- `app_flow.md`
- `backend_schema.md`
- `fix_without_ai.md`
- `identity.md`
- `implementation_plan.md`
- `learnings.md`
- `prd.md`
- `trd.md`
- `ui_ux_design.md`

### 4. `one_off_scripts/`
Ad-hoc manual test scripts and transient files:
- `bot.log`: Old runtime log from initial testing.
- `check_status.py`: Quick verification script for Telegram Bot API status.
- `full_deps.txt`, `full_requirement.txt`: Verbose pip freeze dumps (superseded by standard `requirements.txt`).
- `path_to_ocr.txt`: One-line path pointer to external OCR experiments.
- `query`: Scratch text file.
- `screen_ocr.py`: Standalone CLI OCR test script (bot now uses `plugins/easy_ocr.py`).
- `test_launch.py`: Test script checking `pyautogui.press('win')`.
- `tessdata/`: Empty directory from tesseract test.
- `vision_temp.png`: Transient screenshot generated during OCR development.

### 5. `scratch/`
Experimental and self-correction test scripts:
- `agent_action.py`: Intermediate script generated during LLM self-correction tests.
- `fix_markdown.py`: One-off utility for linting markdown documentation.
- `test_all_plugins.py`: Early test runner for plugins.
- `test_lint.md`: Markdown test payload.
- `test_swarm_direct.py`, `test_swarm_retry.py`: One-off HTTP client test scripts for swarm API.
- `watch_and_fix.py`: Experimental watcher script.
- `wexxy_generated_app.py`: Sample generated script from agent experiments.

### 6. `swarm_system/`
Files belonging to the separate SwarmSystem project (`C:\Users\SUBU\Documents\1MY_APPs\SwarmSystem`):
- `Swarm-system.md`: 2700-line roadmap and notes for hardware-accelerated particle/swarm research.
- `swarm.log`: Output log from swarm experiment runs.
- `swarm_tetra_addon/` & `swarm_tetra_addon.zip`: Blender 5.1 addon for 3D visualization.
- `swarm_tetra_visualizer.py`: Blender Python script for rendering telemetry.
