import tkinter as tk

class EnvironmentWizard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # nagłówek
        tk.Label(self, text="Test Environment Wizard",
                 font=("Eras Bold ITC", 18, "bold")) \
            .grid(row=0, column=1, pady=(10, 20), sticky="n")