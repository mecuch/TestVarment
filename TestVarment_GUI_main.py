import os
import sys
import tkinter as tk
from PIL import ImageTk, Image

import styles
from camera_prev import CameraPage
from sound import SoundPage
from internet import InternetPage
from styles import ButtonsMenuStyle, FramesFooterFontStyle
from others import OtherPage
from environment import EnvironmentWizard
from start import StartPage

# --- Aplikacja ---
root = tk.Tk()
root.title("TestVarment v0.2")

# --- wymiary okna ---
window_width = 1100
window_height = 630

# --- wymiary ekranu ---
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# --- pozycja startowa ---
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# --- ustawienie ---
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.minsize(1100, 630)

BASE_DIR = (
    os.path.dirname(os.path.abspath(sys.executable))
    if getattr(sys, "frozen", False) else
    os.path.dirname(os.path.abspath(__file__))
)

IMG = lambda *p: os.path.join(BASE_DIR, "images", *p)

# --- Wczytywanie obrazów ---
img_logo   = ImageTk.PhotoImage(Image.open(IMG("logo.png")).resize((1000, 100)))

"""# === MENU (belka górna) ===
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu2 = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
file_menu2.add_command(label="Credits", command=lambda: messagebox.showinfo("About this project", f"TestVarment v0.2 created by Marcin 'Mecuch' Pecuch, 2025", parent=root))
menubar.add_cascade(label="Settings", menu=file_menu)
menubar.add_cascade(label="About", menu=file_menu2)
root.config(menu=menubar)"""

# Siatka główna: menu u góry, content poniżej (rozciąga się)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)  # logo
root.grid_rowconfigure(1, weight=0)  # menu
root.grid_rowconfigure(2, weight=1)  # content (jedyny rozciągany)
root.grid_rowconfigure(3, weight=0)  # stopka

# --- Logo ---

logo_frame = tk.Frame(root, padx=10, pady=5)
logo_frame.grid(row=0, column=0, sticky="ew")
logo_label = tk.Label(logo_frame, image=img_logo); logo_label.image = img_logo
logo_label.grid(row=0, column=0, sticky="ew", pady=10)

# --- Pasek menu ---
menu_frame = tk.Frame(root, padx=10, pady=10)
menu_frame.grid(row=1, column=0, sticky="ew")
menu_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)  # równe kolumny

# --- Kontener na ekrany ---
content = tk.Frame(root, padx=16, pady=16)
content.grid(row=2, column=0, sticky="nsew")
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)

# --- Stopka ---
footer_frame = tk.Frame(root, padx=10, pady=6)
footer_frame.grid(row=3, column=0, sticky="ew")
footer_frame.grid_columnconfigure(0, weight=1)
author = tk.Label(footer_frame, font=styles.FramesFooterFontStyle, text="TestVarment v0.2 by Marcin 'Mecuch' Pecuch 2025", fg="#666")
author.grid(row=0, column=0, sticky="ew")

# --- Poszczególne ekrany (ramki) ---
page_start = StartPage(content)
page_testenv = EnvironmentWizard(content)
page_internet = InternetPage(content)
page_sound = SoundPage(content)
page_camera = CameraPage(content)
page_others = OtherPage(content)

for page in (page_start, page_testenv, page_internet, page_sound, page_camera, page_others):
    page.grid(row=0, column=0, sticky="nsew")


# --- Logika przełączania ekranów ---
def show_page(page: tk.Frame):
    page.tkraise()

# --- Przyciski menu ---
btn_start = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, text="START", font=ButtonsMenuStyle.font,
                        command=lambda: show_page(page_start), relief="groove")
btn_testenv = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, text="Test Environment", font=ButtonsMenuStyle.font,
                        command=lambda: show_page(page_testenv), relief="groove")
btn_net = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, text="Internet", font=ButtonsMenuStyle.font,
                    command=lambda: show_page(page_internet), relief="groove")
btn_sound = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, text="Sound", font=ButtonsMenuStyle.font,
                      command=lambda: show_page(page_sound), relief="groove")
btn_camera = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, text="Camera", font=ButtonsMenuStyle.font,
                       command=lambda: show_page(page_camera), relief="groove")
btn_others = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, font=ButtonsMenuStyle.font,
                       command=lambda: show_page(page_others), text="Others", relief="groove")
btn_exit = tk.Button(menu_frame, fg=ButtonsMenuStyle.fg, font=ButtonsMenuStyle.font,
                       command=lambda: root.quit(), text="Exit", relief="groove")

btn_start.grid(row=0, column=0, sticky="ew", padx=4)
btn_testenv.grid(row=0, column=1, sticky="ew", padx=4)
btn_net.grid(row=0, column=2, sticky="ew", padx=4)
btn_sound.grid(row=0, column=3, sticky="ew", padx=4)
btn_camera.grid(row=0, column=4, sticky="ew", padx=4)
btn_others.grid(row=0, column=5, sticky="ew", padx=4)
btn_exit.grid(row=0, column=6, sticky="ew", padx=4)

# Startujemy od ekranu „Basic Configuration”
show_page(page_start)

root.mainloop()