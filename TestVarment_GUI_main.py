import tkinter as tk
from tkinter import messagebox
from camera_prev import CameraPage
from sound import SoundPage
from internet import InternetPage
from keybtouch import KeyboardTester

# --- Aplikacja ---
root = tk.Tk()
root.title("TestVarment v0.2")

# --- wymiary okna ---
window_width = 1100
window_height = 350

# --- wymiary ekranu ---
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# --- pozycja startowa ---
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# --- ustawienie ---
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.minsize(480, 700)

# === MENU (belka górna) ===
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu2 = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
file_menu2.add_command(label="Credits", command=lambda: messagebox.showinfo("About this project", f"TestVarment v0.2 created by Marcin 'Mecuch' Pecuch, 2025", parent=root))
menubar.add_cascade(label="Settings", menu=file_menu)
menubar.add_cascade(label="About", menu=file_menu2)
root.config(menu=menubar)

# Siatka główna: menu u góry, content poniżej (rozciąga się)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# --- Pasek menu (3 przyciski) ---
menu_frame = tk.Frame(root, padx=10, pady=10)
menu_frame.grid(row=0, column=0, sticky="ew")
menu_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)  # równe kolumny

# --- Kontener na ekrany ---
content = tk.Frame(root, padx=16, pady=16)
content.grid(row=1, column=0, sticky="nsew")
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)

# --- Poszczególne ekrany (ramki) ---
page_basic = tk.Frame(content)
page_internet = InternetPage(content)
page_sound = SoundPage(content)
page_camera = CameraPage(content)
page_keybtouch = KeyboardTester(content)

for page in (page_basic, page_internet, page_sound, page_camera, page_keybtouch):
    page.grid(row=0, column=0, sticky="nsew")

# Zawartość: Basic Configuration
lbl_basic = tk.Label(page_basic, text="Basic Configuration", font=("Eras Bold ITC", 18, "bold"))
lbl_basic.pack(expand=True)


# --- Logika przełączania ekranów ---
def show_page(page: tk.Frame):
    page.tkraise()

# --- Przyciski menu ---
btn_testenv = tk.Button(menu_frame, text="Test Environment",command=lambda: show_page(page_basic))
btn_net = tk.Button(menu_frame, text="Internet", command=lambda: show_page(page_internet))
btn_sound = tk.Button(menu_frame, text="Sound", command=lambda: show_page(page_sound))
btn_camera = tk.Button(menu_frame, text="Camera", command=lambda: show_page(page_camera))
btn_keybtouch = tk.Button(menu_frame, text="Keyboard", command=lambda: show_page(page_keybtouch))
btn_others = tk.Button(menu_frame, text="Others")


btn_testenv.grid(row=0, column=0, sticky="ew", padx=4)
btn_net.grid(row=0, column=1, sticky="ew", padx=4)
btn_sound.grid(row=0, column=2, sticky="ew", padx=4)
btn_camera.grid(row=0, column=3, sticky="ew", padx=4)
btn_keybtouch.grid(row=0, column=4, sticky="ew", padx=4)
btn_others.grid(row=0, column=5, sticky="ew", padx=4)

# Startujemy od ekranu „Basic Configuration”
show_page(page_basic)

root.mainloop()