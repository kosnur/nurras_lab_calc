# app/utils.py — Математические утилиты (расчёт погрешностей)


def calc_errors(values: list) -> dict:
    """
    Вычисляет среднее и погрешности по формулам из ТЗ:

        среднее   x_орт = Σx_i / n
        ε_абс           = Σ|x_орт − x_i| / n
        ε_отн           = ε_абс / |x_орт|

    Возвращает:
        {"mean": float, "abs_err": float, "rel_err": float, "n": int}
    или {} если список пустой.
    """
    n = len(values)
    if n == 0:
        return {}
    mean    = sum(values) / n
    abs_err = sum(abs(mean - v) for v in values) / n
    rel_err = abs_err / abs(mean) if mean != 0 else 0.0
    return {"mean": mean, "abs_err": abs_err, "rel_err": rel_err, "n": n}
