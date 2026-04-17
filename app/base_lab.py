# app/base_lab.py — Базовый класс лабораторного калькулятора
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime

from app.theme import (BG, SURFACE, CARD, ACCENT, TEXT,
                       TEXT_DIM, ERROR_COL, BORDER)
from app.utils import calc_errors


class LabFrame(tk.Frame):
    """
    Базовый виджет для одной лабораторной работы.

    Чтобы добавить новую лаб. работу — создай подкласс и переопредели:
        LAB_NAME   : str                  — название работы
        INPUTS     : list[tuple]          — [(label, unit, var_name), ...]
        RESULT_KEY : str                  — ключ словаря из compute()
        compute(inputs) -> dict           — формула расчёта
        _format_result(idx, result) -> str
        _format_errors(err)         -> str
    """

    LAB_NAME   = "Лаборатория"
    INPUTS     = []        # [(label_text, units, var_name), ...]
    RESULT_KEY = "result"  # ключ из compute(), идущий в расчёт погрешности

    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG, **kw)
        self._tab_count    = 0
        self._tab_frames   = []   # tk.Frame per вкладке
        self._tab_vars     = []   # dict {var_name: StringVar} per вкладке
        self._last_results = []   # результаты последнего расчёта
        self._last_errors  = {}   # погрешности последнего расчёта
        self._build_ui()

    # ─────────────────────────────────── UI ──────────────────────
    def _build_ui(self):
        # Заголовок + кнопка добавления вкладки
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(18, 0))

        tk.Label(hdr, text=self.LAB_NAME,
                 bg=BG, fg=TEXT,
                 font=("Segoe UI", 13, "bold"),
                 wraplength=580, justify="left").pack(side="left")

        tk.Button(hdr, text="＋  Тәжірибе қосу",
                  bg=ACCENT, fg="#fff",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2",
                  command=self._add_tab,
                  padx=12, pady=5).pack(side="right")

        # Разделительная линия
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=10)

        # Notebook (вкладки экспериментов)
        nb_frame = tk.Frame(self, bg=BG)
        nb_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self._notebook = ttk.Notebook(nb_frame)
        self._notebook.pack(fill="both", expand=True)

        # Кнопки действий
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=(0, 8))

        tk.Button(btn_row, text="⚡  Есептеу",
                  bg=ACCENT, fg="#fff",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2",
                  command=self._calculate,
                  padx=16, pady=8).pack(side="left", padx=(0, 10))

        tk.Button(btn_row, text="💾  TXT экспорт",
                  bg=CARD, fg=TEXT,
                  font=("Segoe UI", 10),
                  relief="flat", cursor="hand2",
                  command=self._export_txt,
                  padx=12, pady=8).pack(side="left")

        # Область результатов
        res_frame = tk.Frame(self, bg=SURFACE, bd=0, relief="flat")
        res_frame.pack(fill="both", expand=False, padx=20, pady=(0, 16))
        res_frame.pack_propagate(False)
        res_frame.configure(height=220)

        tk.Label(res_frame, text="Нәтиже / Результат",
                 bg=SURFACE, fg=ACCENT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=14, pady=(10, 4))

        self._result_text = tk.Text(
            res_frame,
            bg=SURFACE, fg=TEXT,
            font=("Consolas", 10),
            relief="flat", wrap="word",
            state="disabled",
            insertbackground=TEXT
        )
        self._result_text.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        # Первая вкладка по умолчанию
        self._add_tab()

    # ─────────────────────────────── Вкладки ─────────────────────
    def _add_tab(self):
        self._tab_count += 1
        frame = tk.Frame(self._notebook, bg=CARD, padx=20, pady=16)
        self._notebook.add(frame, text=f"  {self._tab_count}  ")
        self._notebook.select(frame)

        vars_dict = {}

        for lbl, unit, var_name in self.INPUTS:
            row = tk.Frame(frame, bg=CARD)
            row.pack(fill="x", pady=6)

            tk.Label(row, text=lbl, bg=CARD, fg=TEXT,
                     font=("Segoe UI", 10),
                     width=32, anchor="w").pack(side="left")

            sv = tk.StringVar()
            vars_dict[var_name] = sv

            tk.Entry(row, textvariable=sv,
                     bg=BG, fg=TEXT, insertbackground=TEXT,
                     relief="flat", font=("Segoe UI", 10),
                     width=14).pack(side="left", padx=(6, 4))

            tk.Label(row, text=unit, bg=CARD, fg=TEXT_DIM,
                     font=("Segoe UI", 9)).pack(side="left")

        # Кнопка удаления вкладки
        tk.Button(frame, text="🗑  Жою",
                  bg="#3f2020", fg=ERROR_COL,
                  font=("Segoe UI", 9),
                  relief="flat", cursor="hand2",
                  command=lambda f=frame, d=vars_dict: self._remove_tab(f, d),
                  padx=8, pady=4).pack(anchor="e", pady=(10, 0))

        self._tab_frames.append(frame)
        self._tab_vars.append(vars_dict)

    def _remove_tab(self, frame, vars_dict):
        if len(self._tab_frames) <= 1:
            messagebox.showwarning(
                "Ескерту",
                "Кемінде бір тәжірибе болуы керек!\n"
                "Минимум одна вкладка должна остаться.")
            return
        idx = self._tab_frames.index(frame)
        self._tab_frames.pop(idx)
        self._tab_vars.pop(idx)
        self._notebook.forget(frame)

    # ─────────────────────────────── Расчёт ──────────────────────
    def _calculate(self):
        results = []
        for i, vars_dict in enumerate(self._tab_vars):
            try:
                inputs = {k: float(v.get()) for k, v in vars_dict.items()}
            except ValueError:
                messagebox.showerror(
                    "Қате / Ошибка",
                    f"{i+1}-тәжірибеде дұрыс сан енгізілмеген!\n"
                    f"В опыте {i+1} введено некорректное число.")
                return

            try:
                result = self.compute(inputs)
            except ZeroDivisionError:
                messagebox.showerror(
                    "Қате / Ошибка",
                    f"{i+1}-тәжірибеде нөлге бөлу!\n"
                    f"В опыте {i+1} деление на ноль.")
                return

            results.append(result)

        self._last_results = results
        self._last_errors  = calc_errors([r[self.RESULT_KEY] for r in results])
        self._show_results(results, self._last_errors)

    def _show_results(self, results, err):
        lines = ["═" * 52]
        for i, r in enumerate(results):
            lines.append(self._format_result(i + 1, r))
        lines.append("═" * 52)
        if err:
            lines.append(self._format_errors(err))

        self._result_text.configure(state="normal")
        self._result_text.delete("1.0", "end")
        self._result_text.insert("end", "\n".join(lines))
        self._result_text.configure(state="disabled")

    # ─────────────────────────────── Экспорт ─────────────────────
    def _export_txt(self):
        if not self._last_results:
            messagebox.showinfo(
                "Ескерту",
                "Алдымен есептеуді орындаңыз!\n"
                "Сначала выполните расчёт.")
            return

        safe_name = self.LAB_NAME[:30].strip().replace("/", "-").replace("\\", "-")
        path = filedialog.asksaveasfilename(
            title="Нәтижені сақтау / Сохранить результат",
            defaultextension=".txt",
            initialfile=f"{safe_name}.txt",
            filetypes=[("Мәтін файлы / Текстовый файл", "*.txt")]
        )
        if not path:
            return

        now   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "═" * 60,
            "  Физика Зертханасы — Лабораторный калькулятор",
            f"  {self.LAB_NAME}",
            f"  Дата / Күні: {now}",
            "═" * 60,
            "",
            "  ТӘЖІРИБЕ НӘТИЖЕЛЕРІ / РЕЗУЛЬТАТЫ ОПЫТОВ:",
            "  " + "─" * 50,
        ]
        for i, r in enumerate(self._last_results):
            lines.append(self._format_result(i + 1, r))
        lines += [
            "",
            "  ҚОРЫТЫНДЫ / ИТОГ:",
            "  " + "─" * 50,
        ]
        if self._last_errors:
            lines.append(self._format_errors(self._last_errors))
        lines += ["", "═" * 60]

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Сақталды / Сохранено", f"Файл сақталды:\n{path}")
        except OSError as e:
            messagebox.showerror("Қате / Ошибка", f"Файлды сақтау қатесі:\n{e}")

    # ──────────────── Методы для переопределения ──────────────────
    def compute(self, inputs: dict) -> dict:
        """Формула расчёта. Переопределяется в каждой лаб. работe."""
        raise NotImplementedError

    def _format_result(self, idx: int, result: dict) -> str:
        """Строка результата одного опыта."""
        raise NotImplementedError

    def _format_errors(self, err: dict) -> str:
        """Строка итоговых погрешностей."""
        raise NotImplementedError
