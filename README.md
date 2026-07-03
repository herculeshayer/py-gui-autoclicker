# py-gui-autoclicker

A randomized "double-click" autoclicker with a tkinter UI.

Each cycle:
1. Wait a random time within the **initial click interval**.
2. Click.
3. Wait a random time within the **secondary click interval**.
4. Click again (the "double click").
5. Repeat until stopped.

Set both intervals' min/max in the UI, then press **Start**. Press **Stop**
(same button) or hit `Escape` to stop. Slamming the mouse into a screen
corner also force-stops it (pyautogui failsafe).

## Run locally with uv

```bash
uv run python main.py
```

## Run in Docker

Requires an X server reachable from the container (WSLg on Windows works
out of the box; on native Linux you may need `xhost +local:root` first).

```bash
docker compose up --build
```
