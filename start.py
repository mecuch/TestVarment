import tkinter as tk

class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Welcome!",
                 font=("Eras Bold ITC", 18, "bold")) \
            .grid(row=0, column=1, pady=(10, 20), sticky="n")