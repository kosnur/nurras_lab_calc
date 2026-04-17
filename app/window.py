# app/window.py — Главное окно приложения
import tkinter as tk

from app.theme import BG, SURFACE, ACCENT, TEXT, TEXT_DIM, BORDER, apply_style
from app.labs import LABS


class App(tk.Tk):
    """Главное окно с боковым меню и областью отображения лаб. работы."""

    def __init__(self):
        super().__init__()
        self.title("Физика Зертханасы — Лабораторный калькулятор")
        self.geometry("900x680")
        self.minsize(700, 520)
        self.configure(bg=BG)
        apply_style()
        self._build_ui()

    # ─────────────────────────────── UI ──────────────────────────
    def _build_ui(self):
        self._build_sidebar()
        self._build_main_area()
        self._select_lab(0)

    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=SURFACE, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Логотип
        tk.Label(sidebar, text="⚗️",
                 bg=SURFACE, fg=ACCENT,
                 font=("Segoe UI", 28)).pack(pady=(24, 4))
        tk.Label(sidebar, text="Физика\nЗертханасы",
                 bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 12, "bold"),
                 justify="center").pack(pady=(0, 4))
        tk.Label(sidebar, text="лабораторный калькулятор",
                 bg=SURFACE, fg=TEXT_DIM,
                 font=("Segoe UI", 8)).pack(pady=(0, 20))

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=8)

        tk.Label(sidebar, text="ЖҰМЫСТАР / РАБОТЫ",
                 bg=SURFACE, fg=TEXT_DIM,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=16, pady=(8, 6))

        self._sidebar_buttons = []
        for i, (name, _cls) in enumerate(LABS):
            btn = tk.Button(
                sidebar,
                text=name,
                bg=SURFACE, fg=TEXT,
                font=("Segoe UI", 9),
                relief="flat", cursor="hand2",
                anchor="w",
                padx=16, pady=8,
                wraplength=190, justify="left",
                command=lambda i=i: self._select_lab(i)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self._sidebar_buttons.append(btn)

    def _build_main_area(self):
        self._main = tk.Frame(self, bg=BG)
        self._main.pack(side="left", fill="both", expand=True)
        self._current_lab = None

    # ──────────────── Переключение работ ─────────────────────────
    def _select_lab(self, idx: int):
        # Подсветка активной кнопки
        for b in self._sidebar_buttons:
            b.configure(bg=SURFACE, fg=TEXT)
        self._sidebar_buttons[idx].configure(bg=ACCENT, fg="#ffffff")

        # Замена виджета в основной области
        for w in self._main.winfo_children():
            w.destroy()

        _label, cls = LABS[idx]
        self._current_lab = cls(self._main)
        self._current_lab.pack(fill="both", expand=True)
