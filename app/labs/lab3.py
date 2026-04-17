# app/labs/lab3.py — №3 Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау
#
# Формула:  g = 4π²lN² / t²
# Вводится: l (длина нити, м),  N (число колебаний),  t (время, с)
# Находится: g (ускорение своб. падения, м/с²),  gорт (среднее)

import math
from app.base_lab import LabFrame


class Lab3Frame(LabFrame):
    LAB_NAME   = "№3  Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау"
    INPUTS     = [
        ("l — жіптің ұзындығы (длина нити)",  "м",  "l"),
        ("N — тербеліс саны (число колеб.)",  "шт", "N"),
        ("t — тербеліс уақыты (время колеб.)", "с",  "t"),
    ]
    RESULT_KEY = "g"

    # ── Формула ──────────────────────────────────────────────────
    def compute(self, inputs: dict) -> dict:
        l = inputs["l"]
        N = inputs["N"]
        t = inputs["t"]
        if t == 0:
            raise ZeroDivisionError
        g = 4 * math.pi ** 2 * l * N ** 2 / (t ** 2)   # g = 4π²lN²/t²
        return {"l": l, "N": N, "t": t, "g": g}

    # ── Форматирование ───────────────────────────────────────────
    def _format_result(self, idx: int, result: dict) -> str:
        return (f"  Тәжірибе {idx}:  l={result['l']:.3f} м,  "
                f"N={result['N']:.0f},  t={result['t']:.3f} с  →  g = {result['g']:.4f} м/с²")

    def _format_errors(self, err: dict) -> str:
        pct = err["rel_err"] * 100
        return (
            f"\n  📊 Орташа мән (среднее):            gорт = {err['mean']:.4f} м/с²"
            f"\n  📐 Абсолютная погрешность:            Δg   = {err['abs_err']:.4f} м/с²"
            f"\n  📏 Относительная погрешность:         εg   = {pct:.2f} %"
            f"\n  🔢 Тәжірибелер саны (кол-во опытов):  n   = {err['n']}"
        )
