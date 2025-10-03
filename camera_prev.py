import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

# mikr. opcjonalnie (pip install sounddevice numpy)
try:
    import sounddevice as sd
    import numpy as np
except Exception:
    sd = None
    np = None

class CameraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cap = None
        self.running_cam = False
        self.running_mic = False
        self.last_level = 0.0

        self.MAX_W, self.MAX_H = 320, 240

        # siatka 2 kolumny: [preview] | [panel przycisków]
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)  # wypełniacz pod spodem

        tk.Label(self, text="Camera & Microphone test", font=("Segoe UI", 18, "bold"))\
            .grid(row=0, column=0, columnspan=2, pady=(10, 10), sticky="n")

        # podgląd z placeholderem
        self.placeholder = ImageTk.PhotoImage(Image.new("RGB", (self.MAX_W, self.MAX_H), (235, 235, 235)))
        self.lbl_preview = tk.Label(self, image=self.placeholder, bd=2, relief="sunken")
        self.lbl_preview.grid(row=1, column=0, padx=12, pady=8, sticky="n")

        # panel przycisków po prawej
        panel = ttk.Frame(self)
        panel.grid(row=1, column=1, padx=(6, 12), pady=8, sticky="n")
        self.btn_cam = ttk.Button(panel, text="Włącz kamerę", command=self.toggle_camera)
        self.btn_cam.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.btn_mic = ttk.Button(panel, text="Włącz mikrofon", command=self.toggle_mic)
        self.btn_mic.grid(row=1, column=0, sticky="ew")

        # wskaźnik aktywności mikrofonu pod przyciskami
        self.mic_canvas = tk.Canvas(self, width=60, height=60, highlightthickness=0)
        self.mic_canvas.grid(row=2, column=1, pady=(12, 12), sticky="n")
        self.mic_dot = self.mic_canvas.create_oval(10, 10, 50, 50, fill="#999", outline="")

        self.bind("<Destroy>", self._on_destroy)

        # pętla odświeżania UI wskaźnika
        self.after(100, self._update_mic_indicator)

    # --- kamera ---
    def start_camera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap or not self.cap.isOpened():
            self.cap = None
            return
        self.running_cam = True
        self.btn_cam.config(text="Wyłącz kamerę")
        self._update_frame()

    def stop_camera(self):
        self.running_cam = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.btn_cam.config(text="Włącz kamerę")
        self.lbl_preview.config(image=self.placeholder)
        self.lbl_preview.imgtk = None

    def toggle_camera(self):
        self.stop_camera() if self.running_cam else self.start_camera()

    def _update_frame(self):
        if self.running_cam and self.cap:
            ok, frame = self.cap.read()
            if ok:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = frame.shape[:2]
                scale = min(self.MAX_W / w, self.MAX_H / h)
                nw, nh = int(w * scale), int(h * scale)
                frame = cv2.resize(frame, (nw, nh), interpolation=cv2.INTER_AREA)
                bg = Image.new("RGB", (self.MAX_W, self.MAX_H), (235, 235, 235))
                img = Image.fromarray(frame)
                x = (self.MAX_W - nw) // 2
                y = (self.MAX_H - nh) // 2
                bg.paste(img, (x, y))
                imgtk = ImageTk.PhotoImage(bg, master=self)
                self.lbl_preview.imgtk = imgtk
                self.lbl_preview.config(image=imgtk)
            self.after(20, self._update_frame)

    # --- mikrofon ---
    def start_mic(self):
        if sd is None or np is None:
            self.btn_mic.config(text="Włącz mikrofon")
            messagebox = tk.messagebox if hasattr(tk, "messagebox") else __import__("tkinter.messagebox").messagebox
            messagebox.showwarning("Audio", "Brak pakietu 'sounddevice' lub 'numpy'.", parent=self)
            return
        try:
            self.running_mic = True
            self.btn_mic.config(text="Wyłącz mikrofon")
            # strumień wejściowy, mono, mała ramka
            self.stream = sd.InputStream(callback=self._mic_callback, channels=1, samplerate=16000, blocksize=512)
            self.stream.start()
        except Exception as e:
            self.running_mic = False
            self.btn_mic.config(text="Włącz mikrofon")
            messagebox = tk.messagebox if hasattr(tk, "messagebox") else __import__("tkinter.messagebox").messagebox
            messagebox.showerror("Audio", str(e), parent=self)

    def stop_mic(self):
        self.running_mic = False
        try:
            if hasattr(self, "stream") and self.stream:
                self.stream.stop()
                self.stream.close()
        except Exception:
            pass
        self.btn_mic.config(text="Włącz mikrofon")
        self.last_level = 0.0  # zgaś wskaźnik

    def toggle_mic(self):
        self.stop_mic() if self.running_mic else self.start_mic()

    def _mic_callback(self, indata, frames, time, status):
        if status:
            return
        # RMS → poziom 0..1
        rms = float(np.sqrt(np.mean(indata**2)))
        # lekkie wygładzenie
        self.last_level = 0.8 * self.last_level + 0.2 * min(rms * 20.0, 1.0)

    def _update_mic_indicator(self):
        # promień i kolor zależne od poziomu
        lvl = self.last_level if self.running_mic else 0.0
        r = int(10 + 20 * lvl)  # 10..30
        cx, cy = 30, 30
        self.mic_canvas.coords(self.mic_dot, cx - r, cy - r, cx + r, cy + r)
        color = "#3cb371" if lvl > 0.2 else "#999999"
        self.mic_canvas.itemconfig(self.mic_dot, fill=color)
        self.after(60, self._update_mic_indicator)

    # --- sprzątanie ---
    def _on_destroy(self, _):
        self.stop_camera()
        self.stop_mic()
