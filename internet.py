import os, sys, threading
import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from ScriptRunner import Runner

class InternetPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        wifi_password = "wfx%$YEy#7vV"
        wifi_ssid = "PLAY_Swiatlowodowy_A3E1"

        BASE_DIR = (
            os.path.dirname(os.path.abspath(sys.executable))
            if getattr(sys, "frozen", False) else
            os.path.dirname(os.path.abspath(__file__))
        )
        def BAT(*p): return os.path.join(BASE_DIR, "scripts", *p)
        BAT_SPEEDTEST = BAT("netspeed_checker.bat")

        # układ siatki
        self.grid_columnconfigure(0, weight=0)  # etykiety
        self.grid_columnconfigure(1, weight=0)  # wartości rosną
        self.grid_columnconfigure(2, weight=0)  # przyciski
        self.grid_rowconfigure(1, weight=1)  # dystans/rozszerzanie

        # nagłówek przez 3 kolumny
        tk.Label(self, text="Internet Testing module",
                 font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=1, columnspan=20, pady=(10, 20), sticky="ew")

        # wiersz: SSID
        tk.Label(self, text="SSID:", font=("Segoe UI", 10, "bold")) \
            .grid(row=1, column=0, padx=(0, 10), sticky="ew")
        tk.Label(self, text=wifi_ssid, font=("Consolas", 12), fg="blue") \
            .grid(row=1, column=1, sticky="ew")

        # wiersz: Hasło + Copy
        tk.Label(self, text="Hasło:", font=("Segoe UI", 10, "bold")) \
            .grid(row=2, column=0, padx=(0, 10), sticky="ne")
        tk.Label(self, text=wifi_password, font=("Consolas", 11)) \
            .grid(row=2, column=1, sticky="w")
        ttk.Button(self, text="Copy",
                   command=lambda: self.copy_to_clipboard(wifi_password),
                   cursor="hand2") \
            .grid(row=2, column=2, padx=(10, 0), sticky="w")

        # przycisk SpeedTest na dole, wyrównany do lewej
        btn_speed = ttk.Button(self, text="SpeedTest", cursor="hand2")
        btn_speed.config(command=partial(self.run_bat_async, BAT_SPEEDTEST, "Speed test", btn_speed))
        btn_speed.grid(row=100, column=0, columnspan=3, pady=(20, 0), sticky="w")

    def copy_to_clipboard(self, text: str):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        messagebox.showinfo("Clipboard", "Wifi Password Copied!", parent=self)

    def run_bat_async(self, bat_path: str, title: str, btn: ttk.Button):
        btn.config(state="disabled")
        self.config(cursor="watch")
        self.update_idletasks()

        def worker():
            try:
                result = Runner(bat_path).prepare_and_run()
            except Exception as e:
                self.after(0, lambda: (
                    btn.config(state="normal"),
                    self.config(cursor=""),
                    messagebox.showerror(title, str(e), parent=self)
                ))
                return

            def on_done():
                btn.config(state="normal")
                self.config(cursor="")
                if getattr(result, "returncode", 1) == 0:
                    messagebox.showinfo(title, "Script executed correct!", parent=self)
                else:
                    messagebox.showwarning(title, "Script executed incorrect! Something goes wrong!", parent=self)

            self.after(0, on_done)

        threading.Thread(target=worker, daemon=True).start()
