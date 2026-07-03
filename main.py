import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import pyautogui

pyautogui.FAILSAFE = True  # slam mouse to a screen corner to force-stop


class AutoClickerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Randomized Double-Click Autoclicker")
        self.root.resizable(False, False)

        self.stop_event = threading.Event()
        self.worker: threading.Thread | None = None

        frm = ttk.Frame(root, padding=16)
        frm.grid()

        row = 0
        ttk.Label(frm, text="Initial click interval (s)", font=("", 10, "bold")).grid(
            column=0, row=row, columnspan=2, sticky="w", pady=(0, 4)
        )
        row += 1
        ttk.Label(frm, text="Min").grid(column=0, row=row, sticky="e")
        self.initial_min = tk.StringVar(value="1.0")
        ttk.Entry(frm, textvariable=self.initial_min, width=8).grid(column=1, row=row, sticky="w")
        row += 1
        ttk.Label(frm, text="Max").grid(column=0, row=row, sticky="e")
        self.initial_max = tk.StringVar(value="3.0")
        ttk.Entry(frm, textvariable=self.initial_max, width=8).grid(column=1, row=row, sticky="w")

        row += 1
        ttk.Separator(frm, orient="horizontal").grid(
            column=0, row=row, columnspan=2, sticky="ew", pady=8
        )

        row += 1
        ttk.Label(frm, text="Secondary click interval (s)", font=("", 10, "bold")).grid(
            column=0, row=row, columnspan=2, sticky="w", pady=(0, 4)
        )
        row += 1
        ttk.Label(frm, text="Min").grid(column=0, row=row, sticky="e")
        self.secondary_min = tk.StringVar(value="0.1")
        ttk.Entry(frm, textvariable=self.secondary_min, width=8).grid(column=1, row=row, sticky="w")
        row += 1
        ttk.Label(frm, text="Max").grid(column=0, row=row, sticky="e")
        self.secondary_max = tk.StringVar(value="0.4")
        ttk.Entry(frm, textvariable=self.secondary_max, width=8).grid(column=1, row=row, sticky="w")

        row += 1
        ttk.Label(
            frm,
            text=(
                "Each cycle: wait a random time in the initial interval,\n"
                "click, wait a random time in the secondary interval,\n"
                "click again (the \"double click\"), then repeat.\n"
                "Move the mouse to a screen corner to force-stop."
            ),
            justify="left",
            foreground="#555555",
        ).grid(column=0, row=row, columnspan=2, sticky="w", pady=(8, 0))

        row += 1
        self.status_var = tk.StringVar(value="Stopped")
        ttk.Label(frm, textvariable=self.status_var, foreground="#0a6").grid(
            column=0, row=row, columnspan=2, pady=(8, 0)
        )

        row += 1
        self.toggle_btn = ttk.Button(frm, text="Start", command=self.toggle)
        self.toggle_btn.grid(column=0, row=row, columnspan=2, sticky="ew", pady=(8, 0))

        self.root.bind("<Escape>", lambda _e: self.stop())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _read_intervals(self):
        try:
            i_min = float(self.initial_min.get())
            i_max = float(self.initial_max.get())
            s_min = float(self.secondary_min.get())
            s_max = float(self.secondary_max.get())
        except ValueError:
            messagebox.showerror("Invalid input", "All interval fields must be numbers.")
            return None

        if i_min < 0 or i_max < 0 or s_min < 0 or s_max < 0:
            messagebox.showerror("Invalid input", "Intervals must be non-negative.")
            return None
        if i_min > i_max:
            messagebox.showerror("Invalid input", "Initial min must be <= initial max.")
            return None
        if s_min > s_max:
            messagebox.showerror("Invalid input", "Secondary min must be <= secondary max.")
            return None

        return i_min, i_max, s_min, s_max

    def toggle(self):
        if self.worker and self.worker.is_alive():
            self.stop()
        else:
            self.start()

    def start(self):
        intervals = self._read_intervals()
        if intervals is None:
            return
        i_min, i_max, s_min, s_max = intervals

        self.stop_event.clear()
        self.worker = threading.Thread(
            target=self._click_loop, args=(i_min, i_max, s_min, s_max), daemon=True
        )
        self.worker.start()

        self.toggle_btn.config(text="Stop")
        self.status_var.set("Running…")

    def stop(self):
        self.stop_event.set()
        self.toggle_btn.config(text="Start")
        self.status_var.set("Stopped")

    def _click_loop(self, i_min, i_max, s_min, s_max):
        try:
            while not self.stop_event.is_set():
                if self.stop_event.wait(random.uniform(i_min, i_max)):
                    break
                pyautogui.click()

                if self.stop_event.wait(random.uniform(s_min, s_max)):
                    break
                pyautogui.click()
        except pyautogui.FailSafeException:
            pass
        finally:
            self.root.after(0, self.stop)

    def on_close(self):
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    AutoClickerApp(root)
    root.mainloop()
