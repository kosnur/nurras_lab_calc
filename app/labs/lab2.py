# app/labs/lab2.py — №2 Горизонталь лақтырылған дененің қозғалысын зерделеу
#
# Формула:  υ₀ = l · √(g / 2h)
# Вводится: h (высота, м),  l (дальность, м)
# Находится: υ₀ (начальная скорость, м/с),  υ₀орт (среднее)

import math
from app.base_lab import LabFrame

G = 9.81  # ускорение свободного падения, м/с²


class Lab2Frame(LabFrame):
    LAB_NAME   = "№2  Горизонталь лақтырылған дененің қозғалысын зерделеу"
    INPUTS     = [
        ("h — биіктік (высота)",          "м", "h"),
        ("l — ұшу қашықтығы (дальность)", "м", "l"),
    ]
    RESULT_KEY = "v0"

    # ── Формула ──────────────────────────────────────────────────
    def compute(self, inputs: dict) -> dict:
        h = inputs["h"]
        l = inputs["l"]
        if h <= 0:
            raise ZeroDivisionError
        v0 = l * math.sqrt(G / (2 * h))    # υ₀ = l·√(g/2h)
        return {"h": h, "l": l, "v0": v0}

    # ── Форматирование ───────────────────────────────────────────
    def _format_result(self, idx: int, result: dict) -> str:
        return (f"  Тәжірибе {idx}:  h={result['h']:.3f} м,  "
                f"l={result['l']:.3f} м  →  υ₀ = {result['v0']:.4f} м/с")

    def _format_errors(self, err: dict) -> str:
        pct = err["rel_err"] * 100
        return (
            f"\n  📊 Орташа мән (среднее):            υ₀орт = {err['mean']:.4f} м/с"
            f"\n  📐 Абсолютная погрешность:            Δυ₀  = {err['abs_err']:.4f} м/с"
            f"\n  📏 Относительная погрешность:         ευ₀  = {pct:.2f} %"
            f"\n  🔢 Тәжірибелер саны (кол-во опытов):  n   = {err['n']}"
        )
