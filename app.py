import json
import os
import threading
import time
import tkinter as tk
from tkinter import ttk

from core.quality import check_quality
from core.router import RouterController

CONFIG_FILE = "data/config.json"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(CONFIG_FILE)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


class InternetManagerApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Internet Manager")
        self.root.geometry("560x520")
        self.root.minsize(520, 480)

        self.config = load_config()
        self.connections = {
            c["name"]: c for c in self.config["connections"]
        }
        self.router = RouterController(self.connections)

        self.active = self.config.get("active", self.config["connections"][0]["name"])
        self.scores = {name: None for name in self.connections}
        self.status = {name: "Checking..." for name in self.connections}

        self.auto_mode = tk.BooleanVar(value=self.config.get("mode") == "auto")
        self.running = True

        self._build_ui()

        self._start_monitor()

    def _build_ui(self):

        # Colors
        self.bg = "#1e1e2e"
        self.card_bg = "#2a2a3c"
        self.accent = "#4a9eff"
        self.green = "#3fb950"
        self.red = "#f85149"
        self.yellow = "#d29922"
        self.fg = "#e6e6e6"
        self.muted = "#8b8b9e"

        self.root.configure(bg=self.bg)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.bg)
        style.configure("Card.TFrame", background=self.card_bg)
        style.configure("TLabel", background=self.bg, foreground=self.fg, font=("Segoe UI", 11))
        style.configure("Card.TLabel", background=self.card_bg, foreground=self.fg, font=("Segoe UI", 11))
        style.configure("Title.TLabel", background=self.bg, foreground=self.fg, font=("Segoe UI Semibold", 16))
        style.configure("Muted.TLabel", background=self.bg, foreground=self.muted, font=("Segoe UI", 10))
        style.configure("CardMuted.TLabel", background=self.card_bg, foreground=self.muted, font=("Segoe UI", 10))
        style.configure("Active.TLabel", background=self.card_bg, foreground=self.green, font=("Segoe UI Semibold", 11))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Accent.TButton", font=("Segoe UI Semibold", 10), padding=8)
        style.configure("TCheckbutton", background=self.bg, foreground=self.fg, font=("Segoe UI", 11))

        # Header
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=16, pady=(16, 8))

        ttk.Label(header, text="Internet Manager", style="Title.TLabel").pack(side="left")

        auto_cb = ttk.Checkbutton(
            header,
            text="Auto Mode",
            variable=self.auto_mode,
            command=self._on_auto_toggle
        )
        auto_cb.pack(side="right")

        # Connection cards
        self.cards_frame = ttk.Frame(self.root)
        self.cards_frame.pack(fill="x", padx=16, pady=8)

        self.card_widgets = {}

        for name, conn in self.connections.items():
            self._build_card(name, conn)

        # Log area
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(8, 16))

        ttk.Label(log_frame, text="Activity Log", style="Muted.TLabel").pack(anchor="w")

        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg=self.card_bg,
            fg=self.fg,
            insertbackground=self.fg,
            relief="flat",
            font=("Consolas", 10),
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True, pady=(4, 0))

        # Footer
        footer = ttk.Frame(self.root)
        footer.pack(fill="x", padx=16, pady=(0, 12))

        refresh_btn = ttk.Button(
            footer,
            text="Refresh Now",
            command=self._force_refresh
        )
        refresh_btn.pack(side="right")

        self.status_label = ttk.Label(footer, text="Monitoring...", style="Muted.TLabel")
        self.status_label.pack(side="left")

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_card(self, name, conn):

        card = ttk.Frame(self.cards_frame, style="Card.TFrame")
        card.pack(fill="x", pady=4, ipadx=10, ipady=8)

        top = ttk.Frame(card, style="Card.TFrame")
        top.pack(fill="x")

        ttk.Label(top, text=name, style="Card.TLabel").pack(side="left")

        active_label = ttk.Label(top, text="", style="Active.TLabel")
        active_label.pack(side="left", padx=(8, 0))

        score_label = ttk.Label(top, text="--", style="Card.TLabel")
        score_label.pack(side="right")

        ttk.Label(top, text="Score:", style="CardMuted.TLabel").pack(side="right", padx=(0, 4))

        mid = ttk.Frame(card, style="Card.TFrame")
        mid.pack(fill="x", pady=(2, 2))

        status_label = ttk.Label(mid, text="Checking...", style="CardMuted.TLabel")
        status_label.pack(side="left")

        bottom = ttk.Frame(card, style="Card.TFrame")
        bottom.pack(fill="x", pady=(2, 0))

        switch_btn = ttk.Button(
            bottom,
            text="Switch to this",
            style="Accent.TButton",
            command=lambda n=name: self._manual_switch(n)
        )
        switch_btn.pack(side="right")

        self.card_widgets[name] = {
            "active": active_label,
            "score": score_label,
            "status": status_label,
            "button": switch_btn
        }

    def _start_monitor(self):

        def loop():
            while self.running:
                self._check_all()
                if self.auto_mode.get():
                    self._auto_decide()
                time.sleep(10)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def _check_all(self):

        for name, conn in self.connections.items():
            threading.Thread(
                target=self._check_one,
                args=(name, conn["interface"]),
                daemon=True
            ).start()

    def _check_one(self, name, interface):

        self.status[name] = "Checking..."
        self._update_card(name)

        try:
            result = check_quality(interface)
            score = result["score"]
            ping = result["ping"]
        except Exception:
            score = 0
            ping = {"online": False, "latency": None, "loss": 100}

        self.scores[name] = score

        if ping["online"]:
            lat = ping.get("latency")
            lat_str = f"{int(lat)} ms" if lat else "n/a"
            self.status[name] = f"{lat_str} | loss {ping.get('loss', 0)}%"
        else:
            self.status[name] = "Offline"

        self._update_card(name)

    def _update_card(self, name):

        if name not in self.card_widgets:
            return

        w = self.card_widgets[name]
        score = self.scores[name]

        self.root.after(0, lambda: self._apply_card_update(name, w, score))

    def _apply_card_update(self, name, w, score):

        if score is None:
            w["score"].config(text="--")
        else:
            if score >= 70:
                color = self.green
            elif score >= 40:
                color = self.yellow
            else:
                color = self.red
            w["score"].config(text=str(score), foreground=color)

        w["status"].config(text=self.status[name])

        w["active"].config(
            text="(Active)" if name == self.active else "",
            foreground=self.green if name == self.active else self.muted
        )

    def _auto_decide(self):

        primary = min(self.connections.values(), key=lambda c: c["priority"])["name"]
        backup = max(self.connections.values(), key=lambda c: c["priority"])["name"]

        primary_score = self.scores.get(primary)
        backup_score = self.scores.get(backup)

        if primary_score is None or backup_score is None:
            return

        if self.active == primary:
            if primary_score < 50 and backup_score >= 70:
                self._switch_to(backup, reason="primary quality low")
        else:
            if primary_score >= 80:
                self._switch_to(primary, reason="primary recovered")

    def _manual_switch(self, name):

        if self.auto_mode.get():
            self._log("Turn off Auto Mode to switch manually.")
            return

        self._switch_to(name, reason="manual")

    def _switch_to(self, name, reason=""):

        if name == self.active:
            return

        try:
            self.router.switch(name)
        except Exception as e:
            self._log(f"Failed to switch to {name}: {e}")
            return

        self.active = name
        self.config["active"] = name
        save_config(self.config)

        msg = f"Switched to {name}"
        if reason:
            msg += f" ({reason})"
        self._log(msg)

        for n in self.connections:
            self._update_card(n)

    def _on_auto_toggle(self):

        mode = "auto" if self.auto_mode.get() else "manual"
        self.config["mode"] = mode
        save_config(self.config)
        self._log(f"Mode: {mode}")

    def _force_refresh(self):

        self._log("Refreshing...")
        threading.Thread(target=self._check_all, daemon=True).start()

    def _log(self, message):

        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"

        def append():
            self.log_text.config(state="normal")
            self.log_text.insert("end", line)
            self.log_text.see("end")
            self.log_text.config(state="disabled")

        self.root.after(0, append)

    def _on_close(self):

        self.running = False
        self.root.destroy()


def main():

    root = tk.Tk()
    app = InternetManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
