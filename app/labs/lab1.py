# app/labs/lab1.py — №1 Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау
#
# Формула:  a = 2S / t²
# Вводится: S (расстояние, м),  t (время, с)
# Находится: a (ускорение, м/с²),  aорт (среднее)

from app.base_lab import LabFrame


class Lab1Frame(LabFrame):
    LAB_NAME   = "№1  Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау"
    INPUTS     = [
        ("S — арақашықтық (расстояние)", "м", "S"),
        ("t — қозғалыс уақыты (время)",  "с", "t"),
    ]
    RESULT_KEY = "a"

    # ── Формула ──────────────────────────────────────────────────
    def compute(self, inputs: dict) -> dict:
        S = inputs["S"]
        t = inputs["t"]
        if t == 0:
            raise ZeroDivisionError
        a = 2 * S / (t ** 2)        # a = 2S / t²
        return {"S": S, "t": t, "a": a}

    # ── Форматирование ───────────────────────────────────────────
    def _format_result(self, idx: int, result: dict) -> str:
        return (f"  Тәжірибе {idx}:  S={result['S']:.3f} м,  "
                f"t={result['t']:.3f} с  →  a = {result['a']:.4f} м/с²")

    def _format_errors(self, err: dict) -> str:
        pct = err["rel_err"] * 100
        return (
            f"\n  📊 Орташа мән (среднее):            aорт = {err['mean']:.4f} м/с²"
            f"\n  📐 Абсолютная погрешность:            Δa  = {err['abs_err']:.4f} м/с²"
            f"\n  📏 Относительная погрешность:         εa  = {pct:.2f} %"
            f"\n  🔢 Тәжірибелер саны (кол-во опытов):  n  = {err['n']}"
        )
