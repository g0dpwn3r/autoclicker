<!--
Guidance for automated coding agents (Copilot/Coding AI) working on this repo.
Keep this file short, actionable and repo-specific. Avoid generic advice.
-->
# Copilot instructions — python-autoclicker

Quick context (the why):
- This repository implements a small, single-process desktop AutoClicker written in Python with a Tkinter GUI. The main flow:
  - `main.py` instantiates `inc.GUI.GUI` which builds the Tk UI and kicks off recording in a background thread.
  - `inc/Recording.py` listens to a hotkey (pynput) and mouse events to record click positions and timings. It then delegates replay to `inc/Clicker.py`.
  - `inc/Clicker.py` performs movements and clicks using `pyautogui`, applying easing functions and randomized timing/position.
  - `inc/ConfigParse.py` reads/writes `config.ini` and converts the model list strings into pyautogui easing functions.
  - `inc/GUIConsole.py` is a singleton Toplevel used by `Clicker`/`Recording` to display recorded rows and export CSVs.

Key files to inspect when making changes:
- `main.py` — app entry and lifecycle.
- `inc/GUI.py` — UI layout, platform fallbacks (wmctrl/xdotool) and how recording is started.
- `inc/Recording.py` — event loop for keyboard/mouse; state machine: recording <-> waiting_for_start <-> clicking.
- `inc/Clicker.py` — movement / click replay logic, radius/angle math, use of pyautogui easing functions.
- `inc/ConfigParse.py` — config serialization/parsing; maps strings like `easeInQuad` to functions.
- `inc/GUIConsole.py` — singleton pattern; `get_instance()` is used across the codebase.

Important design notes and constraints (do not break these):
- Single-threaded UI: GUI runs on Tk mainloop. Long-running work (Recording.record) is started via a daemon thread in `GUI.start()` to avoid blocking the UI.
- `GUIConsole` is implemented as a singleton Toplevel — create it only via `GUIConsole.get_instance()`.
- Hotkey handling relies on `pynput.keyboard.Key` objects. `Recording` accepts either a Key or a string like `Key.space` — prefer preserving that conversion logic.
- Config parsing stores easing function names as a space-separated string in `config.ini`. Changes must preserve backward-compatible formatting.
- pyautogui's FailSafeException is surfaced in `Clicker.click` — do not suppress it silently.

Platform-specific behavior and fallbacks:
- Window selection: `inc/GUI.app_list()` prefers `pygetwindow` and falls back to Linux commands `wmctrl` and `xdotool`. When writing features that interact with windows, keep these fallbacks in mind and avoid assuming `pygetwindow` exists.
- Icon loading in `GUI.__init__` attempts to load `icon.ico` and falls back gracefully. Tests should avoid relying on GUI assets being present.

Developer workflows and commands discovered from repo files:
- Run app locally (development):
  - Install deps: `pip install -r Requirements.txt`
  - Run: `python main.py`
- Packaging: `setup.py` contains a py2exe setup for building a Windows console exe. Do not remove without adding a replacement.

Project-specific conventions and patterns:
- Minimal type use: code is mostly dynamic-typed. When adding annotations, keep them optional and local to new functions.
- Singletons: `GUIConsole` follows a simple `_instance` pattern — follow it when adding similar global UI components.
- Config format: `config.ini` uses section `[Mouse]` and keys exactly as in `ConfigParse`. Use `ConfigParse` helpers when reading/writing instead of touching `config.ini` directly.

Testing, linting and build hints for an AI agent:
- There are no unit tests in the repo. For quick validation of changes:
  - Run `python -m pyflakes <file>` or `python -m py_compile <file>` to check syntax.
  - Run the GUI: `python main.py` (interactive smoke test).
- When editing modules used by the GUI, start the app and exercise the hotkey flow — the event loop and pynput listeners are the main runtime concerns.

Small examples from the codebase (use these patterns):
- Mapping easing names to functions (see `inc/ConfigParse.parseQuad`):
  - 'easeInQuad' -> `pyautogui.easeInQuad`

- Creating the singleton console (see `inc/GUIConsole.get_instance`):
  - `guic = GUIConsole.get_instance()` — don't instantiate `GUIConsole()` directly.

What an AI agent should do when making changes:
- Preserve public behavior: GUI layout, config format, and hotkey semantics must remain stable unless the change is explicit and documented.
- If you add dependencies, update `Requirements.txt` and document in README.
- Add small, focused smoke tests when changing parsing logic (e.g., a short script that reads `config.ini` via `ConfigParse` and asserts expected values).

When unsure or blocked:
- If a change affects runtime behavior (hotkeys, recording, clicking), provide an instruction for a human to run the app and verify.
- Ask for clarification before changing packaging (`setup.py`) or the config format.

Contact for follow-up (leave as TODO if unknown):
- If you change behavior that might impact users (timing, randomness, default keybind), add a short entry in README and open a PR mentioning manual testing steps.

---

If anything here seems incomplete or you need examples for a specific change, tell me which file or behavior you want the agent to edit and I will expand this doc with exact code snippets and test suggestions.
