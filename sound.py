import tkinter as tk
from tkinter import ttk, messagebox
import winsound, pathlib

class SoundPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Sound testing module", font=("Segoe UI", 18, "bold")).pack(pady=20)

        # przyciski
        ttk.Button(self, text="Test dźwięku", command=self.play_test).pack(pady=8)
        ttk.Button(self, text="Stop", command=self.stop_sound).pack(pady=8)

    def play_test(self):
        path = pathlib.Path(__file__).with_name("test_sound.wav")
        if not path.exists():
            messagebox.showerror("Błąd", f"Brak pliku: {path.name}", parent=self)
            return

        # odtwarzanie w tle (asynchronicznie)
        winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)

    def stop_sound(self):
        # zatrzymanie dźwięku
        winsound.PlaySound(None, winsound.SND_PURGE)
