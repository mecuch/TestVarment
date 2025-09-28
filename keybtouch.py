import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class KeyboardTester(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._btns, self._btn_bg = {}, {}
        self._pressed_once = set()
        self._aliases = {"PrintScreen":"Print", "Sys_Req":"Print"}
        self._count_var = tk.StringVar(value="0/0")

        # ścieżka logu na Pulpit
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop, exist_ok=True)
        self._log_path = os.path.join(desktop, "keyboard_log.txt")

        self._make_ui()
        self._bind_events()
        self._init_logfile()

    # ==== UI ====
    def _make_ui(self):
        top = ttk.Frame(self); top.pack(fill="x", padx=10, pady=10)
        ttk.Label(top, text="Tester klawiatury", font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Label(top, textvariable=self._count_var, font=("Segoe UI", 12)).pack(side="left", padx=12)
        ttk.Button(top, text="Wyczyść log", command=self.clear_logs).pack(side="right")

        mid = ttk.Frame(self); mid.pack(fill="both", expand=True, padx=10)
        right = ttk.Frame(self); right.pack(fill="both", expand=True, padx=10, pady=(8,10))
        self.log_list = tk.Listbox(right, height=8); self.log_list.pack(fill="both", expand=True)
        ttk.Label(self, text="Kliknij w obszar i wciskaj klawisze.", foreground="#666").pack(pady=(6,8))

        rows = [
            [("Esc","Escape"),("F1","F1"),("F2","F2"),("F3","F3"),("F4","F4"),("F5","F5"),
             ("F6","F6"),("F7","F7"),("F8","F8"),("F9","F9"),("F10","F10"),("F11","F11"),
             ("F12","F12"),("PrtSc","Print"),("ScrLk","Scroll_Lock"),("Pause","Pause")],
            [("`","grave"),("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),
             ("7","7"),("8","8"),("9","9"),("0","0"),("-","minus"),("=","equal"),
             ("Backspace","BackSpace")],
            [("Tab","Tab"),("Q","q"),("W","w"),("E","e"),("R","r"),("T","t"),("Y","y"),
             ("U","u"),("I","i"),("O","o"),("P","p"),("[","bracketleft"),
             ("]","bracketright"),("\\","backslash")],
            [("Caps","Caps_Lock"),("A","a"),("S","s"),("D","d"),("F","f"),("G","g"),
             ("H","h"),("J","j"),("K","k"),("L","l"),(";","semicolon"),
             ("'","apostrophe"),("Enter","Return")],
            [("Shift","Shift_L"),("Z","z"),("X","x"),("C","c"),("V","v"),("B","b"),
             ("N","n"),("M","m"),(",","comma"),(".","period"),("/","slash"),
             ("Shift","Shift_R")],
            [("Ctrl","Control_L"),("Win","Super_L"),("Alt","Alt_L"),("Space","space"),
             ("Alt","Alt_R"),("Menu","Menu"),("Ctrl","Control_R")]
        ]
        kb = ttk.Frame(mid); kb.pack(side="left", anchor="n")
        special = {"BackSpace":10,"Tab":7,"Caps_Lock":8,"Return":10,"Shift_L":10,"Shift_R":12,
                   "space":30,"Control_L":7,"Control_R":7,"Super_L":7,"Alt_L":6,"Alt_R":6,"Menu":6}
        for r,row in enumerate(rows):
            rf = ttk.Frame(kb); rf.grid(row=r, column=0, sticky="w", pady=2)
            for c,(lab,ks) in enumerate(row):
                w = special.get(ks,5)
                b = tk.Button(rf, text=lab, width=w); b.grid(row=0,column=c,padx=2)
                self._btns[ks]=b; self._btn_bg[ks]=b.cget("bg")

        # NumPad
        np = ttk.LabelFrame(mid, text="NumPad"); np.pack(side="left", padx=(16,0), anchor="n")
        def add(r,c,ks,lab,span=1,w=5):
            b=tk.Button(np,text=lab,width=w); b.grid(row=r,column=c,padx=2,pady=2,columnspan=span,sticky="we")
            self._btns[ks]=b; self._btn_bg[ks]=b.cget("bg")
        add(0,0,"Num_Lock","NumLoc"); add(0,1,"KP_Divide","/"); add(0,2,"KP_Multiply","*"); add(0,3,"KP_Subtract","-")
        add(1,0,"KP_7","7"); add(1,1,"KP_8","8"); add(1,2,"KP_9","9"); add(1,3,"KP_Add","+")
        add(2,0,"KP_4","4"); add(2,1,"KP_5","5"); add(2,2,"KP_6","6"); add(2,3,"KP_Add","+")
        add(3,0,"KP_1","1"); add(3,1,"KP_2","2"); add(3,2,"KP_3","3"); add(3,3,"KP_Enter","Enter",w=5)
        add(4,0,"KP_0","0",span=2,w=12); add(4,2,"KP_Decimal",".")

        self._update_counter()

        # fokus-proxy 1×1
        self._proxy = tk.Canvas(self, width=1, height=1, highlightthickness=0, takefocus=1)
        self._proxy.place(x=0, y=0, width=1, height=1)
        self._proxy.focus_set()

    # ==== BINDY ====
    def _bind_events(self):
        self.bind_all("<KeyPress>", self._on_press_all, add="+")
        self.bind_all("<Button-1>", lambda e: self._proxy.focus_set(), add="+")
        for seq in ("<KeyPress-Tab>", "<KeyPress-ISO_Left_Tab>", "<KeyPress-Print>", "<KeyPress-Menu>"):
            self._proxy.bind(seq, self._on_press_proxy, add="+")

    # ==== LOG PLIK ====
    def _init_logfile(self):
        if not os.path.exists(self._log_path):
            with open(self._log_path, "w", encoding="utf-8") as f:
                f.write("Keyboard log\n")
        # separator sesji
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

    # globalny fallback
    def _on_press_all(self, e):
        ks = self._canonical(e)
        self._hit(ks); self._log(ks)

    # uprzywilejowane
    def _on_press_proxy(self, e):
        ks = self._canonical(e)
        self._hit(ks); self._log(ks)
        return "break"

    # ==== MAPOWANIE ====
    def _canonical(self, e):
        ks = e.keysym; kc = e.keycode
        kc_map = {
            96:"KP_0",97:"KP_1",98:"KP_2",99:"KP_3",100:"KP_4",101:"KP_5",
            102:"KP_6",103:"KP_7",104:"KP_8",105:"KP_9",
            106:"KP_Multiply",107:"KP_Add",109:"KP_Subtract",110:"KP_Decimal",111:"KP_Divide"
        }
        if kc in kc_map: return kc_map[kc]
        if ks=="Return" and kc in (108,335): return "KP_Enter"
        if kc==44: return "Print"  # PrintScreen
        nav={"End":"KP_1","Down":"KP_2","Next":"KP_3","Left":"KP_4","Begin":"KP_5",
             "Right":"KP_6","Home":"KP_7","Up":"KP_8","Prior":"KP_9",
             "Insert":"KP_0","Delete":"KP_Decimal","Page_Up":"KP_9","Page_Down":"KP_3"}
        if ks in nav: return nav[ks]
        return self._aliases.get(ks, ks)

    # ==== POMOCNICZE ====
    def _hit(self, ks):
        b = self._btns.get(ks)
        if b:
            if ks not in self._pressed_once:
                self._pressed_once.add(ks); self._update_counter()
            b.configure(bg="lightgreen", relief="sunken")

    def _update_counter(self):
        self._count_var.set(f"{len(self._pressed_once)}/{len(self._btns)}")

    def _log(self, ks):
        t = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        line = f"[{t}] wciśnięto: {ks}"
        self.log_list.insert("end", line)
        self.log_list.see("end")
        # dopisz do pliku
        try:
            with open(self._log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass  # celowo cicho, GUI ma działać dalej

    # API
    def get_logs(self):
        return [self.log_list.get(i) for i in range(self.log_list.size())]

    def clear_logs(self):
        # wyczyść listę
        self.log_list.delete(0, "end")
        # resetuj stan klawiszy
        for ks, b in self._btns.items():
            b.configure(bg=self._btn_bg[ks], relief="raised")
        self._pressed_once.clear()
        self._update_counter()
