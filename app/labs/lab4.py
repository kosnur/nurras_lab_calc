# app/labs/lab4.py — №4 Беттік толқындардың таралу жылдамдығын анықтау
#
# Формула:  υ = l / t
# Вводится: t (уақыт, с),  l (Ыдыстың ұзындығы, м)
# Находится: υ (толқынның жылдамдығы, м/с),  υорт (среднее)

from app.base_lab import LabFrame


class Lab4Frame(LabFrame):
    LAB_NAME   = "№4  Беттік толқындардың таралу жылдамдығын анықтау"
    INPUTS     = [
        ("t — уақыт (время)", "с", "t"),
        ("l — Ыдыстың ұзындығы (длина сосуда)", "м", "l"),
    ]
    RESULT_KEY = "υ"

    # ── Формула ──────────────────────────────────────────────────
    def compute(self, inputs: dict) -> dict:
        t = inputs["t"]
        l = inputs["l"]
        if t == 0:
            raise ZeroDivisionError
        υ = l / t            # υ = l / t
        return {"t": t, "l": l, "υ": υ}

    # ── Форматирование ───────────────────────────────────────────
    def _format_result(self, idx: int, result: dict) -> str:
        return (f"  Тәжірибе {idx}:  t={result['t']:.3f} с,  "
                f"l={result['l']:.3f} м  →  υ = {result['υ']:.4f} м/с")

    def _format_errors(self, err: dict) -> str:
        pct = err["rel_err"] * 100
        return (
            f"\n  📊 Орташа мән (среднее):            υорт = {err['mean']:.4f} м/с"
            f"\n  📐 Абсолютная погрешность:            Δυ  = {err['abs_err']:.4f} м/с"
            f"\n  📏 Относительная погрешность:         ευ  = {pct:.2f} %"
            f"\n  🔢 Тәжірибелер саны (кол-во опытов):  n  = {err['n']}"
        )
