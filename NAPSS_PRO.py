import tkinter as tk
import sympy as sp
import datetime
import ctypes

# ══════════════════════════════════════════════════════════════
#  SYMPY SETUP
# ══════════════════════════════════════════════════════════════
x = sp.Symbol('x')
h = sp.Symbol('h')
f = sp.Function('f')

FIRST_EQS = [
    (3*f(x) - 4*f(x-h) + f(x-2*h)) / (2*h),
    (f(x+h) - f(x-h)) / (2*h),
    (-3*f(x) + 4*f(x+h) - f(x+2*h)) / (2*h),
]
SECOND_EQS = [
    (2*f(x) - 5*f(x-h) + 4*f(x-2*h) - f(x-3*h)) / h**2,
    (f(x+h) + f(x-h) - 2*f(x)) / h**2,
    (2*f(x) - 5*f(x+h) + 4*f(x+2*h) - f(x+3*h)) / h**2,
]

FIELD_MAP = {
    (0, 0): ["f(x)", "f(x-h)", "f(x-2h)"],
    (0, 1): ["f(x+h)", "f(x-h)"],
    (0, 2): ["f(x)", "f(x+h)", "f(x+2h)"],
    (1, 0): ["f(x)", "f(x-h)", "f(x-2h)", "f(x-3h)"],
    (1, 1): ["f(x)", "f(x+h)", "f(x-h)"],
    (1, 2): ["f(x)", "f(x+h)", "f(x+2h)", "f(x+3h)"],
}

SYMPY_KEY = {
    "f(x)":    lambda: f(x),
    "f(x+h)":  lambda: f(x+h),
    "f(x-h)":  lambda: f(x-h),
    "f(x+2h)": lambda: f(x+2*h),
    "f(x-2h)": lambda: f(x-2*h),
    "f(x+3h)": lambda: f(x+3*h),
    "f(x-3h)": lambda: f(x-3*h),
}

# ══════════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ══════════════════════════════════════════════════════════════
C = {
    "bg":      "#080810",
    "surface": "#0e0e1c",
    "card":    "#12121f",
    "card2":   "#16162a",
    "border":  "#1e1e36",
    "border2": "#2a2a4a",
    "cyan":    "#00d4ff",
    "purple":  "#a259ff",
    "green":   "#00ff9d",
    "yellow":  "#ffd166",
    "red":     "#ff4d6d",
    "text":    "#dde1f0",
    "text2":   "#8890b0",
    "text3":   "#4a4f70",
    "white":   "#ffffff",
}

EQ_NAMES   = ["Backward", "Central", "Forward"]
EQ_COLORS  = [C["green"], C["cyan"], C["purple"]]
EQ_FORMULAS = {
    (0,0): "f'(x) = [3f(x) - 4f(x-h) + f(x-2h)] / 2h",
    (0,1): "f'(x) = [f(x+h) - f(x-h)] / 2h",
    (0,2): "f'(x) = [-3f(x) + 4f(x+h) - f(x+2h)] / 2h",
    (1,0): "f''(x) = [2f(x) - 5f(x-h) + 4f(x-2h) - f(x-3h)] / h²",
    (1,1): "f''(x) = [f(x+h) - 2f(x) + f(x-h)] / h²",
    (1,2): "f''(x) = [2f(x) - 5f(x+h) + 4f(x+2h) - f(x+3h)] / h²",
}

# ══════════════════════════════════════════════════════════════
#  CUSTOM WIDGETS
# ══════════════════════════════════════════════════════════════
class NeonEntry(tk.Frame):
    def __init__(self, master, textvariable=None, width=9, accent=C["cyan"], **kw):
        super().__init__(master, bg=C["border"], padx=1, pady=1)
        self._accent = accent
        self._idle   = C["border"]
        inner = tk.Frame(self, bg=C["card2"])
        inner.pack(fill="both", expand=True)
        self.var = textvariable or tk.StringVar()
        self._e  = tk.Entry(inner, textvariable=self.var,
                            width=width, bg=C["card2"], fg=accent,
                            insertbackground=accent, relief="flat",
                            font=("Consolas", 11))
        self._e.pack(padx=4, pady=4)
        self._e.bind("<FocusIn>",  lambda e: self.config(bg=self._accent))
        self._e.bind("<FocusOut>", lambda e: self.config(bg=self._idle))

    def get(self):  return self.var.get()
    def set(self, v): self.var.set(v)


class SegmentedControl(tk.Frame):
    def __init__(self, master, options, colors, variable, command=None, **kw):
        super().__init__(master, bg=C["surface"],
                         highlightthickness=1, highlightbackground=C["border2"])
        self._var     = variable
        self._command = command
        self._btns    = []
        for i, (opt, col) in enumerate(zip(options, colors)):
            btn = tk.Label(self, text=opt, font=("Consolas", 10, "bold"),
                           fg=C["text3"], bg=C["surface"],
                           padx=16, pady=7, cursor="hand2")
            btn.grid(row=0, column=i, padx=(1 if i else 0))
            btn.bind("<Button-1>", lambda e, idx=i, c=col: self._select(idx, c, fire=True))
            self._btns.append((btn, col))
        init = variable.get()
        self._select(init, colors[init], fire=False)

    def _select(self, idx, col, fire=True):
        self._var.set(idx)
        for i, (btn, c) in enumerate(self._btns):
            btn.config(fg=c if i == idx else C["text3"],
                       bg=C["card2"] if i == idx else C["surface"])
        if fire and self._command:
            self._command()

# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════
class NAPSS(tk.Tk):
    def __init__(self):
        try:
            myappid = 'mycompany.napss.solver.v2'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        super().__init__()
        self.title("NAPSS  ·  Numerical Analysis Problem Solver")
        
        try:
            self.iconbitmap("app_icon.ico")
        except Exception:
            pass  

        self.configure(bg=C["bg"])
        self.resizable(False, False)
        W, H = 960, 710
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

        self._order      = tk.IntVar(value=0)  # 0: First, 1: Second
        self._eq_idx     = tk.IntVar(value=0)  # 0: Backward, 1: Central, 2: Forward
        self._xvar       = tk.StringVar()
        self._hvar       = tk.StringVar()
        self._result_var = tk.StringVar(value="—")
        self._status_var = tk.StringVar(value="Ready  ·  Select order and equation to begin.")
        self._history    = []
        self._f_entries  = {}
        self._fval_card  = None
        self._fval_outer = None
        self._hist_lbl   = None
        self._status_lbl = None
        self._formula_lbl = None
        self._clock_lbl   = None

        self._build_header()
        self._build_statusbar()  # يتم بناء وعرض شريط الحالة أولاً ليكون مثبتاً في القاع ثابت الموضِع
        self._build_body()
        
        self._on_change()

    def _build_header(self):
        hdr = tk.Frame(self, bg=C["surface"], height=78)
        hdr.pack(side="top", fill="x")
        hdr.pack_propagate(False)

        logo_blk = tk.Frame(hdr, bg=C["surface"])
        logo_blk.pack(side="left", padx=24)

        logo_row = tk.Frame(logo_blk, bg=C["surface"])
        logo_row.pack(anchor="w", pady=(10,0))

        for letter, col in zip("NAPSS", [C["cyan"], C["purple"], C["green"], C["yellow"], C["cyan"]]):
            tk.Label(logo_row, text=letter, fg=col, bg=C["surface"],
                     font=("Consolas", 20, "bold")).pack(side="left")

        tk.Label(logo_blk, text="Numerical Analysis Problem Solver System",
                 fg=C["text3"], bg=C["surface"], font=("Consolas", 8)).pack(anchor="w", pady=(2, 0))

        self._clock_lbl = tk.Label(hdr, text="", fg=C["text3"],
                                   bg=C["surface"], font=("Consolas", 9))
        self._clock_lbl.pack(side="right", padx=20, pady=(0, 8))
        self._tick()

        tk.Frame(self, height=1, bg=C["border2"]).pack(side="top", fill="x")
        tk.Frame(self, height=2, bg=C["purple"]).pack(side="top", fill="x")

    def _tick(self):
        now = datetime.datetime.now().strftime("%H:%M:%S  ·  %d %b %Y")
        self._clock_lbl.config(text=now)
        self.after(1000, self._tick)

    def _build_statusbar(self):
        status_container = tk.Frame(self, bg=C["surface"])
        status_container.pack(side="bottom", fill="x")

        tk.Frame(status_container, height=1, bg=C["border"]).pack(fill="x", side="top")
        bar = tk.Frame(status_container, bg=C["surface"], pady=5)
        bar.pack(fill="x")
        
        tk.Label(bar, text="●", fg=C["green"], bg=C["surface"],
                 font=("Consolas", 8)).pack(side="left", padx=(14,4))
        self._status_lbl = tk.Label(bar, textvariable=self._status_var,
                                    fg=C["text3"], bg=C["surface"],
                                    font=("Consolas", 8), anchor="w")
        self._status_lbl.pack(side="left")
        tk.Label(bar, text="v2.0  ·  NAPSS", fg=C["text3"],
                 bg=C["surface"], font=("Consolas", 8)).pack(side="right", padx=14)

    def _build_body(self):
        body = tk.Frame(self, bg=C["bg"])
        body.pack(side="top", fill="both", expand=True, padx=24, pady=12)

        # 01 — Order
        self._section_label(body, "01", "Derivative Order", C["cyan"])
        order_row = tk.Frame(body, bg=C["bg"])
        order_row.pack(fill="x", pady=(4,10))
        SegmentedControl(
            order_row,
            options=["   First Derivative  f'(x)   ",
                     "   Second Derivative  f''(x)   "],
            colors=[C["cyan"], C["purple"]],
            variable=self._order,
            command=self._on_change
        ).pack(side="left")

        # 02 — Equation type
        self._section_label(body, "02", "Equation Type", C["purple"])
        eq_row = tk.Frame(body, bg=C["bg"])
        eq_row.pack(fill="x", pady=(4,10))
        SegmentedControl(
            eq_row,
            options=["   Backward   ", "   Central   ", "   Forward   "],
            colors=EQ_COLORS,
            variable=self._eq_idx,
            command=self._on_change
        ).pack(side="left")

        self._formula_lbl = tk.Label(eq_row, text="", fg=C["green"],
                                     bg=C["bg"], font=("Consolas", 9, "bold"),
                                     justify="left")
        self._formula_lbl.pack(side="left", padx=(14,0))

        # 03 — x and h
        self._section_label(body, "03", "Parameters  x  and  h", C["green"])
        xh_card = tk.Frame(body, bg=C["card"],
                           highlightthickness=1, highlightbackground=C["border"])
        xh_card.pack(fill="x", pady=(4,10), ipady=6)
        xh_inner = tk.Frame(xh_card, bg=C["card"])
        xh_inner.pack(padx=20, anchor="w")
        for ci, (name, var, col) in enumerate([("x", self._xvar, C["cyan"]),
                                               ("h", self._hvar, C["green"])]):
            tk.Label(xh_inner, text=f"{name}  =", fg=col, bg=C["card"],
                     font=("Consolas", 12, "bold")).grid(
                         row=0, column=ci*2, padx=(0,8), pady=2)
            NeonEntry(xh_inner, textvariable=var, width=10, accent=col).grid(
                row=0, column=ci*2+1, padx=(0,36))

        # 04 — Function values
        self._section_label(body, "04", "Function Values", C["yellow"])
        self._fval_outer = tk.Frame(body, bg=C["bg"])
        self._fval_outer.pack(fill="x", pady=(4,10))

        # 05 — Action + Result
        self._section_label(body, "05", "Calculate", C["text2"])
        action_row = tk.Frame(body, bg=C["bg"])
        action_row.pack(fill="x", pady=(4,10))

        btn_calc = tk.Button(action_row, text="CALCULATE", command=self._calculate,
                             bg=C["purple"], fg=C["white"], activebackground="#b873ff",
                             activeforeground=C["white"], font=("Consolas", 10, "bold"),
                             bd=0, relief="flat", padx=20, pady=8, cursor="hand2")
        btn_calc.pack(side="left")

        btn_clear = tk.Button(action_row, text="CLEAR", command=self._clear,
                              bg=C["card2"], fg=C["text2"], activebackground=C["border2"],
                              activeforeground=C["white"], font=("Consolas", 10, "bold"),
                              bd=0, relief="flat", padx=15, pady=8, cursor="hand2")
        btn_clear.pack(side="left", padx=(10,0))

        res_card = tk.Frame(action_row, bg=C["card"],
                            highlightthickness=1, highlightbackground=C["border"])
        res_card.pack(side="left", fill="x", expand=True, padx=(18,0), ipady=2)
        tk.Label(res_card, text="RESULT", fg=C["text3"],
                 bg=C["card"], font=("Consolas", 7)).pack(anchor="w", padx=12, pady=(4,0))
        tk.Label(res_card, textvariable=self._result_var, fg=C["yellow"],
                 bg=C["card"], font=("Consolas", 15, "bold"),
                 anchor="w").pack(anchor="w", padx=12, pady=(0,4))

        # 06 — History
        self._section_label(body, "06", "History", C["text3"])
        hist_card = tk.Frame(body, bg=C["card"], height=85,
                              highlightthickness=1, highlightbackground=C["border"])
        hist_card.pack(fill="x", pady=(4,0))
        hist_card.pack_propagate(False)  # تجميد الارتفاع لمنع دفع شريط الحالة

        hist_inner = tk.Frame(hist_card, bg=C["card"])
        hist_inner.pack(fill="both", expand=True, padx=14, pady=4)

        self._hist_lbl = tk.Label(hist_inner, text="No calculations yet.",
                                  fg=C["text3"], bg=C["card"],
                                  font=("Consolas", 9), anchor="nw", justify="left")
        self._hist_lbl.pack(side="left", fill="both", expand=True)

        btn_del_hist = tk.Button(hist_inner, text="DELETE", command=self._clear_history,
                                 bg="#2a1520", fg=C["red"], activebackground=C["red"],
                                 activeforeground=C["white"], font=("Consolas", 8, "bold"),
                                 bd=1, relief="solid", highlightthickness=0,
                                 highlightbackground=C["red"], padx=10, pady=3, cursor="hand2")
        btn_del_hist.pack(side="right", anchor="ne")

    def _section_label(self, parent, num, title, col):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill="x", pady=(0,0))
        tk.Label(row, text=num, fg=col, bg=C["bg"],
                 font=("Consolas", 8, "bold")).pack(side="left", padx=(0,4))
        tk.Frame(row, width=3, bg=col).pack(side="left", fill="y", pady=2)
        tk.Label(row, text=f"  {title}", fg=C["text2"], bg=C["bg"],
                 font=("Consolas", 9)).pack(side="left")
        tk.Frame(row, height=1, bg=C["border"]).pack(
            side="left", fill="x", expand=True, padx=10)

    def _build_fval_card(self):
        if self._fval_card:
            self._fval_card.destroy()

        order = self._order.get()
        eq    = self._eq_idx.get()
        keys  = FIELD_MAP.get((order, eq), [])
        cols  = [C["cyan"], C["green"], C["purple"], C["yellow"]]

        self._fval_card = tk.Frame(self._fval_outer, bg=C["card"],
                                   highlightthickness=1,
                                   highlightbackground=C["border"])
        self._fval_card.pack(fill="x", ipady=6)

        inner = tk.Frame(self._fval_card, bg=C["card"])
        inner.pack(padx=16, pady=(2,0), anchor="w")

        self._f_entries.clear()
        for i, key in enumerate(keys):
            col = cols[i % len(cols)]
            tk.Label(inner, text=f"{key} =", fg=col,
                     bg=C["card"], font=("Consolas", 11)).grid(
                         row=0, column=i*2, padx=(0,4), pady=2)
            ent = NeonEntry(inner, width=9, accent=col)
            ent.grid(row=0, column=i*2+1, padx=(0,12))
            self._f_entries[key] = ent

    def _update_formula(self):
        if self._formula_lbl:
            key = (self._order.get(), self._eq_idx.get())
            self._formula_lbl.config(text=EQ_FORMULAS.get(key, ""))

    def _on_change(self):
        if self._fval_outer:
            self._build_fval_card()
            self._update_formula()
            self._result_var.set("—")

    def _set_status(self, msg, col=None):
        self._status_var.set(msg)
        if self._status_lbl:
            self._status_lbl.config(fg=col or C["text3"])

    def _calculate(self):
        try:
            xv = float(self._xvar.get())
            hv = float(self._hvar.get())
        except ValueError:
            self._result_var.set("—")
            self._set_status("⚠  x and h must be numeric values.", C["red"])
            return

        fvals = {}
        for key, ent in self._f_entries.items():
            raw = ent.get().strip()
            if not raw:
                self._set_status(f"⚠  Missing value for {key}", C["red"])
                self._result_var.set("—")
                return
            try:
                fvals[key] = float(raw)
            except ValueError:
                self._set_status(f"⚠  {key} must be a number.", C["red"])
                self._result_var.set("—")
                return

        order = self._order.get()
        eq    = self._eq_idx.get()
        expr  = (FIRST_EQS if order == 0 else SECOND_EQS)[eq]

        subs   = [(SYMPY_KEY[k](), v) for k, v in fvals.items()]
        result = float(expr.subs(subs).subs([(x, xv), (h, hv)]))
        label  = "f'" if order == 0 else "f''"
        r_str  = f"{label}({round(xv,4)})  =  {round(result, 8)}"

        self._result_var.set(r_str)
        self._set_status(
            f"✔  Calculated using {EQ_NAMES[eq]} difference method.", C["green"])

        self._history.insert(0, r_str)
        self._history = self._history[:3]
        self._hist_lbl.config(text="\n".join(self._history))

    def _clear(self):
        self._xvar.set("")
        self._hvar.set("")
        for ent in self._f_entries.values():
            ent.set("")

        self._result_var.set("—")
        self._set_status("Cleared.", C["text3"])

    def _clear_history(self):
        self._history.clear()
        self._hist_lbl.config(text="No calculations yet.")
        self._set_status("History cleared.", C["text3"])


if __name__ == "__main__":
    app = NAPSS()
    app.mainloop()