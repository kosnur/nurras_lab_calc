# app/theme.py — Цвета и стили приложения
from tkinter import ttk

# ── Палитра ──────────────────────────────────────────────────
BG        = "#1e1e2e"
SURFACE   = "#2a2a3e"
CARD      = "#313145"
ACCENT    = "#7c83ff"
ACCENT2   = "#a78bfa"
TEXT      = "#e2e8f0"
TEXT_DIM  = "#94a3b8"
SUCCESS   = "#4ade80"
ERROR_COL = "#f87171"
BORDER    = "#3f3f5c"


def apply_style() -> None:
    """Применяет тёмную тему ко всем ttk-виджетам."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 10))

    # Notebook (вкладки экспериментов)
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=CARD, foreground=TEXT_DIM,
                    padding=[14, 6], font=("Segoe UI", 10))
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#ffffff")])

    # Кнопки
    style.configure("Accent.TButton",
                    background=ACCENT, foreground="#ffffff",
                    font=("Segoe UI", 10, "bold"),
                    padding=[10, 6], relief="flat")
    style.map("Accent.TButton",
              background=[("active", ACCENT2)])

    style.configure("Danger.TButton",
                    background="#dc2626", foreground="#ffffff",
                    font=("Segoe UI", 9),
                    padding=[6, 4], relief="flat")
    style.map("Danger.TButton",
              background=[("active", "#b91c1c")])

    style.configure("Ghost.TButton",
                    background=SURFACE, foreground=TEXT_DIM,
                    font=("Segoe UI", 10),
                    padding=[10, 6], relief="flat")
    style.map("Ghost.TButton",
              background=[("active", CARD)])

    # Entry
    style.configure("TEntry",
                    fieldbackground=CARD, foreground=TEXT,
                    insertcolor=TEXT, bordercolor=BORDER,
                    relief="flat", padding=6)

    # Separator
    style.configure("TSeparator", background=BORDER)

    # Scrollbar
    style.configure("TScrollbar",
                    background=SURFACE, troughcolor=BG,
                    borderwidth=0, arrowcolor=TEXT_DIM)
