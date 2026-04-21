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

import csv
import io
import math
import datetime
import streamlit as st

# ─────────────────────────────── Конфигурация страницы ───────────────────────
st.set_page_config(
    page_title="Физика Зертханасы — Лабораторный калькулятор",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  ПЕРЕВОДЫ / АУДАРМАЛАР
# ═══════════════════════════════════════════════════════════════════════════════

TRANSLATIONS = {
    "kk": {
        # Sidebar
        "app_title": "Физика\nЗертханасы",
        "app_subtitle": "зертханалық калькулятор",
        "nav_section": "ЖҰМЫСТАР",
        "footer": "Физика зертханасы © 2025\nStreamlit Cloud",
        "theme_label": "☀️ Күндізгі тақырып",
        "lang_label": "🌐 Тіл",
        # Buttons
        "add_exp": "＋ Тәжірибе қосу",
        "remove_exp": "－ Жою",
        "calculate": "⚡ Есептеу",
        "export_txt": "💾 TXT жүктеу",
        "export_csv": "📊 CSV жүктеу",
        # Results
        "result_header": "#### 📊 Нәтиже",
        "mean_label": "Орташа мән",
        "abs_err_label": "Δ (абс. қате)",
        "rel_err_label": "ε (салыст. қате)",
        "exp_label": "Тәжірибе",
        # Error summary
        "mean_text": "Орташа мән (среднее)",
        "abs_err_text": "Абсолютті қате (абс. погр.)",
        "rel_err_text": "Салыстырмалы қате (отн. погр.)",
        "count_text": "Тәжірибелер саны (кол-во опытов)",
        # Lab nav labels
        "lab1_nav": "№1  Теңүдемелі қозғалыс",
        "lab2_nav": "№2  Горизонталь лақтыру",
        "lab3_nav": "№3  Математикалық маятник",
        "lab4_nav": "№4  Беттік толқын жылдамдығы",
        # Lab 1
        "lab1_badge": "Зерт. жұмыс №1",
        "lab1_title": "№1 Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау",
        "lab1_caption": "Определение ускорения тела при равноускоренном движении",
        "lab1_S": "S — арақашықтық (расстояние)",
        "lab1_t": "t — қозғалыс уақыты (время)",
        # Lab 2
        "lab2_badge": "Зерт. жұмыс №2",
        "lab2_title": "№2 Горизонталь лақтырылған дененің қозғалысын зерделеу",
        "lab2_caption": "Изучение движения тела, брошенного горизонтально",
        "lab2_h": "h — биіктік (высота)",
        "lab2_l": "l — ұшу қашықтығы (дальность)",
        # Lab 3
        "lab3_badge": "Зерт. жұмыс №3",
        "lab3_title": "№3 Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау",
        "lab3_caption": "Определение ускорения свободного падения с помощью математического маятника",
        "lab3_l": "l — жіптің ұзындығы (длина нити)",
        "lab3_N": "N — тербеліс саны (число колебаний)",
        "lab3_t": "t — тербеліс уақыты (время)",
        # Lab 4
        "lab4_badge": "Зерт. жұмыс №4",
        "lab4_title": "№4 Беттік толқындардың таралу жылдамдығын анықтау",
        "lab4_caption": "Определение скорости распространения поверхностных волн",
        "lab4_t": "t — уақыт (время)",
        "lab4_l": "l — Ыдыстың ұзындығы (длина сосуда)",
        # CSV header
        "csv_exp_col": "Тәжірибе",
        "csv_mean_row": "Орташа мән",
        "csv_abs_row": "Абсолютті қате",
        "csv_rel_row": "Салыстырмалы қате (%)",
        # TXT header
        "txt_header": "Физика Зертханасы — Зертханалық калькулятор",
        "txt_results": "ТӘЖІРИБЕ НӘТИЖЕЛЕРІ / РЕЗУЛЬТАТЫ ОПЫТОВ:",
        "txt_summary": "ҚОРЫТЫНДЫ / ИТОГ:",
        "txt_date": "Күні",
    },
    "ru": {
        # Sidebar
        "app_title": "Физика\nЛаборатория",
        "app_subtitle": "лабораторный калькулятор",
        "nav_section": "РАБОТЫ",
        "footer": "Физика лаборатория © 2025\nStreamlit Cloud",
        "theme_label": "☀️ Дневная тема",
        "lang_label": "🌐 Язык",
        # Buttons
        "add_exp": "＋ Добавить опыт",
        "remove_exp": "－ Удалить",
        "calculate": "⚡ Рассчитать",
        "export_txt": "💾 Скачать TXT",
        "export_csv": "📊 Скачать CSV",
        # Results
        "result_header": "#### 📊 Результат",
        "mean_label": "Среднее",
        "abs_err_label": "Δ (абс. погр.)",
        "rel_err_label": "ε (отн. погр.)",
        "exp_label": "Опыт",
        # Error summary
        "mean_text": "Среднее значение (орташа мән)",
        "abs_err_text": "Абсолютная погрешность (абс. қате)",
        "rel_err_text": "Относительная погрешность (отн. қате)",
        "count_text": "Количество опытов (тәжірибелер саны)",
        # Lab nav labels
        "lab1_nav": "№1  Равноускоренное движение",
        "lab2_nav": "№2  Горизонтальный бросок",
        "lab3_nav": "№3  Математический маятник",
        "lab4_nav": "№4  Скорость поверхн. волн",
        # Lab 1
        "lab1_badge": "Лаб. работа №1",
        "lab1_title": "№1 Определение ускорения тела при равноускоренном движении",
        "lab1_caption": "Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау",
        "lab1_S": "S — расстояние (арақашықтық)",
        "lab1_t": "t — время движения (қозғалыс уақыты)",
        # Lab 2
        "lab2_badge": "Лаб. работа №2",
        "lab2_title": "№2 Изучение движения тела, брошенного горизонтально",
        "lab2_caption": "Горизонталь лақтырылған дененің қозғалысын зерделеу",
        "lab2_h": "h — высота (биіктік)",
        "lab2_l": "l — дальность (ұшу қашықтығы)",
        # Lab 3
        "lab3_badge": "Лаб. работа №3",
        "lab3_title": "№3 Определение ускорения свободного падения с помощью математического маятника",
        "lab3_caption": "Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау",
        "lab3_l": "l — длина нити (жіптің ұзындығы)",
        "lab3_N": "N — число колебаний (тербеліс саны)",
        "lab3_t": "t — время (тербеліс уақыты)",
        # Lab 4
        "lab4_badge": "Лаб. работа №4",
        "lab4_title": "№4 Определение скорости распространения поверхностных волн",
        "lab4_caption": "Беттік толқындардың таралу жылдамдығын анықтау",
        "lab4_t": "t — время (уақыт)",
        "lab4_l": "l — длина сосуда (ыдыстың ұзындығы)",
        # CSV header
        "csv_exp_col": "Опыт",
        "csv_mean_row": "Среднее",
        "csv_abs_row": "Абс. погрешность",
        "csv_rel_row": "Отн. погрешность (%)",
        # TXT header
        "txt_header": "Физика Лаборатория — Лабораторный калькулятор",
        "txt_results": "РЕЗУЛЬТАТЫ ОПЫТОВ / ТӘЖІРИБЕ НӘТИЖЕЛЕРІ:",
        "txt_summary": "ИТОГ / ҚОРЫТЫНДЫ:",
        "txt_date": "Дата",
    },
}


def t(key: str) -> str:
    """Возвращает перевод строки для текущего языка."""
    lang = st.session_state.get("lang", "kk")
    return TRANSLATIONS[lang].get(key, key)


# ═══════════════════════════════════════════════════════════════════════════════
#  ТЕМЫ / CSS
# ═══════════════════════════════════════════════════════════════════════════════

DARK_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #12121f 100%); }

  [data-testid="stSidebar"] {
    background: #16162a !important;
    border-right: 1px solid #2a2a48;
  }
  [data-testid="stSidebar"] * { color: #c8c8e8 !important; }

  h1, h2, h3 { color: #e8e8ff !important; }

  .exp-card {
    background: #1e1e35;
    border: 1px solid #2e2e50;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
  }
  .exp-card:hover { border-color: #7c6bff; }

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

  [data-testid="stMetric"] {
    background: #1e1e35;
    border: 1px solid #2e2e50;
    border-radius: 10px;
    padding: 12px 16px;
  }
  [data-testid="stMetricValue"] { color: #a78bfa !important; font-size: 1.4rem !important; }
  [data-testid="stMetricLabel"] { color: #8888aa !important; }

  .stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(124,107,255,0.3) !important;
  }

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

  hr { border-color: #2a2a48 !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }

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

  .warn-box {
    background: #2a1f3a;
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    color: #fbbf24;
    font-size: 13px;
    margin: 8px 0;
  }

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

  .input-label { padding-top: 8px; color: #c8c8e8; }
  .input-unit  { padding-top: 8px; color: #8888aa; }
</style>
"""

LIGHT_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background: linear-gradient(135deg, #f0f0ff 0%, #fafafa 100%); }

  [data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #ddd8ff;
  }
  [data-testid="stSidebar"] * { color: #2d2d5e !important; }

  h1, h2, h3 { color: #1a1a3e !important; }
  p, label, .stMarkdown { color: #2d2d5e; }

  .exp-card {
    background: #ffffff;
    border: 1px solid #d4ceff;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
    box-shadow: 0 2px 8px rgba(109,40,217,0.06);
  }
  .exp-card:hover { border-color: #7c6bff; }

  .result-box {
    background: #f5f3ff;
    border: 1px solid #c4b5fd;
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #3730a3;
    white-space: pre-wrap;
    line-height: 1.8;
  }

  [data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #d4ceff;
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: 0 1px 4px rgba(109,40,217,0.08);
  }
  [data-testid="stMetricValue"] { color: #6d28d9 !important; font-size: 1.4rem !important; }
  [data-testid="stMetricLabel"] { color: #7c7ca8 !important; }

  .stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(109,40,217,0.2) !important;
  }

  .stNumberInput input, .stTextInput input {
    background: #fafafa !important;
    border: 1px solid #d4ceff !important;
    border-radius: 8px !important;
    color: #1a1a3e !important;
    font-family: 'JetBrains Mono', monospace !important;
  }
  .stNumberInput input:focus, .stTextInput input:focus {
    border-color: #7c6bff !important;
    box-shadow: 0 0 0 2px rgba(124,107,255,0.15) !important;
  }

  hr { border-color: #ddd8ff !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }

  [data-testid="stTab"] { background: transparent !important; }
  button[data-baseweb="tab"] {
    background: #f0eeff !important;
    border-radius: 8px 8px 0 0 !important;
    color: #7c7ca8 !important;
    font-weight: 500 !important;
  }
  button[data-baseweb="tab"][aria-selected="true"] {
    background: #ede9ff !important;
    color: #6d28d9 !important;
    border-bottom: 2px solid #7c6bff !important;
  }

  .lab-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6d28d9, #8b5cf6);
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .warn-box {
    background: #fffbeb;
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    color: #92400e;
    font-size: 13px;
    margin: 8px 0;
  }

  .formula-box {
    background: #f5f3ff;
    border: 1px solid #c4b5fd;
    border-radius: 8px;
    padding: 10px 16px;
    font-family: 'JetBrains Mono', monospace;
    color: #6d28d9;
    font-size: 14px;
    margin: 8px 0 16px 0;
  }

  .input-label { padding-top: 8px; color: #2d2d5e; }
  .input-unit  { padding-top: 8px; color: #7c7ca8; }
</style>
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  ИНИЦИАЛИЗАЦИЯ SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state.lang = "kk"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "active_lab" not in st.session_state:
    st.session_state.active_lab = "lab1"


# ── Inject CSS ────────────────────────────────────────────────────────────────
if st.session_state.theme == "dark":
    st.markdown(DARK_CSS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)


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

def compute_lab1(S: float, t_val: float) -> dict:
    """a = 2S / t²"""
    if t_val == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    a = 2 * S / (t_val ** 2)
    return {"S": S, "t": t_val, "a": a}


def compute_lab2(h: float, l: float) -> dict:
    """υ₀ = l · √(g / 2h)"""
    if h <= 0:
        raise ZeroDivisionError("h должна быть > 0")
    v0 = l * math.sqrt(G / (2 * h))
    return {"h": h, "l": l, "v0": v0}


def compute_lab3(l: float, N: float, t_val: float) -> dict:
    """g = 4π²lN² / t²"""
    if t_val == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    g = 4 * math.pi ** 2 * l * N ** 2 / (t_val ** 2)
    return {"l": l, "N": N, "t": t_val, "g": g}


def compute_lab4(t_val: float, l: float) -> dict:
    """υ = l / t"""
    if t_val == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    v = l / t_val
    return {"t": t_val, "l": l, "v": v}


# ═══════════════════════════════════════════════════════════════════════════════
#  ФОРМАТИРОВАНИЕ РЕЗУЛЬТАТОВ
# ═══════════════════════════════════════════════════════════════════════════════

def format_lab1_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  S={r['S']:.3f} м,  "
            f"t={r['t']:.3f} с  →  a = {r['a']:.4f} м/с²")

def format_lab2_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  h={r['h']:.3f} м,  "
            f"l={r['l']:.3f} м  →  υ₀ = {r['v0']:.4f} м/с")

def format_lab3_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  l={r['l']:.3f} м,  "
            f"N={r['N']:.0f},  t={r['t']:.3f} с  →  g = {r['g']:.4f} м/с²")

def format_lab4_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  t={r['t']:.3f} с,  "
            f"l={r['l']:.3f} м  →  υ = {r['v']:.4f} м/с")


def format_errors(err: dict, symbol: str, unit: str) -> str:
    pct = err["rel_err"] * 100
    return (
        f"\n  📊 {t('mean_text')}:  {symbol}орт = {err['mean']:.4f} {unit}"
        f"\n  📐 {t('abs_err_text')}:  Δ{symbol} = {err['abs_err']:.4f} {unit}"
        f"\n  📏 {t('rel_err_text')}:  ε{symbol} = {pct:.2f} %"
        f"\n  🔢 {t('count_text')}:  n = {err['n']}"
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
        f"  {t('txt_header')}",
        f"  {lab_name}",
        f"  {t('txt_date')}: {now}",
        "═" * 60,
        "",
        f"  {t('txt_results')}",
        "  " + "─" * 50,
    ]
    for i, r in enumerate(results):
        lines.append(fmt_fn(i + 1, r))
    lines += [
        "",
        f"  {t('txt_summary')}",
        "  " + "─" * 50,
    ]
    if errors:
        lines.append(format_errors(errors, err_sym, err_unit))
    lines += ["", "═" * 60]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  ГЕНЕРАЦИЯ CSV
# ═══════════════════════════════════════════════════════════════════════════════

def build_csv(
    lab_name: str,
    results: list,
    errors: dict,
    col_headers: list,   # e.g. ["S (м)", "t (с)", "a (м/с²)"]
    value_keys: list,    # keys in result dict matching col_headers
    result_key: str,     # key of the main computed value
    result_unit: str,
) -> str:
    """Строит CSV-строку из результатов лабораторной работы."""
    output = io.StringIO()
    writer = csv.writer(output)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Мета-строки
    writer.writerow([t("txt_header")])
    writer.writerow([lab_name])
    writer.writerow([f"{t('txt_date')}: {now}"])
    writer.writerow([])

    # Заголовок таблицы
    writer.writerow([t("csv_exp_col")] + col_headers)

    # Строки опытов
    for i, r in enumerate(results):
        row = [i + 1] + [f"{r[k]:.4f}" for k in value_keys]
        writer.writerow(row)

    # Пустая строка перед итогом
    writer.writerow([])

    # Итог
    if errors:
        pct = errors["rel_err"] * 100
        writer.writerow([t("csv_mean_row")] + [""] * (len(col_headers) - 1) + [f"{errors['mean']:.4f} {result_unit}"])
        writer.writerow([t("csv_abs_row")]  + [""] * (len(col_headers) - 1) + [f"{errors['abs_err']:.4f} {result_unit}"])
        writer.writerow([t("csv_rel_row")]  + [""] * (len(col_headers) - 1) + [f"{pct:.2f}"])
        writer.writerow([t("count_text")]   + [""] * (len(col_headers) - 1) + [str(errors["n"])])

    return output.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
#  ВСПОМОГАТЕЛЬНЫЕ UI-КОМПОНЕНТЫ
# ═══════════════════════════════════════════════════════════════════════════════

def experiment_number_input(label: str, unit: str, key: str, value: float = 0.0):
    """Поле ввода числа с единицами измерения."""
    col_label, col_input, col_unit = st.columns([3, 2, 1])
    with col_label:
        st.markdown(f"<div class='input-label'>{label}</div>", unsafe_allow_html=True)
    with col_input:
        val = st.number_input("", value=value, format="%.4f",
                              key=key, label_visibility="collapsed")
    with col_unit:
        st.markdown(f"<div class='input-unit'>{unit}</div>", unsafe_allow_html=True)
    return val


def metrics_row(results: list, errors: dict, value_key: str, unit: str):
    """Строка метрик: среднее, Δ, ε."""
    if not results or not errors:
        return
    n_cols = min(4, len(results) + 3)
    cols = st.columns(n_cols)
    for i, r in enumerate(results[:n_cols - 3]):
        with cols[i]:
            st.metric(f"{t('exp_label')} {i+1}", f"{r[value_key]:.4f} {unit}")
    with cols[-3]:
        st.metric(t("mean_label"), f"{errors['mean']:.4f} {unit}")
    with cols[-2]:
        st.metric(t("abs_err_label"), f"{errors['abs_err']:.4f} {unit}")
    with cols[-1]:
        st.metric(t("rel_err_label"), f"{errors['rel_err']*100:.2f} %")


def export_buttons(txt_content: str, csv_content: str, file_base: str, key_prefix: str):
    """Два кнопки экспорта: TXT и CSV рядом."""
    col_txt, col_csv, _ = st.columns([1, 1, 4])
    with col_txt:
        st.download_button(
            label=t("export_txt"),
            data=txt_content.encode("utf-8"),
            file_name=f"{file_base}_result.txt",
            mime="text/plain",
            key=f"{key_prefix}_download_txt",
            use_container_width=True,
        )
    with col_csv:
        st.download_button(
            label=t("export_csv"),
            data=csv_content.encode("utf-8-sig"),  # utf-8-sig для корректного открытия в Excel
            file_name=f"{file_base}_result.csv",
            mime="text/csv",
            key=f"{key_prefix}_download_csv",
            use_container_width=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  СТРАНИЦЫ ЛАБОРАТОРНЫХ РАБОТ
# ═══════════════════════════════════════════════════════════════════════════════

def page_lab1():
    st.markdown(f'<div class="lab-badge">{t("lab1_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab1_title')}")
    st.caption(t("lab1_caption"))
    st.markdown('<div class="formula-box">a = 2S / t²</div>', unsafe_allow_html=True)

    if "lab1_count" not in st.session_state:
        st.session_state.lab1_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab1_add", use_container_width=True):
            st.session_state.lab1_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab1_remove", use_container_width=True,
                     disabled=st.session_state.lab1_count <= 1):
            st.session_state.lab1_count -= 1

    st.divider()

    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab1_count)]
    tabs = st.tabs(tab_labels)

    all_S, all_t = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            S = experiment_number_input(t("lab1_S"), "м", key=f"lab1_S_{i}", value=1.0)
            t_val = experiment_number_input(t("lab1_t"), "с", key=f"lab1_t_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_S.append(S)
            all_t.append(t_val)

    st.divider()
    if st.button(t("calculate"), key="lab1_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (S, t_val) in enumerate(zip(all_S, all_t)):
            try:
                results.append(compute_lab1(S, t_val))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["a"] for r in results])
            st.session_state["lab1_results"] = results
            st.session_state["lab1_errors"]  = errors

    if "lab1_results" in st.session_state:
        results = st.session_state["lab1_results"]
        errors  = st.session_state["lab1_errors"]

        st.markdown(t("result_header"))
        metrics_row(results, errors, "a", "м/с²")

        txt_result = format_result_block(results, errors, format_lab1_result, "a", "м/с²")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)

        txt_content = build_txt(t("lab1_title"), results, errors, format_lab1_result, "a", "м/с²")
        csv_content = build_csv(
            t("lab1_title"), results, errors,
            col_headers=["S (м)", "t (с)", "a (м/с²)"],
            value_keys=["S", "t", "a"],
            result_key="a", result_unit="м/с²",
        )
        export_buttons(txt_content, csv_content, "lab1", "lab1")


# ─────────────────────────────────────────────────────────────────────────────

def page_lab2():
    st.markdown(f'<div class="lab-badge">{t("lab2_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab2_title')}")
    st.caption(t("lab2_caption"))
    st.markdown('<div class="formula-box">υ₀ = l · √(g / 2h),  г/де g = 9.81 м/с²</div>',
                unsafe_allow_html=True)

    if "lab2_count" not in st.session_state:
        st.session_state.lab2_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab2_add", use_container_width=True):
            st.session_state.lab2_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab2_remove", use_container_width=True,
                     disabled=st.session_state.lab2_count <= 1):
            st.session_state.lab2_count -= 1

    st.divider()

    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab2_count)]
    tabs = st.tabs(tab_labels)

    all_h, all_l = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            h = experiment_number_input(t("lab2_h"), "м", key=f"lab2_h_{i}", value=1.0)
            l = experiment_number_input(t("lab2_l"), "м", key=f"lab2_l_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_h.append(h)
            all_l.append(l)

    st.divider()
    if st.button(t("calculate"), key="lab2_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (h, l) in enumerate(zip(all_h, all_l)):
            try:
                results.append(compute_lab2(h, l))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["v0"] for r in results])
            st.session_state["lab2_results"] = results
            st.session_state["lab2_errors"]  = errors

    if "lab2_results" in st.session_state:
        results = st.session_state["lab2_results"]
        errors  = st.session_state["lab2_errors"]

        st.markdown(t("result_header"))
        metrics_row(results, errors, "v0", "м/с")

        txt_result = format_result_block(results, errors, format_lab2_result, "υ₀", "м/с")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)

        txt_content = build_txt(t("lab2_title"), results, errors, format_lab2_result, "υ₀", "м/с")
        csv_content = build_csv(
            t("lab2_title"), results, errors,
            col_headers=["h (м)", "l (м)", "υ₀ (м/с)"],
            value_keys=["h", "l", "v0"],
            result_key="v0", result_unit="м/с",
        )
        export_buttons(txt_content, csv_content, "lab2", "lab2")


# ─────────────────────────────────────────────────────────────────────────────

def page_lab3():
    st.markdown(f'<div class="lab-badge">{t("lab3_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab3_title')}")
    st.caption(t("lab3_caption"))
    st.markdown('<div class="formula-box">g = 4π²lN² / t²</div>', unsafe_allow_html=True)

    if "lab3_count" not in st.session_state:
        st.session_state.lab3_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab3_add", use_container_width=True):
            st.session_state.lab3_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab3_remove", use_container_width=True,
                     disabled=st.session_state.lab3_count <= 1):
            st.session_state.lab3_count -= 1

    st.divider()

    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab3_count)]
    tabs = st.tabs(tab_labels)

    all_l, all_N, all_t = [], [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            l = experiment_number_input(t("lab3_l"), "м",   key=f"lab3_l_{i}", value=1.0)
            N = experiment_number_input(t("lab3_N"), "шт",  key=f"lab3_N_{i}", value=10.0)
            t_val = experiment_number_input(t("lab3_t"), "с", key=f"lab3_t_{i}", value=20.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_l.append(l)
            all_N.append(N)
            all_t.append(t_val)

    st.divider()
    if st.button(t("calculate"), key="lab3_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (l, N, t_val) in enumerate(zip(all_l, all_N, all_t)):
            try:
                results.append(compute_lab3(l, N, t_val))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["g"] for r in results])
            st.session_state["lab3_results"] = results
            st.session_state["lab3_errors"]  = errors

    if "lab3_results" in st.session_state:
        results = st.session_state["lab3_results"]
        errors  = st.session_state["lab3_errors"]

        st.markdown(t("result_header"))
        metrics_row(results, errors, "g", "м/с²")

        txt_result = format_result_block(results, errors, format_lab3_result, "g", "м/с²")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)

        txt_content = build_txt(t("lab3_title"), results, errors, format_lab3_result, "g", "м/с²")
        csv_content = build_csv(
            t("lab3_title"), results, errors,
            col_headers=["l (м)", "N (шт)", "t (с)", "g (м/с²)"],
            value_keys=["l", "N", "t", "g"],
            result_key="g", result_unit="м/с²",
        )
        export_buttons(txt_content, csv_content, "lab3", "lab3")


# ─────────────────────────────────────────────────────────────────────────────

def page_lab4():
    st.markdown(f'<div class="lab-badge">{t("lab4_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab4_title')}")
    st.caption(t("lab4_caption"))
    st.markdown('<div class="formula-box">υ = l / t</div>', unsafe_allow_html=True)

    if "lab4_count" not in st.session_state:
        st.session_state.lab4_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab4_add", use_container_width=True):
            st.session_state.lab4_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab4_remove", use_container_width=True,
                     disabled=st.session_state.lab4_count <= 1):
            st.session_state.lab4_count -= 1

    st.divider()

    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab4_count)]
    tabs = st.tabs(tab_labels)

    all_t, all_l = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            t_val = experiment_number_input(t("lab4_t"), "с", key=f"lab4_t_{i}", value=1.0)
            l = experiment_number_input(t("lab4_l"), "м", key=f"lab4_l_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_t.append(t_val)
            all_l.append(l)

    st.divider()
    if st.button(t("calculate"), key="lab4_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (t_val, l) in enumerate(zip(all_t, all_l)):
            try:
                results.append(compute_lab4(t_val, l))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["v"] for r in results])
            st.session_state["lab4_results"] = results
            st.session_state["lab4_errors"]  = errors

    if "lab4_results" in st.session_state:
        results = st.session_state["lab4_results"]
        errors  = st.session_state["lab4_errors"]

        st.markdown(t("result_header"))
        metrics_row(results, errors, "v", "м/с")

        txt_result = format_result_block(results, errors, format_lab4_result, "υ", "м/с")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)

        txt_content = build_txt(t("lab4_title"), results, errors, format_lab4_result, "υ", "м/с")
        csv_content = build_csv(
            t("lab4_title"), results, errors,
            col_headers=["t (с)", "l (м)", "υ (м/с)"],
            value_keys=["t", "l", "v"],
            result_key="v", result_unit="м/с",
        )
        export_buttons(txt_content, csv_content, "lab4", "lab4")


# ═══════════════════════════════════════════════════════════════════════════════
#  САЙДБАР
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # ── Логотип ──────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='text-align:center; padding: 20px 0 10px'>
        <div style='font-size:48px'>⚗️</div>
        <div style='font-size:18px; font-weight:700; margin-top:8px'>
            {t('app_title').replace(chr(10), '<br>')}
        </div>
        <div style='font-size:11px; opacity:0.6; margin-top:4px'>
            {t('app_subtitle')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Язык ─────────────────────────────────────────────────────────────────
    lang_choice = st.radio(
        t("lang_label"),
        options=["Қазақша 🇰🇿", "Русский 🇷🇺"],
        index=0 if st.session_state.lang == "kk" else 1,
        key="lang_radio",
        horizontal=True,
    )
    new_lang = "kk" if lang_choice.startswith("Қ") else "ru"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

    # ── Тема ─────────────────────────────────────────────────────────────────
    theme_on = st.toggle(
        t("theme_label"),
        value=(st.session_state.theme == "light"),
        key="theme_toggle",
    )
    new_theme = "light" if theme_on else "dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.divider()

    # ── Навигация ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-size:11px; opacity:0.55; font-weight:600;
                letter-spacing:1px; padding: 4px 8px 8px'>
        {t('nav_section')}
    </div>
    """, unsafe_allow_html=True)

    LABS = [
        (t("lab1_nav"), "lab1"),
        (t("lab2_nav"), "lab2"),
        (t("lab3_nav"), "lab3"),
        (t("lab4_nav"), "lab4"),
    ]

    for label, key in LABS:
        is_active = st.session_state.active_lab == key
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_lab = key
            st.rerun()

    st.divider()
    st.markdown(f"""
    <div style='font-size:11px; opacity:0.4; text-align:center; padding:8px'>
        {t('footer').replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  РОУТЕР
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.active_lab == "lab1":
    page_lab1()
elif st.session_state.active_lab == "lab2":
    page_lab2()
elif st.session_state.active_lab == "lab3":
    page_lab3()
elif st.session_state.active_lab == "lab4":
    page_lab4()
