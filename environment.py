import os
import sys
import threading
import tkinter as tk
from functools import partial
from tkinter import messagebox
from ScriptRunner import Runner
from PIL import ImageTk, Image
from styles import FramesTextStyle, FramesButtonsStyle

class EnvironmentWizard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        BASE_DIR = (
            os.path.dirname(os.path.abspath(sys.executable))
            if getattr(sys, "frozen", False) else
            os.path.dirname(os.path.abspath(__file__))
        )
        BAT =  lambda *p: os.path.join(BASE_DIR, "scripts", *p)
        IMG = lambda *p: os.path.join(BASE_DIR, "images", *p)

        BAT_SPEEDTEST = BAT("netspeed_checker.bat")

        self.preparation_logo = ImageTk.PhotoImage(
            Image.open(IMG("preparation.png")).resize((80, 80), Image.LANCZOS),
            master=self
        )
        self.installation_logo = ImageTk.PhotoImage(
            Image.open(IMG("installation.png")).resize((80, 80), Image.LANCZOS),
            master=self
        )

        # 5 kolumn: lewa, środek1, środek2, środek3, prawa
        self.grid_columnconfigure(0, weight=1)  # lewa pusta
        self.grid_columnconfigure(1, weight=0)  # środek1 (przycisk lewy)
        self.grid_columnconfigure(2, weight=0)  # środek2 (obrazek)
        self.grid_columnconfigure(3, weight=0)  # środek2 (przycisk prawy)
        self.grid_columnconfigure(4, weight=1)  # prawa pusta

        # nagłówek
        tk.Label(self, text="Test Environment Wizard",
                 font=FramesTextStyle.big_font) \
            .grid(row=0, column=2, pady=(10, 20), sticky="n")

        # ciało frame
        tk.Label(self, image=self.preparation_logo) \
            .grid(row=1, column=2, pady=(20, 30), sticky="n")

        # przycisk 1
        btn_part = tk.Button(self, text="Partition Status",
                             font=FramesButtonsStyle.font, cursor="hand2", relief="groove")
        btn_part.config(command=partial(self.run_bat_async, BAT_SPEEDTEST, "Speed test", btn_part))
        btn_part.grid(row=1, column=1, pady=(20, 20), sticky="ew")

        # przycisk 2
        btn_part = tk.Button(self, text="Partition Disk",
                             font=FramesButtonsStyle.font, cursor="hand2", relief="groove")
        btn_part.config(command=partial(self.run_bat_async, BAT_SPEEDTEST, "Speed test", btn_part))
        btn_part.grid(row=1, column=3, pady=(20, 20), sticky="ew")

        tk.Label(self, image=self.installation_logo) \
            .grid(row=2, column=2, pady=(20, 30), sticky="n")

        # przycisk 3
        btn_part = tk.Button(self, text="Install Environment",
                             font=FramesButtonsStyle.font, cursor="hand2", relief="groove")
        btn_part.config(command=partial(self.run_bat_async, BAT_SPEEDTEST, "Speed test", btn_part))
        btn_part.grid(row=2, column=1, pady=(20, 20), sticky="ew")

        # przycisk 4
        btn_part = tk.Button(self, text="Uninstall Environment",
                             font=FramesButtonsStyle.font, cursor="hand2", relief="groove")
        btn_part.config(command=partial(self.run_bat_async, BAT_SPEEDTEST, "Speed test", btn_part))
        btn_part.grid(row=2, column=3, pady=(20, 20), sticky="ew")


    def run_bat_async(self, bat_path: str, title: str, btn: tk.Button):
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


