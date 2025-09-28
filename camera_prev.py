import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class CameraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cap = None
        self.running = False

        tk.Label(self, text="Camera testing module", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.label = tk.Label(self, text="Podgląd z kamery pojawi się tutaj")
        self.label.pack(padx=10, pady=10)

        self.btn = ttk.Button(self, text="Włącz kamerę", command=self.toggle_camera)
        self.btn.pack(pady=10)

        # sprzątanie przy zamknięciu strony/okna
        self.bind("<Destroy>", self._on_destroy)

    # --- API publiczne ---
    def start(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap or not self.cap.isOpened():
            self.cap = None
            self.label.config(text="Nie można otworzyć kamery")
            return
        self.running = True
        self.btn.config(text="Wyłącz kamerę")
        self._update()

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.btn.config(text="Włącz kamerę")
        self.label.config(image="", text="Podgląd zatrzymany")
        self.label.imgtk = None

    def toggle_camera(self):
        if self.running:
            self.stop()
        else:
            self.start()

    # --- wewnętrzne ---
    def _update(self):
        if self.running and self.cap:
            ok, frame = self.cap.read()
            if ok:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
                self.label.imgtk = imgtk
                self.label.config(image=imgtk, text="")
            self.after(20, self._update)

    def _on_destroy(self, _event):
        # bezpieczne zwolnienie zasobów przy niszczeniu widgetu
        if self.running or self.cap:
            self.stop()
