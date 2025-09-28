import os, sys, threading
import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from ScriptRunner import Runner
from styles import FramesTextStyle, FramesButtonsStyle

class InternetPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        wifi_password = "wfx%$YEy#7vV"
        wifi_ssid = "PLAY_Swiatlowodowy_A3E1"
        wifi_ssid5GHz = "PLAY_Swiatlowodowy_A3E1_5G"

        BASE_DIR = (
            os.path.dirname(os.path.abspath(sys.executable))
            if getattr(sys, "frozen", False) else
            os.path.dirname(os.path.abspath(__file__))
        )
        def BAT(*p): return os.path.join(BASE_DIR, "scripts", *p)
        BAT_SPEEDTEST = BAT("netspeed_checker.bat")

        # 3 kolumny: lewa, środek, prawa
        self.grid_columnconfigure(0, weight=1)  # lewa pusta
        self.grid_columnconfigure(1, weight=0)  # środek (treść)
        self.grid_columnconfigure(2, weight=1)  # prawa pusta

        # nagłówek
        tk.Label(self, text="Internet Testing module",
                 font=("Eras Bold ITC", 18, "bold")) \
            .grid(row=0, column=1, pady=(10, 20), sticky="n")

        # SSID
        frame_ssid = ttk.Frame(self)
        frame_ssid.grid(row=2, column=1, pady=5)
        frame_ssid.grid_columnconfigure(0, weight=0)
        frame_ssid.grid_columnconfigure(1, weight=1)

        tk.Label(frame_ssid, text="SSID (2.4 GHz):", font=FramesTextStyle.font) \
            .grid(row=0, column=0, padx=(0, 8), sticky="w")
        tk.Label(frame_ssid, text=wifi_ssid, font=("Consolas", 12), fg=FramesTextStyle.fg_pswd) \
            .grid(row=0, column=1, sticky="w")

        tk.Label(frame_ssid, text="SSID (5.0 GHz):", font=FramesTextStyle.font) \
            .grid(row=1, column=0, padx=(0, 8), sticky="w")
        tk.Label(frame_ssid, text=wifi_ssid5GHz, font=("Consolas", 12), fg=FramesTextStyle.fg_pswd) \
            .grid(row=1, column=1, sticky="w")

        # Hasło + Copy
        frame_pw = ttk.Frame(self)
        frame_pw.grid(row=3, column=1, pady=5)
        tk.Label(frame_pw, text="Hasło:", font=FramesTextStyle.font).pack(side="left", padx=(0, 8))
        tk.Label(frame_pw, text=wifi_password, font=("Consolas", 11)).pack(side="left")
        tk.Button(frame_pw, text="Copy",
                  command=lambda: self.copy_to_clipboard(wifi_password),
                  cursor="hand2", relief="groove", font=FramesButtonsStyle.font).pack(side="left", padx=8)

        # SpeedTest przycisk pod spodem
        btn_speed = tk.Button(self, text="Perform SpeedTest", font=FramesButtonsStyle.font, cursor="hand2", relief="groove")
        btn_speed.config(command=partial(self.run_bat_async, BAT_SPEEDTEST, "Speed test", btn_speed))
        btn_speed.grid(row=4, column=1, pady=(20, 0), sticky="n")

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
