import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ScriptRunner import Runner
from utils import partition_count, yt_usability, yt_batt

# === ŚCIEŻKI BAZOWE ===
BASE_DIR = (
    os.path.dirname(os.path.abspath(sys.executable))
    if getattr(sys, "frozen", False) else
    os.path.dirname(os.path.abspath(__file__))
)

IMG = lambda *p: os.path.join(BASE_DIR, "img", *p)
BAT = lambda *p: os.path.join(BASE_DIR, "scripts", *p)
REP = lambda *p: os.path.join(BASE_DIR, "repository", *p)

# === GŁÓWNE OKNO + WYŚRODKOWANIE ===
root = tk.Tk()
root.title("TestVarment v0.1")

window_width = 440
window_height = 630
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# === MENU (belka górna) ===
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu2 = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
file_menu2.add_command(label="Credits", command=lambda: messagebox.showinfo("About this project", f"TestVarment v0.1 created by Marcin 'Mecuch' Pecuch, 2025", parent=root))
menubar.add_cascade(label="Settings", menu=file_menu)
menubar.add_cascade(label="About", menu=file_menu2)
root.config(menu=menubar)

# Siatka dla root
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# === RAMKI ===
frame_top = tk.Frame(root)
frame_top.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

frame_middle1 = tk.Frame(root)
frame_middle1.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))

frame_middle2 = tk.Frame(root)
frame_middle2.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 5))

frame_bottom = tk.Frame(root)
frame_bottom.grid(row=3, column=0, padx=1, pady=(1, 2))

frame_top.grid_rowconfigure(0, weight=1)
frame_top.grid_columnconfigure(0, weight=1)

frame_middle2.grid_rowconfigure(0, weight=1)
frame_middle2.grid_columnconfigure(0, weight=1)
for r in (0, 1, 2, 3):
    root.grid_rowconfigure(r, weight=1)

# === OBRAZY (wczytanie) ===
img_logo   = ImageTk.PhotoImage(Image.open(IMG("logo.png")).resize((150, 100)))
img_label1 = ImageTk.PhotoImage(Image.open(IMG("label1.png")).resize((120, 50)))
img_label2 = ImageTk.PhotoImage(Image.open(IMG("label2.png")).resize((120, 50)))
img_serial = ImageTk.PhotoImage(Image.open(IMG("serial.png")).resize((120, 50)))
img_winkey = ImageTk.PhotoImage(Image.open(IMG("winkey.png")).resize((120, 50)))
img_spd    = ImageTk.PhotoImage(Image.open(IMG("spdtest.png")).resize((120, 50)))
img_install= ImageTk.PhotoImage(Image.open(IMG("install.png")).resize((120, 50)))
img_delete = ImageTk.PhotoImage(Image.open(IMG("delete.png")).resize((120, 50)))
img_part   = ImageTk.PhotoImage(Image.open(IMG("partition.png")).resize((120, 50)))
img_partstat = ImageTk.PhotoImage(Image.open(IMG("partstat.png")).resize((120, 50)))
img_deskicon = ImageTk.PhotoImage(Image.open(IMG("deskicon.png")).resize((390, 50)))
img_label3 = ImageTk.PhotoImage(Image.open(IMG("label3.png")).resize((120, 50)))
img_ytbat = ImageTk.PhotoImage(Image.open(IMG("yt_batt.png")).resize((120, 50)))
img_ytuser = ImageTk.PhotoImage(Image.open(IMG("yt_user.png")).resize((120, 50)))

# === LOGO ===
logo_label = tk.Label(frame_top, image=img_logo); logo_label.image = img_logo
logo_label.grid(row=0, column=0, sticky="n", pady=10)

# === HELPER: uruchamianie BAT + komunikat ===
def run_bat_async(bat_path: str, title: str, btn: tk.Button):
    """Uruchamia .bat w wątku, nie blokując tkintera."""
    # zasygnalizuj zajętość
    btn.config(state="disabled")
    root.config(cursor="watch")
    root.update_idletasks()

    def worker():
        try:
            result = Runner(bat_path).prepare_and_run()
        except Exception as e:
            # wróć do wątku GUI z komunikatem o błędzie
            root.after(0, lambda: (
                btn.config(state="normal"),
                root.config(cursor=""),
                messagebox.showerror(title, str(e))
            ))
            return

        def on_done():
            btn.config(state="normal")
            root.config(cursor="")

            if result.returncode == 0:
                msg = "Script executed correct!"
                show = messagebox.showinfo
            else:
                msg = "Script executed incorrect! Something goes wrong!"
                show = messagebox.showwarning

            show(title, msg)

        root.after(0, on_done)

    threading.Thread(target=worker, daemon=True).start()
# === POZOSTAŁE FUNKCJE ===

def copy_to_clipboard(text: str):
    frame_middle1.clipboard_clear()
    frame_middle1.clipboard_append(text)
    frame_middle1.update()
    messagebox.showinfo("Clipboard", f"Wifi Password Copied!")

# === ŚRODKOWA RAMKA1 - ZAWARTOŚĆ ===
wifi_password = "wfx%$YEy#7vV"
wifi_ssid = "PLAY_Swiatlowodowy_A3E1"

wifi_ssid_label = tk.Label(frame_middle1, text=wifi_ssid, font=("Consolas", 12), fg="blue")
wifi_ssid_label.grid(row=0, column=0, padx=10, pady=10)

pasw_lbl = tk.Label(frame_middle1, text=wifi_password, font=("Consolas", 10), fg="black")
pasw_lbl.grid(row=0, column=1, padx=10, pady=10)

btn = tk.Button(frame_middle1, text="Copy", command=lambda: copy_to_clipboard(wifi_password), relief="groove", cursor="hand2")
btn.grid(row=0, column=2, padx=10, pady=10)

# === MAPOWANIE PRZYCISKÓW → .BAT (zmień pod swoje nazwy) ===
BAT_SERIAL     = BAT("serial_checker.bat")
BAT_WINKEY     = BAT("winserial_checker.bat")
BAT_SPEEDTEST  = BAT("netspeed_checker.bat")
BAT_DISKSHRINK = BAT("ssd_shrink.bat")
BAT_INSTALL    = BAT("test_env_install.bat")
BAT_UNINSTALL  = BAT("test_env_uninstall.bat")
BAT_ICONSETTER = BAT("deskticon_setter.bat")

# === PRZYCISKI (ikony) DOLNA RAMKA ===
#
btn1 = tk.Button(frame_bottom, image=img_serial, relief="groove", cursor="hand2")
btn1.config(command=lambda b=btn1: run_bat_async(BAT_SERIAL, "Serial checker", b))
btn1.grid(row=0, column=0, padx=5, pady=50)
#
btn2 = tk.Button(frame_bottom, image=img_winkey, relief="groove", cursor="hand2")
btn2.config(command=lambda b=btn2: run_bat_async(BAT_WINKEY, "WinKey / Icons", b))
btn2.grid(row=0, column=1, padx=5, pady=50, sticky="ew")
#
btn3 = tk.Button(frame_bottom, image=img_spd, relief="groove", cursor="hand2")
btn3.config(command=lambda b=btn3: run_bat_async(BAT_SPEEDTEST, "Speed test", b))
btn3.grid(row=0, column=2, padx=5, pady=50, sticky="ew")

lab1_label = tk.Label(frame_bottom, image=img_label1); lab1_label.image = img_label1
lab1_label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

lab2_label = tk.Label(frame_bottom, image=img_label2); lab2_label.image = img_label2
lab2_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

btn4 = tk.Button(frame_bottom, image=img_install, relief="groove", cursor="hand2")
btn4.config(command=lambda b=btn4: run_bat_async(BAT_INSTALL, "Install env", b))
btn4.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

btn5 = tk.Button(frame_bottom, image=img_delete, relief="groove", cursor="hand2")
btn5.config(command=lambda b=btn5: run_bat_async(BAT_UNINSTALL, "Uninstall env", b))
btn5.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

btn6 = tk.Button(frame_bottom, image=img_part, relief="groove", cursor="hand2")
btn6.config(command=lambda b=btn6: run_bat_async(BAT_DISKSHRINK, "Partition", b))
btn6.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

btn7 = tk.Button(frame_bottom, image=img_partstat, command=lambda: messagebox.showinfo("Partition Status", partition_count(0)), relief="ridge", cursor="hand2")
btn7.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn8 = tk.Button(frame_middle2, image=img_deskicon, relief="groove", cursor="hand2")
btn8.config(command=lambda b=btn8: run_bat_async(BAT_ICONSETTER, "Desktop Icon Setter", b))
btn8.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lab3_label = tk.Label(frame_bottom, image=img_label3); lab3_label.image = img_label3
lab3_label.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

btn9 = tk.Button(frame_bottom, image=img_ytbat, command=lambda: yt_batt(), relief="groove", cursor="hand2")
btn9.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

btn10 = tk.Button(frame_bottom, image=img_ytuser, command=lambda: yt_usability(), relief="groove", cursor="hand2")
btn10.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

# === START ===
root.mainloop()
