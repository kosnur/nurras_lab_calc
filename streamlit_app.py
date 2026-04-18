"""
streamlit_app.py — Физика Зертханасы (Streamlit Cloud версия)

Запуск локально:
    pip install streamlit
    streamlit run streamlit_app.py

Деплой на Streamlit Cloud:
    1. Загрузи проект на GitHub
    2. Зайди на share.streamlit.io → New app → выбери репозиторий
    3. Main file path: streamlit_app.py
"""

import math
import datetime
import io
import streamlit as st

# ─────────────────────────────── Конфигурация страницы ───────────────────────
st.set_page_config(
    page_title="Физика Зертханасы — Лабораторный калькулятор",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────── CSS ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Основной фон */
  .stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #12121f 100%);
  }

  /* Сайдбар */
  [data-testid="stSidebar"] {
    background: #16162a !important;
    border-right: 1px solid #2a2a48;
  }
  [data-testid="stSidebar"] * {
    color: #c8c8e8 !important;
  }

  /* Заголовки */
  h1, h2, h3 { color: #e8e8ff !important; }

  /* Карточки опытов */
  .exp-card {
    background: #1e1e35;
    border: 1px solid #2e2e50;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
  }
  .exp-card:hover { border-color: #7c6bff; }

  /* Область результатов */
  .result-box {
    background: #1a1a2e;
    border: 1px solid #3a3a60;
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #b8d4ff;
    white-space: pre-wrap;
    line-height: 1.8;
  }

  /* Метрики */
  [data-testid="stMetric"] {
    background: #1e1e35;
    border: 1px solid #2e2e50;
    border-radius: 10px;
    padding: 12px 16px;
  }
  [data-testid="stMetricValue"] { color: #a78bfa !important; font-size: 1.4rem !important; }
  [data-testid="stMetricLabel"] { color: #8888aa !important; }

  /* Кнопки */
  .stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(124,107,255,0.3) !important; }

  /* Поля ввода */
  .stNumberInput input, .stTextInput input {
    background: #12121f !important;
    border: 1px solid #2e2e50 !important;
    border-radius: 8px !important;
    color: #e8e8ff !important;
    font-family: 'JetBrains Mono', monospace !important;
  }
  .stNumberInput input:focus, .stTextInput input:focus {
    border-color: #7c6bff !important;
    box-shadow: 0 0 0 2px rgba(124,107,255,0.2) !important;
  }

  /* Разделитель */
  hr { border-color: #2a2a48 !important; }

  /* Скрыть меню hamburger и footer */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }

  /* Вкладки */
  [data-testid="stTab"] { background: transparent !important; }
  button[data-baseweb="tab"] {
    background: #1e1e35 !important;
    border-radius: 8px 8px 0 0 !important;
    color: #8888aa !important;
    font-weight: 500 !important;
  }
  button[data-baseweb="tab"][aria-selected="true"] {
    background: #2e2e50 !important;
    color: #a78bfa !important;
    border-bottom: 2px solid #7c6bff !important;
  }

  /* Бейдж работы */
  .lab-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c6bff, #a78bfa);
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  /* Предупреждение */
  .warn-box {
    background: #2a1f3a;
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    color: #fbbf24;
    font-size: 13px;
    margin: 8px 0;
  }

  /* Формула */
  .formula-box {
    background: #12121f;
    border: 1px solid #2e2e50;
    border-radius: 8px;
    padding: 10px 16px;
    font-family: 'JetBrains Mono', monospace;
    color: #a78bfa;
    font-size: 14px;
    margin: 8px 0 16px 0;
  }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  УТИЛИТЫ
# ═══════════════════════════════════════════════════════════════════════════════

def calc_errors(values: list) -> dict:
    """Среднее, абсолютная и относительная погрешности."""
    n = len(values)
    if n == 0:
        return {}
    mean    = sum(values) / n
    abs_err = sum(abs(mean - v) for v in values) / n
    rel_err = abs_err / abs(mean) if mean != 0 else 0.0
    return {"mean": mean, "abs_err": abs_err, "rel_err": rel_err, "n": n}


G = 9.81  # ускорение свободного падения, м/с²


# ═══════════════════════════════════════════════════════════════════════════════
#  ФОРМУЛЫ ЛАБОРАТОРНЫХ РАБОТ
# ═══════════════════════════════════════════════════════════════════════════════

def compute_lab1(S: float, t: float) -> dict:
    """a = 2S / t²"""
    if t == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    a = 2 * S / (t ** 2)
    return {"S": S, "t": t, "a": a}


def compute_lab2(h: float, l: float) -> dict:
    """υ₀ = l · √(g / 2h)"""
    if h <= 0:
        raise ZeroDivisionError("h должна быть > 0")
    v0 = l * math.sqrt(G / (2 * h))
    return {"h": h, "l": l, "v0": v0}


def compute_lab3(l: float, N: float, t: float) -> dict:
    """g = 4π²lN² / t²"""
    if t == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    g = 4 * math.pi ** 2 * l * N ** 2 / (t ** 2)
    return {"l": l, "N": N, "t": t, "g": g}


def compute_lab4(t: float, l: float) -> dict:
    """υ = l / t"""
    if t == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    v = l / t
    return {"t": t, "l": l, "v": v}


# ═══════════════════════════════════════════════════════════════════════════════
#  ФОРМАТИРОВАНИЕ РЕЗУЛЬТАТОВ
# ═══════════════════════════════════════════════════════════════════════════════

def format_lab1_result(idx: int, r: dict) -> str:
    return (f"  Тәжірибе {idx}:  S={r['S']:.3f} м,  "
            f"t={r['t']:.3f} с  →  a = {r['a']:.4f} м/с²")

def format_lab2_result(idx: int, r: dict) -> str:
    return (f"  Тәжірибе {idx}:  h={r['h']:.3f} м,  "
            f"l={r['l']:.3f} м  →  υ₀ = {r['v0']:.4f} м/с")

def format_lab3_result(idx: int, r: dict) -> str:
    return (f"  Тәжірибе {idx}:  l={r['l']:.3f} м,  "
            f"N={r['N']:.0f},  t={r['t']:.3f} с  →  g = {r['g']:.4f} м/с²")

def format_lab4_result(idx: int, r: dict) -> str:
    return (f"  Тәжірибе {idx}:  t={r['t']:.3f} с,  "
            f"l={r['l']:.3f} м  →  υ = {r['v']:.4f} м/с")

def format_errors(err: dict, symbol: str, unit: str) -> str:
    pct = err["rel_err"] * 100
    return (
        f"\n  📊 Орташа мән (среднее):            {symbol}орт = {err['mean']:.4f} {unit}"
        f"\n  📐 Абсолютная погрешность:            Δ{symbol}  = {err['abs_err']:.4f} {unit}"
        f"\n  📏 Относительная погрешность:         ε{symbol}  = {pct:.2f} %"
        f"\n  🔢 Тәжірибелер саны (кол-во опытов):  n  = {err['n']}"
    )

def format_result_block(results: list, errors: dict, fmt_fn, err_sym: str, err_unit: str) -> str:
    lines = ["═" * 54]
    for i, r in enumerate(results):
        lines.append(fmt_fn(i + 1, r))
    lines.append("═" * 54)
    if errors:
        lines.append(format_errors(errors, err_sym, err_unit))
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  ГЕНЕРАЦИЯ TXT
# ═══════════════════════════════════════════════════════════════════════════════

def build_txt(lab_name: str, results: list, errors: dict, fmt_fn, err_sym: str, err_unit: str) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "═" * 60,
        "  Физика Зертханасы — Лабораторный калькулятор",
        f"  {lab_name}",
        f"  Дата / Күні: {now}",
        "═" * 60,
        "",
        "  ТӘЖІРИБЕ НӘТИЖЕЛЕРІ / РЕЗУЛЬТАТЫ ОПЫТОВ:",
        "  " + "─" * 50,
    ]
    for i, r in enumerate(results):
        lines.append(fmt_fn(i + 1, r))
    lines += [
        "",
        "  ҚОРЫТЫНДЫ / ИТОГ:",
        "  " + "─" * 50,
    ]
    if errors:
        lines.append(format_errors(errors, err_sym, err_unit))
    lines += ["", "═" * 60]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  ВСПОМОГАТЕЛЬНЫЕ UI-КОМПОНЕНТЫ
# ═══════════════════════════════════════════════════════════════════════════════

def experiment_number_input(label: str, unit: str, key: str, value: float = 0.0):
    """Поле ввода числа с единицами измерения."""
    col_label, col_input, col_unit = st.columns([3, 2, 1])
    with col_label:
        st.markdown(f"<div style='padding-top:8px;color:#c8c8e8'>{label}</div>",
                    unsafe_allow_html=True)
    with col_input:
        val = st.number_input("", value=value, format="%.4f",
                              key=key, label_visibility="collapsed")
    with col_unit:
        st.markdown(f"<div style='padding-top:8px;color:#8888aa'>{unit}</div>",
                    unsafe_allow_html=True)
    return val


def metrics_row(results: list, errors: dict, value_key: str, unit: str):
    """Строка метрик: среднее, Δ, ε."""
    if not results or not errors:
        return
    n_cols = min(4, len(results) + 3)
    cols = st.columns(n_cols)
    for i, r in enumerate(results[:n_cols - 3]):
        with cols[i]:
            st.metric(f"Опыт {i+1}", f"{r[value_key]:.4f} {unit}")
    with cols[-3]:
        st.metric("Среднее (орт)", f"{errors['mean']:.4f} {unit}")
    with cols[-2]:
        st.metric("Δ (абс. погр.)", f"{errors['abs_err']:.4f} {unit}")
    with cols[-1]:
        st.metric("ε (отн. погр.)", f"{errors['rel_err']*100:.2f} %")


# ═══════════════════════════════════════════════════════════════════════════════
#  СТРАНИЦЫ ЛАБОРАТОРНЫХ РАБОТ
# ═══════════════════════════════════════════════════════════════════════════════

def page_lab1():
    st.markdown('<div class="lab-badge">Лаб. работа №1</div>', unsafe_allow_html=True)
    st.markdown("### №1 Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау")
    st.caption("Определение ускорения тела при равноускоренном движении")
    st.markdown('<div class="formula-box">a = 2S / t²</div>', unsafe_allow_html=True)

    # ── Управление количеством опытов ──
    if "lab1_count" not in st.session_state:
        st.session_state.lab1_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button("＋ Тәжірибе қосу", key="lab1_add", use_container_width=True):
            st.session_state.lab1_count += 1
    with col_remove:
        if st.button("－ Жою", key="lab1_remove", use_container_width=True,
                     disabled=st.session_state.lab1_count <= 1):
            st.session_state.lab1_count -= 1

    st.divider()

    # ── Вкладки опытов ──
    tab_labels = [f"Тәжірибе {i+1}" for i in range(st.session_state.lab1_count)]
    tabs = st.tabs(tab_labels)

    all_S, all_t = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            S = experiment_number_input("S — арақашықтық (расстояние)", "м",
                                        key=f"lab1_S_{i}", value=1.0)
            t = experiment_number_input("t — қозғалыс уақыты (время)", "с",
                                        key=f"lab1_t_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_S.append(S)
            all_t.append(t)

    # ── Расчёт ──
    st.divider()
    if st.button("⚡ Есептеу / Рассчитать", key="lab1_calc",
                 use_container_width=True, type="primary"):
        results = []
        error_occurred = False
        for i, (S, t) in enumerate(zip(all_S, all_t)):
            try:
                results.append(compute_lab1(S, t))
            except ZeroDivisionError as e:
                st.error(f"Опыт {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["a"] for r in results])
            st.session_state["lab1_results"] = results
            st.session_state["lab1_errors"]  = errors

    # ── Показ результатов ──
    if "lab1_results" in st.session_state:
        results = st.session_state["lab1_results"]
        errors  = st.session_state["lab1_errors"]

        st.markdown("#### 📊 Нәтиже / Результат")
        metrics_row(results, errors, "a", "м/с²")

        txt_result = format_result_block(
            results, errors, format_lab1_result, "a", "м/с²")
        st.markdown(f'<div class="result-box">{txt_result}</div>',
                    unsafe_allow_html=True)

        # ── Экспорт TXT ──
        txt_content = build_txt(
            "№1 Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау",
            results, errors, format_lab1_result, "a", "м/с²")
        st.download_button(
            label="💾 TXT экспорт",
            data=txt_content.encode("utf-8"),
            file_name="lab1_result.txt",
            mime="text/plain",
            key="lab1_download"
        )


# ─────────────────────────────────────────────────────────────────────────────

def page_lab2():
    st.markdown('<div class="lab-badge">Лаб. работа №2</div>', unsafe_allow_html=True)
    st.markdown("### №2 Горизонталь лақтырылған дененің қозғалысын зерделеу")
    st.caption("Изучение движения тела, брошенного горизонтально")
    st.markdown('<div class="formula-box">υ₀ = l · √(g / 2h),  где g = 9.81 м/с²</div>',
                unsafe_allow_html=True)

    if "lab2_count" not in st.session_state:
        st.session_state.lab2_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button("＋ Тәжірибе қосу", key="lab2_add", use_container_width=True):
            st.session_state.lab2_count += 1
    with col_remove:
        if st.button("－ Жою", key="lab2_remove", use_container_width=True,
                     disabled=st.session_state.lab2_count <= 1):
            st.session_state.lab2_count -= 1

    st.divider()

    tab_labels = [f"Тәжірибе {i+1}" for i in range(st.session_state.lab2_count)]
    tabs = st.tabs(tab_labels)

    all_h, all_l = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            h = experiment_number_input("h — биіктік (высота)", "м",
                                        key=f"lab2_h_{i}", value=1.0)
            l = experiment_number_input("l — ұшу қашықтығы (дальность)", "м",
                                        key=f"lab2_l_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_h.append(h)
            all_l.append(l)

    st.divider()
    if st.button("⚡ Есептеу / Рассчитать", key="lab2_calc",
                 use_container_width=True, type="primary"):
        results = []
        error_occurred = False
        for i, (h, l) in enumerate(zip(all_h, all_l)):
            try:
                results.append(compute_lab2(h, l))
            except ZeroDivisionError as e:
                st.error(f"Опыт {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["v0"] for r in results])
            st.session_state["lab2_results"] = results
            st.session_state["lab2_errors"]  = errors

    if "lab2_results" in st.session_state:
        results = st.session_state["lab2_results"]
        errors  = st.session_state["lab2_errors"]

        st.markdown("#### 📊 Нәтиже / Результат")
        metrics_row(results, errors, "v0", "м/с")

        txt_result = format_result_block(
            results, errors, format_lab2_result, "υ₀", "м/с")
        st.markdown(f'<div class="result-box">{txt_result}</div>',
                    unsafe_allow_html=True)

        txt_content = build_txt(
            "№2 Горизонталь лақтырылған дененің қозғалысын зерделеу",
            results, errors, format_lab2_result, "υ₀", "м/с")
        st.download_button(
            label="💾 TXT экспорт",
            data=txt_content.encode("utf-8"),
            file_name="lab2_result.txt",
            mime="text/plain",
            key="lab2_download"
        )


# ─────────────────────────────────────────────────────────────────────────────

def page_lab3():
    st.markdown('<div class="lab-badge">Лаб. работа №3</div>', unsafe_allow_html=True)
    st.markdown("### №3 Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау")
    st.caption("Определение ускорения свободного падения с помощью математического маятника")
    st.markdown('<div class="formula-box">g = 4π²lN² / t²</div>',
                unsafe_allow_html=True)

    if "lab3_count" not in st.session_state:
        st.session_state.lab3_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button("＋ Тәжірибе қосу", key="lab3_add", use_container_width=True):
            st.session_state.lab3_count += 1
    with col_remove:
        if st.button("－ Жою", key="lab3_remove", use_container_width=True,
                     disabled=st.session_state.lab3_count <= 1):
            st.session_state.lab3_count -= 1

    st.divider()

    tab_labels = [f"Тәжірибе {i+1}" for i in range(st.session_state.lab3_count)]
    tabs = st.tabs(tab_labels)

    all_l, all_N, all_t = [], [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            l = experiment_number_input("l — жіптің ұзындығы (длина нити)", "м",
                                        key=f"lab3_l_{i}", value=1.0)
            N = experiment_number_input("N — тербеліс саны (число колебаний)", "шт",
                                        key=f"lab3_N_{i}", value=10.0)
            t = experiment_number_input("t — тербеліс уақыты (время)", "с",
                                        key=f"lab3_t_{i}", value=20.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_l.append(l)
            all_N.append(N)
            all_t.append(t)

    st.divider()
    if st.button("⚡ Есептеу / Рассчитать", key="lab3_calc",
                 use_container_width=True, type="primary"):
        results = []
        error_occurred = False
        for i, (l, N, t) in enumerate(zip(all_l, all_N, all_t)):
            try:
                results.append(compute_lab3(l, N, t))
            except ZeroDivisionError as e:
                st.error(f"Опыт {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["g"] for r in results])
            st.session_state["lab3_results"] = results
            st.session_state["lab3_errors"]  = errors

    if "lab3_results" in st.session_state:
        results = st.session_state["lab3_results"]
        errors  = st.session_state["lab3_errors"]

        st.markdown("#### 📊 Нәтиже / Результат")
        metrics_row(results, errors, "g", "м/с²")

        txt_result = format_result_block(
            results, errors, format_lab3_result, "g", "м/с²")
        st.markdown(f'<div class="result-box">{txt_result}</div>',
                    unsafe_allow_html=True)

        txt_content = build_txt(
            "№3 Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау",
            results, errors, format_lab3_result, "g", "м/с²")
        st.download_button(
            label="💾 TXT экспорт",
            data=txt_content.encode("utf-8"),
            file_name="lab3_result.txt",
            mime="text/plain",
            key="lab3_download"
        )


# ─────────────────────────────────────────────────────────────────────────────

def page_lab4():
    st.markdown('<div class="lab-badge">Лаб. работа №4</div>', unsafe_allow_html=True)
    st.markdown("### №4 Беттік толқындардың таралу жылдамдығын анықтау")
    st.caption("Определение скорости распространения поверхностных волн")
    st.markdown('<div class="formula-box">υ = l / t</div>', unsafe_allow_html=True)

    if "lab4_count" not in st.session_state:
        st.session_state.lab4_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button("＋ Тәжірибе қосу", key="lab4_add", use_container_width=True):
            st.session_state.lab4_count += 1
    with col_remove:
        if st.button("－ Жою", key="lab4_remove", use_container_width=True,
                     disabled=st.session_state.lab4_count <= 1):
            st.session_state.lab4_count -= 1

    st.divider()

    tab_labels = [f"Тәжірибе {i+1}" for i in range(st.session_state.lab4_count)]
    tabs = st.tabs(tab_labels)

    all_t, all_l = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            t = experiment_number_input("t — уақыт (время)", "с",
                                        key=f"lab4_t_{i}", value=1.0)
            l = experiment_number_input("l — Ыдыстың ұзындығы (длина сосуда)", "м",
                                        key=f"lab4_l_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_t.append(t)
            all_l.append(l)

    st.divider()
    if st.button("⚡ Есептеу / Рассчитать", key="lab4_calc",
                 use_container_width=True, type="primary"):
        results = []
        error_occurred = False
        for i, (t, l) in enumerate(zip(all_t, all_l)):
            try:
                results.append(compute_lab4(t, l))
            except ZeroDivisionError as e:
                st.error(f"Опыт {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["v"] for r in results])
            st.session_state["lab4_results"] = results
            st.session_state["lab4_errors"]  = errors

    if "lab4_results" in st.session_state:
        results = st.session_state["lab4_results"]
        errors  = st.session_state["lab4_errors"]

        st.markdown("#### 📊 Нәтиже / Результат")
        metrics_row(results, errors, "v", "м/с")

        txt_result = format_result_block(
            results, errors, format_lab4_result, "υ", "м/с")
        st.markdown(f'<div class="result-box">{txt_result}</div>',
                    unsafe_allow_html=True)

        txt_content = build_txt(
            "№4 Беттік толқындардың таралу жылдамдығын анықтау",
            results, errors, format_lab4_result, "υ", "м/с")
        st.download_button(
            label="💾 TXT экспорт",
            data=txt_content.encode("utf-8"),
            file_name="lab4_result.txt",
            mime="text/plain",
            key="lab4_download"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  ГЛАВНЫЙ РОУТЕР
# ═══════════════════════════════════════════════════════════════════════════════

# ── Сайдбар ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px'>
        <div style='font-size:48px'>⚗️</div>
        <div style='font-size:18px; font-weight:700; color:#e8e8ff; margin-top:8px'>
            Физика<br>Зертханасы
        </div>
        <div style='font-size:11px; color:#6666aa; margin-top:4px'>
            лабораторный калькулятор
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='font-size:11px; color:#6666aa; font-weight:600;
                letter-spacing:1px; padding: 4px 8px 8px'>
        ЖҰМЫСТАР / РАБОТЫ
    </div>
    """, unsafe_allow_html=True)

    LABS = [
        ("№1  Теңүдемелі қозғалыс",    "lab1"),
        ("№2  Горизонталь лақтыру",     "lab2"),
        ("№3  Математикалық маятник",   "lab3"),
        ("№4  Беттік толқын жылдамдығы", "lab4"),
    ]

    if "active_lab" not in st.session_state:
        st.session_state.active_lab = "lab1"

    for label, key in LABS:
        is_active = st.session_state.active_lab == key
        btn_style = (
            "background:linear-gradient(135deg,#7c6bff,#a78bfa);"
            "color:white;border-radius:8px;"
        ) if is_active else ""
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_lab = key
            st.rerun()

    st.divider()
    st.markdown("""
    <div style='font-size:11px; color:#444466; text-align:center; padding:8px'>
        Физика зертханасы © 2025<br>
        Streamlit Cloud
    </div>
    """, unsafe_allow_html=True)

# ── Контент ──────────────────────────────────────────────────────────────────
if st.session_state.active_lab == "lab1":
    page_lab1()
elif st.session_state.active_lab == "lab2":
    page_lab2()
elif st.session_state.active_lab == "lab3":
    page_lab3()
elif st.session_state.active_lab == "lab4":
    page_lab4()
