# Changelog

All notable changes to **Wexxy PC Bot** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-11-05

### Added
- **Dedicated `removed/` Archive Hierarchy**:
  - `removed/backup_files/`: Archived historical `.bak` files (`bot.py.bak`, `launcher.py.bak`, `touchpad.py.bak`).
  - `removed/disabled_plugins/`: Archived disabled experimental plugins (`swarm.py.disabled`, `syzygy_agent.py.disabled`, `vision.py.disabled`).
  - `removed/legacy_docs/`: Archived 9 early planning markdown drafts (`app_flow.md`, `backend_schema.md`, `fix_without_ai.md`, `identity.md`, `implementation_plan.md`, `learnings.md`, `prd.md`, `trd.md`, `ui_ux_design.md`) consolidated into `PROJECT_MANUAL.md`.
  - `removed/one_off_scripts/`: Archived standalone test scripts (`screen_ocr.py`, `test_launch.py`, `check_status.py`, `path_to_ocr.txt`, `query`, `full_deps.txt`, `full_requirement.txt`, `vision_temp.png`, `bot.log`).
  - `removed/scratch/`: Archived temporary scratch scripts and experimental suites.
  - `removed/swarm_system/`: Archived separate SwarmSystem particle and Blender 5.1 research files (`Swarm-system.md`, `swarm_tetra_visualizer.py`, `swarm_tetra_addon.zip`, `swarm_tetra_addon/`, `swarm.log`).
  - `removed/README.md`: Index and explanation of all archived assets.
- **Security & Secret Isolation**:
  - Created `.env` and `.env.example` to isolate Telegram bot credentials and admin IDs.
  - Refactored `config.py` to securely read configuration from `.env` and environment variables without requiring external dependencies.
  - Sanitized hardcoded tokens across all scripts before archival.
  - Created comprehensive `.gitignore` preventing accidental commits of secrets, runtime locks, logs, vendorized libraries (`libs/`), and cache files.
- **Documentation Overhaul**:
  - Created top-level `README.md` with complete architectural overview, quick start, command catalog, and security specifications.
  - Created `AGENTS.md` specifying operational guidelines, plugin conventions, and safety constraints for autonomous AI coding agents.
  - Updated `PROJECT_MANUAL.md` with newly added active plugins and the `.env` configuration architecture.
  - Created `CHANGELOG.md` to track architectural milestones.

### Changed
- Active plugins catalog in `PROJECT_MANUAL.md` synchronized with production codebase to include `shell.py`, `software.py`, `easy_ocr.py`, and `routing.py`.
- Cleaned root repository workspace of redundant files, leaving only production code, configuration templates, and documentation.

---

## [2.0.0] - 2026-10-26

### Added
- **Linux-Like Interactive Shell (`plugins/shell.py`)**: Added `/sh` command supporting persistent directory navigation (`cd`, `pwd`, `ls`, `cat`, `mkdir`, `rm`, `mv`, `cp`, `tree`, `whoami`, `hostname`, `env`, `head`, `tail`, `touch`, `clear`).
- **Windows Package Management (`plugins/software.py`)**: Added `/winget` integration allowing headless package search, installation, upgrade, and listing.
- **Screen OCR via EasyOCR (`plugins/easy_ocr.py`)**: Replaced deprecated Tesseract implementation with EasyOCR, removing dependency on external Tesseract binaries.
- **Dynamic Media Routing (`plugins/routing.py`)**: Added `/media_route_reveal` and `/change_media_route` commands to switch media destinations on-the-fly.
- **IDE Bridge (`plugins/antigravity.py`)**: Added `/control_antigravity <prompt>` to automate IDE workspace focus and prompt transfer.
- **Automatic Command Autocomplete Sync**: Dynamic registration of all loaded plugins directly with Telegram's bot menu via `application.bot.set_my_commands()`.

### Fixed
- **Media Routing Registration**: Moved `/media_route_reveal` and `/change_media_route` handlers outside the optional `plugins.voice` try block in `bot.py` so they are always registered even when voice packages are absent.
- **Multimodal Image Upload Fallback**: Protected incoming image uploads in `plugins/files.py` with try/except so absence of `plugins.voice` gracefully falls back to saving files in `Downloads/WexxyBot/`.
- **Nebula Dashboard Template Path**: Fixed `nebula_dashboard/app.py` to resolve `index.html` relative to script directory rather than process working directory.
- **Documentation Command Accuracy**: Updated `README.md` and `PROJECT_MANUAL.md` command catalogs to reflect `/rustdesk`, `/pc_status`, `/monitor` (Guardian mode), and web tools.
- Fixed touchpad coordinate letterboxing issue via `getAbsoluteCoords()` in `trackpad.html`.
- Enforced `--no-autoupdate` on `cloudflared.exe` Popen call to avoid tunnel freezing.
- Added automatic process termination for orphaned `cloudflared.exe` instances.

---

## [1.1.0] - 2026-05-19

### Added
- **Nebula OS Dashboard (`nebula_dashboard/`)**: Integrated glassmorphic system monitoring dashboard with real-time CPU, RAM, and disk utilization charts via Chart.js and Flask.
- **Consolidated Master Guide (`PROJECT_MANUAL.md`)**: Consolidated early architectural specifications, PRDs, TRDs, and operational manuals into a unified document.

### Fixed
- Fixed Telegram polling conflict bug via single-instance process lock `wexxy.bot.lock`.

---

## [1.0.0] - 2026-05-04

### Added
- Initial release of Wexxy PC Bot.
- Asynchronous Telegram bot core with dynamic plugin discovery.
- System volume control via `pycaw`.
- Screen capture via `mss` and `Pillow`.
- Fast file search using Everything CLI (`es.exe`).
- Remote mouse and keyboard emulation via `pyautogui`.
- Remote touchpad web portal served via Flask and Cloudflare tunnels.
- Windows power management (lock, shutdown, restart, sleep, logout).

