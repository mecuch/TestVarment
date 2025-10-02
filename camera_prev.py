import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class CameraPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cap = None
        self.running = False

        # docelowy rozmiar podglądu
        self.MAX_W, self.MAX_H = 320, 240

        tk.Label(self, text="Camera testing module", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.label = tk.Label(self, text="Podgląd z kamery pojawi się tutaj")
        self.label.pack(padx=10, pady=10)

        self.btn = ttk.Button(self, text="Włącz kamerę", command=self.toggle_camera)
        self.btn.pack(pady=10)

        self.bind("<Destroy>", self._on_destroy)

    # --- API publiczne ---
    def start(self):
        # na Windows często stabilniej z CAP_DSHOW
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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
                # BGR -> RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # skalowanie z zachowaniem proporcji do MAX_W x MAX_H
                h, w = frame.shape[:2]
                scale = min(self.MAX_W / w, self.MAX_H / h)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

                imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
                self.label.imgtk = imgtk
                self.label.config(image=imgtk, text="")
            self.after(20, self._update)

    def _on_destroy(self, _event):
        if self.running or self.cap:
            self.stop()
