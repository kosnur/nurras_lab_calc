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
        # Lab nav labels — 9 сынып
        "grade9_section": "9-СЫНЫП",
        "lab1_nav": "№1  Теңүдемелі қозғалыс",
        "lab2_nav": "№2  Горизонталь лақтыру",
        "lab3_nav": "№3  Математикалық маятник",
        "lab4_nav": "№4  Беттік толқын жылдамдығы",
        # Lab nav labels — 10 сынып
        "grade10_section": "10-СЫНЫП",
        "lab10_1_nav": "№1  Көлбеу науа бойымен үдеу",
        "lab10_2_nav": "№2  Ұшу қашықтығы мен бұрыш",
        "lab10_3_nav": "№3  Домалайтын дене қозғалысы",
        "lab10_4_nav": "№4  Күштерді қосу",
        "lab10_7_nav": "№7  ЭҚК және ішкі кедергі",
        # Lab nav labels — 11 сынып
        "grade11_section": "11-СЫНЫП",
        "lab11_1_nav": "№1  Трансформатор орамдары",
        "lab11_4_nav": "№4  Шынының сыну көрсеткіші",
        # Lab 1 (9 сынып)
        "lab1_badge": "9-сынып · Зерт. жұмыс №1",
        "lab1_title": "№1 Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау",
        "lab1_caption": "Определение ускорения тела при равноускоренном движении",
        "lab1_S": "S — арақашықтық (расстояние)",
        "lab1_t": "t — қозғалыс уақыты (время)",
        # Lab 2 (9 сынып)
        "lab2_badge": "9-сынып · Зерт. жұмыс №2",
        "lab2_title": "№2 Горизонталь лақтырылған дененің қозғалысын зерделеу",
        "lab2_caption": "Изучение движения тела, брошенного горизонтально",
        "lab2_h": "h — биіктік (высота)",
        "lab2_l": "l — ұшу қашықтығы (дальность)",
        # Lab 3 (9 сынып)
        "lab3_badge": "9-сынып · Зерт. жұмыс №3",
        "lab3_title": "№3 Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау",
        "lab3_caption": "Определение ускорения свободного падения с помощью математического маятника",
        "lab3_l": "l — жіптің ұзындығы (длина нити)",
        "lab3_N": "N — тербеліс саны (число колебаний)",
        "lab3_t": "t — тербеліс уақыты (время)",
        # Lab 4 (9 сынып)
        "lab4_badge": "9-сынып · Зерт. жұмыс №4",
        "lab4_title": "№4 Беттік толқындардың таралу жылдамдығын анықтау",
        "lab4_caption": "Определение скорости распространения поверхностных волн",
        "lab4_t": "t — уақыт (время)",
        "lab4_l": "l — Ыдыстың ұзындығы (длина сосуда)",
        # Lab 10-1
        "lab10_1_badge": "10-сынып · Зерт. жұмыс №1",
        "lab10_1_title": "№1 Көлбеу науа бойымен қозғалатын дененің үдеуін анықтау",
        "lab10_1_caption": "Определение ускорения тела, движущегося по наклонному лотку",
        "lab10_1_S": "S — арақашықтық (расстояние)",
        "lab10_1_t": "t — қозғалыс уақыты (время)",
        # Lab 10-2
        "lab10_2_badge": "10-сынып · Зерт. жұмыс №2",
        "lab10_2_title": "№2 Дененің ұшу қашықтығының лақтыру бұрышына тәуелділігін зерттеу",
        "lab10_2_caption": "Исследование зависимости дальности полёта тела от угла бросания",
        "lab10_2_angle": "Бұрыш (Угол бросания)",
        "lab10_2_l": "Ұшу қашықтығы (Дальность полёта), см",
        "lab10_2_mean": "Орташа мән (Среднее)",
        "lab10_2_graph_title": "Ұшу қашықтығы мен бұрыш тәуелділігі",
        "lab10_2_graph_x": "Бұрыш (°)",
        "lab10_2_graph_y": "Орташа қашықтық (см)",
        # Lab 10-3
        "lab10_3_badge": "10-сынып · Зерт. жұмыс №3",
        "lab10_3_title": "№3 Көлбеу науамен домалайтын дененің қозғалысын оқып үйрену",
        "lab10_3_caption": "Изучение движения тела, катящегося по наклонному лотку",
        "lab10_3_m": "m — масса (масса тела)",
        "lab10_3_R": "R — радиус (радиус тела)",
        "lab10_3_h": "h — биіктік (высота центра масс)",
        "lab10_3_H": "H — толық биіктік (полная высота)",
        "lab10_3_l": "l — ұзындық (длина лотка)",
        # Lab 10-4
        "lab10_4_badge": "10-сынып · Зерт. жұмыс №4",
        "lab10_4_title": "№4 Бір-біріне бұрыш жасай бағытталған күштерді қосу",
        "lab10_4_caption": "Сложение сил, направленных под углом друг к другу",
        "lab10_4_G": "G — ауырлық күш (сила тяжести), Н",
        "lab10_4_Fk1": "Fk1 — керілу күші 1 (сила натяжения 1), Н",
        "lab10_4_Fk2": "Fk2 — керілу күші 2 (сила натяжения 2), Н",
        "lab10_4_alpha": "α — бұрыш (угол между силами), °",
        # Lab 10-7
        "lab10_7_badge": "10-сынып · Зерт. жұмыс №7",
        "lab10_7_title": "№7 Ток көзінің электр қозғаушы күші мен ішкі кедергісін анықтау",
        "lab10_7_caption": "Определение ЭДС и внутреннего сопротивления источника тока",
        "lab10_7_I1": "I₁ — 1-ші Ток күші (Сила тока 1)",
        "lab10_7_U1": "U₁ — 1-ші Кернеу (Напряжение 1)",
        "lab10_7_I2": "I₂ — 2-ші Ток күші (Сила тока 2)",
        "lab10_7_U2": "U₂ — 2-ші Кернеу (Напряжение 2)",
        "lab10_7_graph_title": "Кернеу-Ток сипаттамасы (U-I)",
        "lab10_7_graph_x": "Ток күші I (А)",
        "lab10_7_graph_y": "Кернеу U (В)",
        # Lab 11-1
        "lab11_1_badge": "11-сынып · Зерт. жұмыс №1",
        "lab11_1_title": "№1 Трансформатор орамдарының санын анықтау",
        "lab11_1_caption": "Определение числа витков трансформатора",
        "lab11_1_calc1_header": "1-есептеу: N1 табу",
        "lab11_1_N2": "N2 — уақытша орамадағы орамдар саны",
        "lab11_1_U2_a": "U2 — уақытша орамадағы кернеу, В",
        "lab11_1_U1_a": "U1 — бірінші реттік орамадағы кернеу, В",
        "lab11_1_calc2_header": "2-есептеу: N2 табу",
        "lab11_1_N1": "N1жуық — бірінші реттік орамадағы орамдардың жуық саны",
        "lab11_1_U2_b": "U2 — екінші реттік орамадағы кернеу, В",
        "lab11_1_U1_b": "U1 — бірінші реттік орамадағы кернеу, В",
        # Lab 11-4
        "lab11_4_badge": "11-сынып · Зерт. жұмыс №4",
        "lab11_4_title": "№4 Шынының сыну көрсеткішін анықтау",
        "lab11_4_caption": "Определение показателя преломления стекла",
        "lab11_4_AD": "AD — түскен сәуленің жолы (путь падающего луча)",
        "lab11_4_CB": "CB — сынған сәуленің жолы (путь преломлённого луча)",
        "lab11_4_graph_title": "Сыну көрсеткіші (η) тәуелділігі",
        "lab11_4_graph_x": "Тәжірибе №",
        "lab11_4_graph_y": "η (сыну көрсеткіші)",
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
        # Lab nav labels — 9 класс
        "grade9_section": "9-КЛАСС",
        "lab1_nav": "№1  Равноускоренное движение",
        "lab2_nav": "№2  Горизонтальный бросок",
        "lab3_nav": "№3  Математический маятник",
        "lab4_nav": "№4  Скорость поверхн. волн",
        # Lab nav labels — 10 класс
        "grade10_section": "10-КЛАСС",
        "lab10_1_nav": "№1  Ускорение по наклон. лотку",
        "lab10_2_nav": "№2  Дальность и угол бросания",
        "lab10_3_nav": "№3  Катящееся тело",
        "lab10_4_nav": "№4  Сложение сил",
        "lab10_7_nav": "№7  ЭДС и внутр. сопротивление",
        # Lab nav labels — 11 класс
        "grade11_section": "11-КЛАСС",
        "lab11_1_nav": "№1  Витки трансформатора",
        "lab11_4_nav": "№4  Показатель преломления",
        # Lab 1 (9 класс)
        "lab1_badge": "9-класс · Лаб. работа №1",
        "lab1_title": "№1 Определение ускорения тела при равноускоренном движении",
        "lab1_caption": "Теңүдемелі қозғалыс кезіндегі дененің үдеуін анықтау",
        "lab1_S": "S — расстояние (арақашықтық)",
        "lab1_t": "t — время движения (қозғалыс уақыты)",
        # Lab 2 (9 класс)
        "lab2_badge": "9-класс · Лаб. работа №2",
        "lab2_title": "№2 Изучение движения тела, брошенного горизонтально",
        "lab2_caption": "Горизонталь лақтырылған дененің қозғалысын зерделеу",
        "lab2_h": "h — высота (биіктік)",
        "lab2_l": "l — дальность (ұшу қашықтығы)",
        # Lab 3 (9 класс)
        "lab3_badge": "9-класс · Лаб. работа №3",
        "lab3_title": "№3 Определение ускорения свободного падения с помощью математического маятника",
        "lab3_caption": "Математикалық маятниктің көмегімен еркін түсу үдеуін анықтау",
        "lab3_l": "l — длина нити (жіптің ұзындығы)",
        "lab3_N": "N — число колебаний (тербеліс саны)",
        "lab3_t": "t — время (тербеліс уақыты)",
        # Lab 4 (9 класс)
        "lab4_badge": "9-класс · Лаб. работа №4",
        "lab4_title": "№4 Определение скорости распространения поверхностных волн",
        "lab4_caption": "Беттік толқындардың таралу жылдамдығын анықтау",
        "lab4_t": "t — время (уақыт)",
        "lab4_l": "l — длина сосуда (ыдыстың ұзындығы)",
        # Lab 10-1
        "lab10_1_badge": "10-класс · Лаб. работа №1",
        "lab10_1_title": "№1 Определение ускорения тела, движущегося по наклонному лотку",
        "lab10_1_caption": "Көлбеу науа бойымен қозғалатын дененің үдеуін анықтау",
        "lab10_1_S": "S — расстояние (арақашықтық)",
        "lab10_1_t": "t — время движения (қозғалыс уақыты)",
        # Lab 10-2
        "lab10_2_badge": "10-класс · Лаб. работа №2",
        "lab10_2_title": "№2 Исследование зависимости дальности полёта тела от угла бросания",
        "lab10_2_caption": "Дененің ұшу қашықтығының лақтыру бұрышына тәуелділігін зерттеу",
        "lab10_2_angle": "Угол бросания",
        "lab10_2_l": "Дальность полёта (Ұшу қашықтығы), см",
        "lab10_2_mean": "Среднее (Орташа мән)",
        "lab10_2_graph_title": "Зависимость дальности полёта от угла",
        "lab10_2_graph_x": "Угол (°)",
        "lab10_2_graph_y": "Средняя дальность (см)",
        # Lab 10-3
        "lab10_3_badge": "10-класс · Лаб. работа №3",
        "lab10_3_title": "№3 Изучение движения тела, катящегося по наклонному лотку",
        "lab10_3_caption": "Көлбеу науамен домалайтын дененің қозғалысын оқып үйрену",
        "lab10_3_m": "m — масса тела",
        "lab10_3_R": "R — радиус тела",
        "lab10_3_h": "h — высота центра масс",
        "lab10_3_H": "H — полная высота",
        "lab10_3_l": "l — длина лотка",
        # Lab 10-4
        "lab10_4_badge": "10-класс · Лаб. работа №4",
        "lab10_4_title": "№4 Сложение сил, направленных под углом друг к другу",
        "lab10_4_caption": "Бір-біріне бұрыш жасай бағытталған күштерді қосу",
        "lab10_4_G": "G — сила тяжести, Н",
        "lab10_4_Fk1": "Fk1 — сила натяжения 1, Н",
        "lab10_4_Fk2": "Fk2 — сила натяжения 2, Н",
        "lab10_4_alpha": "α — угол между силами, °",
        # Lab 10-7
        "lab10_7_badge": "10-класс · Лаб. работа №7",
        "lab10_7_title": "№7 Определение ЭДС и внутреннего сопротивления источника тока",
        "lab10_7_caption": "Ток көзінің электр қозғаушы күші мен ішкі кедергісін анықтау",
        "lab10_7_I1": "I₁ — Сила тока 1 (1-ші Ток күші)",
        "lab10_7_U1": "U₁ — Напряжение 1 (1-ші Кернеу)",
        "lab10_7_I2": "I₂ — Сила тока 2 (2-ші Ток күші)",
        "lab10_7_U2": "U₂ — Напряжение 2 (2-ші Кернеу)",
        "lab10_7_graph_title": "Характеристика U-I источника тока",
        "lab10_7_graph_x": "Ток I (А)",
        "lab10_7_graph_y": "Напряжение U (В)",
        # Lab 11-1
        "lab11_1_badge": "11-класс · Лаб. работа №1",
        "lab11_1_title": "№1 Определение числа витков трансформатора",
        "lab11_1_caption": "Трансформатор орамдарының санын анықтау",
        "lab11_1_calc1_header": "Расчёт 1: Найти N1",
        "lab11_1_N2": "N2 — число витков временной обмотки",
        "lab11_1_U2_a": "U2 — напряжение временной обмотки, В",
        "lab11_1_U1_a": "U1 — напряжение первичной обмотки, В",
        "lab11_1_calc2_header": "Расчёт 2: Найти N2",
        "lab11_1_N1": "N1прибл — приближённое число витков первичной обмотки",
        "lab11_1_U2_b": "U2 — напряжение вторичной обмотки, В",
        "lab11_1_U1_b": "U1 — напряжение первичной обмотки, В",
        # Lab 11-4
        "lab11_4_badge": "11-класс · Лаб. работа №4",
        "lab11_4_title": "№4 Определение показателя преломления стекла",
        "lab11_4_caption": "Шынының сыну көрсеткішін анықтау",
        "lab11_4_AD": "AD — путь падающего луча (түскен сәуленің жолы)",
        "lab11_4_CB": "CB — путь преломлённого луча (сынған сәуленің жолы)",
        "lab11_4_graph_title": "Зависимость показателя преломления (η)",
        "lab11_4_graph_x": "Опыт №",
        "lab11_4_graph_y": "η (показатель преломления)",
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


# ── 10 класс ──────────────────────────────────────────────────────────────────

def compute_lab10_1(S: float, t_val: float) -> dict:
    """a = 2S / t²  (наклонный лоток)"""
    if t_val == 0:
        raise ZeroDivisionError("t не может быть равно нулю")
    a = 2 * S / (t_val ** 2)
    return {"S": S, "t": t_val, "a": a}


def compute_lab10_3(m: float, R: float, h: float, H: float, l: float) -> dict:
    """J = m·R²·(4hH − l²) / l²"""
    if l == 0:
        raise ZeroDivisionError("l не может быть равно нулю")
    J = m * R ** 2 * (4 * h * H - l ** 2) / (l ** 2)
    return {"m": m, "R": R, "h": h, "H": H, "l": l, "J": J}


def compute_lab10_4(Fk1: float, Fk2: float, alpha_deg: float) -> dict:
    """R = √(Fk1² + Fk2² − 2·Fk1·Fk2·cos α)"""
    alpha_rad = math.radians(alpha_deg)
    R = math.sqrt(Fk1 ** 2 + Fk2 ** 2 - 2 * Fk1 * Fk2 * math.cos(alpha_rad))
    return {"Fk1": Fk1, "Fk2": Fk2, "alpha": alpha_deg, "R": R}


# ── 11 класс ──────────────────────────────────────────────────────────────────

def compute_lab11_1_N1(N2: float, U2: float, U1: float) -> dict:
    """N1 = U1·N2 / U2"""
    if U2 == 0:
        raise ZeroDivisionError("U2 не может быть равно нулю")
    N1 = U1 * N2 / U2
    return {"N2": N2, "U2": U2, "U1": U1, "N1": N1}


def compute_lab11_1_N2(N1: float, U2: float, U1: float) -> dict:
    """N2 = U2·N1 / U1"""
    if U1 == 0:
        raise ZeroDivisionError("U1 не может быть равно нулю")
    N2 = U2 * N1 / U1
    return {"N1": N1, "U2": U2, "U1": U1, "N2": N2}


def compute_lab10_7(I1: float, U1: float, I2: float, U2: float) -> dict:
    """ε = (U2·I1 − U1·I2) / (I1 − I2)  и  r = (U1 − U2) / (I2 − I1)"""
    if I1 == I2:
        raise ZeroDivisionError("Токтың мәндері тең болмауы керек — I1 және I2 бірдей болмауы керек")
    eps = (U2 * I1 - U1 * I2) / (I1 - I2)
    r   = (U1 - U2) / (I2 - I1)
    return {"I1": I1, "U1": U1, "I2": I2, "U2": U2, "eps": eps, "r": r}


def compute_lab11_4(AD: float, CB: float) -> dict:
    """η = AD / CB"""
    if CB == 0:
        raise ZeroDivisionError("CB нульге тең болмауы керек")
    eta = AD / CB
    return {"AD": AD, "CB": CB, "eta": eta}


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

def format_lab10_1_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  S={r['S']:.3f} м,  "
            f"t={r['t']:.3f} с  →  a = {r['a']:.4f} м/с²")

def format_lab10_3_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  m={r['m']:.3f} кг, R={r['R']:.3f} м, "
            f"h={r['h']:.3f} м, H={r['H']:.3f} м, l={r['l']:.3f} м  →  J = {r['J']:.4f} кг·м²")

def format_lab10_4_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  Fk1={r['Fk1']:.3f} Н, Fk2={r['Fk2']:.3f} Н, "
            f"α={r['alpha']:.1f}°  →  R = {r['R']:.4f} Н")

def format_lab10_7_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  I1={r['I1']:.4f} А, U1={r['U1']:.4f} В,  "
            f"I2={r['I2']:.4f} А, U2={r['U2']:.4f} В  →  ε = {r['eps']:.4f} В,  r = {r['r']:.4f} Ом")

def format_lab11_4_result(idx: int, r: dict) -> str:
    return (f"  {t('exp_label')} {idx}:  AD={r['AD']:.4f},  CB={r['CB']:.4f}  →  η = {r['eta']:.4f}")


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


# ─────────────────────────────────────────────────────────────────────────────
# 10 класс
# ─────────────────────────────────────────────────────────────────────────────

def page_lab10_1():
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#059669,#34d399)">{t("lab10_1_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab10_1_title')}")
    st.caption(t("lab10_1_caption"))
    st.markdown('<div class="formula-box">a = 2S / t²</div>', unsafe_allow_html=True)

    if "lab10_1_count" not in st.session_state:
        st.session_state.lab10_1_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab10_1_add", use_container_width=True):
            st.session_state.lab10_1_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab10_1_remove", use_container_width=True,
                     disabled=st.session_state.lab10_1_count <= 1):
            st.session_state.lab10_1_count -= 1

    st.divider()
    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab10_1_count)]
    tabs = st.tabs(tab_labels)
    all_S, all_t = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            S = experiment_number_input(t("lab10_1_S"), "м", key=f"lab10_1_S_{i}", value=1.0)
            t_val = experiment_number_input(t("lab10_1_t"), "с", key=f"lab10_1_t_{i}", value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_S.append(S)
            all_t.append(t_val)

    st.divider()
    if st.button(t("calculate"), key="lab10_1_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (S, t_val) in enumerate(zip(all_S, all_t)):
            try:
                results.append(compute_lab10_1(S, t_val))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["a"] for r in results])
            st.session_state["lab10_1_results"] = results
            st.session_state["lab10_1_errors"]  = errors

    if "lab10_1_results" in st.session_state:
        results = st.session_state["lab10_1_results"]
        errors  = st.session_state["lab10_1_errors"]
        st.markdown(t("result_header"))
        metrics_row(results, errors, "a", "м/с²")
        txt_result = format_result_block(results, errors, format_lab10_1_result, "a", "м/с²")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)
        txt_content = build_txt(t("lab10_1_title"), results, errors, format_lab10_1_result, "a", "м/с²")
        csv_content = build_csv(
            t("lab10_1_title"), results, errors,
            col_headers=["S (м)", "t (с)", "a (м/с²)"],
            value_keys=["S", "t", "a"],
            result_key="a", result_unit="м/с²",
        )
        export_buttons(txt_content, csv_content, "lab10_1", "lab10_1")


# ─────────────────────────────────────────────────────────────────────────────

def page_lab10_2():
    import json
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#059669,#34d399)">{t("lab10_2_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab10_2_title')}")
    st.caption(t("lab10_2_caption"))
    st.markdown('<div class="formula-box">l̄ = (l₁+l₂+l₃+l₄+l₅) / 5  →  График: l̄(α)</div>', unsafe_allow_html=True)

    if "lab10_2_angles" not in st.session_state:
        st.session_state.lab10_2_angles = [30.0]
        st.session_state.lab10_2_rows   = [[0.0, 0.0, 0.0, 0.0, 0.0]]

    col_add2, col_rem2, _ = st.columns([1, 1, 6])
    with col_add2:
        if st.button(t("add_exp"), key="lab10_2_add", use_container_width=True):
            st.session_state.lab10_2_angles.append(45.0)
            st.session_state.lab10_2_rows.append([0.0, 0.0, 0.0, 0.0, 0.0])
    with col_rem2:
        if st.button(t("remove_exp"), key="lab10_2_remove", use_container_width=True,
                     disabled=len(st.session_state.lab10_2_angles) <= 1):
            st.session_state.lab10_2_angles.pop()
            st.session_state.lab10_2_rows.pop()

    st.divider()
    angle_labels = [f"{t('exp_label')} {i+1}" for i in range(len(st.session_state.lab10_2_angles))]
    tabs = st.tabs(angle_labels)
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            angle_val = st.number_input(
                t("lab10_2_angle") + " (°)",
                value=st.session_state.lab10_2_angles[i],
                min_value=0.0, max_value=90.0, step=5.0,
                key=f"lab10_2_angle_{i}",
            )
            st.session_state.lab10_2_angles[i] = angle_val
            st.markdown(f"**{t('lab10_2_l')}:**")
            cols = st.columns(5)
            for j in range(5):
                with cols[j]:
                    val = st.number_input(
                        f"l{j+1}", value=st.session_state.lab10_2_rows[i][j],
                        min_value=0.0, step=0.1, format="%.2f",
                        key=f"lab10_2_l_{i}_{j}", label_visibility="visible",
                    )
                    st.session_state.lab10_2_rows[i][j] = val
            mean_val = sum(st.session_state.lab10_2_rows[i]) / 5
            st.metric(t("lab10_2_mean"), f"{mean_val:.2f} см")
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    if st.button(t("calculate"), key="lab10_2_calc", use_container_width=True, type="primary"):
        angles = list(st.session_state.lab10_2_angles)
        means  = [sum(row) / 5 for row in st.session_state.lab10_2_rows]
        st.session_state["lab10_2_plot_angles"] = angles
        st.session_state["lab10_2_plot_means"]  = means

    if "lab10_2_plot_angles" in st.session_state:
        angles = st.session_state["lab10_2_plot_angles"]
        means  = st.session_state["lab10_2_plot_means"]
        st.markdown(t("result_header"))
        import pandas as pd
        chart_data = pd.DataFrame({t("lab10_2_graph_x"): angles, t("lab10_2_graph_y"): means})
        chart_data = chart_data.sort_values(t("lab10_2_graph_x"))
        st.line_chart(chart_data.set_index(t("lab10_2_graph_x")),
                      use_container_width=True)
        # Таблица итогов
        rows_html = "".join(
            f"<tr><td>{a:.1f}°</td><td>{m:.2f} см</td></tr>"
            for a, m in zip(angles, means)
        )
        st.markdown(
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<tr><th style='text-align:left;padding:6px'>{t('lab10_2_graph_x')}</th>"
            f"<th style='text-align:left;padding:6px'>{t('lab10_2_graph_y')}</th></tr>"
            f"{rows_html}</table>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────

def page_lab10_3():
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#059669,#34d399)">{t("lab10_3_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab10_3_title')}")
    st.caption(t("lab10_3_caption"))
    st.markdown('<div class="formula-box">J = m·R²·(4h·H − l²) / l²</div>', unsafe_allow_html=True)

    if "lab10_3_count" not in st.session_state:
        st.session_state.lab10_3_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab10_3_add", use_container_width=True):
            st.session_state.lab10_3_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab10_3_remove", use_container_width=True,
                     disabled=st.session_state.lab10_3_count <= 1):
            st.session_state.lab10_3_count -= 1

    st.divider()
    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab10_3_count)]
    tabs = st.tabs(tab_labels)
    all_m, all_R, all_h, all_H, all_l = [], [], [], [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            m_v   = experiment_number_input(t("lab10_3_m"), "кг",  key=f"lab10_3_m_{i}",  value=0.1)
            R_v   = experiment_number_input(t("lab10_3_R"), "м",   key=f"lab10_3_R_{i}",  value=0.05)
            h_v   = experiment_number_input(t("lab10_3_h"), "м",   key=f"lab10_3_h_{i}",  value=0.1)
            H_v   = experiment_number_input(t("lab10_3_H"), "м",   key=f"lab10_3_H_{i}",  value=0.5)
            l_v   = experiment_number_input(t("lab10_3_l"), "м",   key=f"lab10_3_l_{i}",  value=1.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_m.append(m_v); all_R.append(R_v); all_h.append(h_v)
            all_H.append(H_v); all_l.append(l_v)

    st.divider()
    if st.button(t("calculate"), key="lab10_3_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (m, R, h, H, l) in enumerate(zip(all_m, all_R, all_h, all_H, all_l)):
            try:
                results.append(compute_lab10_3(m, R, h, H, l))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["J"] for r in results])
            st.session_state["lab10_3_results"] = results
            st.session_state["lab10_3_errors"]  = errors

    if "lab10_3_results" in st.session_state:
        results = st.session_state["lab10_3_results"]
        errors  = st.session_state["lab10_3_errors"]
        st.markdown(t("result_header"))
        metrics_row(results, errors, "J", "кг·м²")
        txt_result = format_result_block(results, errors, format_lab10_3_result, "J", "кг·м²")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)
        txt_content = build_txt(t("lab10_3_title"), results, errors, format_lab10_3_result, "J", "кг·м²")
        csv_content = build_csv(
            t("lab10_3_title"), results, errors,
            col_headers=["m (кг)", "R (м)", "h (м)", "H (м)", "l (м)", "J (кг·м²)"],
            value_keys=["m", "R", "h", "H", "l", "J"],
            result_key="J", result_unit="кг·м²",
        )
        export_buttons(txt_content, csv_content, "lab10_3", "lab10_3")


# ─────────────────────────────────────────────────────────────────────────────

def page_lab10_4():
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#059669,#34d399)">{t("lab10_4_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab10_4_title')}")
    st.caption(t("lab10_4_caption"))
    st.markdown('<div class="formula-box">R = √(Fk1² + Fk2² − 2·Fk1·Fk2·cos α)</div>', unsafe_allow_html=True)

    if "lab10_4_count" not in st.session_state:
        st.session_state.lab10_4_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab10_4_add", use_container_width=True):
            st.session_state.lab10_4_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab10_4_remove", use_container_width=True,
                     disabled=st.session_state.lab10_4_count <= 1):
            st.session_state.lab10_4_count -= 1

    st.divider()
    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab10_4_count)]
    tabs = st.tabs(tab_labels)
    all_Fk1, all_Fk2, all_alpha = [], [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            G_v     = experiment_number_input(t("lab10_4_G"),  "Н", key=f"lab10_4_G_{i}",     value=1.0)
            Fk1_v   = experiment_number_input(t("lab10_4_Fk1"),"Н", key=f"lab10_4_Fk1_{i}",  value=1.0)
            Fk2_v   = experiment_number_input(t("lab10_4_Fk2"),"Н", key=f"lab10_4_Fk2_{i}",  value=1.0)
            alpha_v = experiment_number_input(t("lab10_4_alpha"),"°",key=f"lab10_4_alpha_{i}",value=60.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_Fk1.append(Fk1_v); all_Fk2.append(Fk2_v); all_alpha.append(alpha_v)

    st.divider()
    if st.button(t("calculate"), key="lab10_4_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (Fk1, Fk2, alpha) in enumerate(zip(all_Fk1, all_Fk2, all_alpha)):
            try:
                results.append(compute_lab10_4(Fk1, Fk2, alpha))
            except Exception as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["R"] for r in results])
            st.session_state["lab10_4_results"] = results
            st.session_state["lab10_4_errors"]  = errors

    if "lab10_4_results" in st.session_state:
        results = st.session_state["lab10_4_results"]
        errors  = st.session_state["lab10_4_errors"]
        st.markdown(t("result_header"))
        metrics_row(results, errors, "R", "Н")
        txt_result = format_result_block(results, errors, format_lab10_4_result, "R", "Н")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)
        txt_content = build_txt(t("lab10_4_title"), results, errors, format_lab10_4_result, "R", "Н")
        csv_content = build_csv(
            t("lab10_4_title"), results, errors,
            col_headers=["Fk1 (Н)", "Fk2 (Н)", "α (°)", "R (Н)"],
            value_keys=["Fk1", "Fk2", "alpha", "R"],
            result_key="R", result_unit="Н",
        )
        export_buttons(txt_content, csv_content, "lab10_4", "lab10_4")


# ─────────────────────────────────────────────────────────────────────────────
# 11 класс
# ─────────────────────────────────────────────────────────────────────────────

def page_lab11_1():
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#b45309,#f59e0b)">{t("lab11_1_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab11_1_title')}")
    st.caption(t("lab11_1_caption"))
    st.markdown('<div class="formula-box">N1 = U1·N2 / U2 &nbsp;|&nbsp; N2 = U2·N1 / U1</div>', unsafe_allow_html=True)

    st.markdown(f"#### {t('lab11_1_calc1_header')}")
    st.markdown('<div class="exp-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        N2_a  = experiment_number_input(t("lab11_1_N2"),  "шт", key="lab11_1_N2_a",  value=100.0)
        U2_a  = experiment_number_input(t("lab11_1_U2_a"),"В",  key="lab11_1_U2_a",  value=12.0)
        U1_a  = experiment_number_input(t("lab11_1_U1_a"),"В",  key="lab11_1_U1_a",  value=220.0)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(t("calculate") + " → N1", key="lab11_1_calc1", use_container_width=True, type="primary"):
        try:
            res = compute_lab11_1_N1(N2_a, U2_a, U1_a)
            st.session_state["lab11_1_res1"] = res
        except ZeroDivisionError as e:
            st.error(str(e))

    if "lab11_1_res1" in st.session_state:
        r = st.session_state["lab11_1_res1"]
        c1, c2, c3 = st.columns(3)
        c1.metric("N2", f"{r['N2']:.0f} шт")
        c2.metric("U1 / U2", f"{r['U1']:.1f} / {r['U2']:.1f} В")
        c3.metric("N1жуық", f"{r['N1']:.1f} шт")
        st.markdown(f'<div class="result-box">  N1жуық = U1·N2 / U2 = {r["U1"]:.1f}·{r["N2"]:.0f} / {r["U2"]:.1f} = {r["N1"]:.2f} шт</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown(f"#### {t('lab11_1_calc2_header')}")
    st.markdown('<div class="exp-card">', unsafe_allow_html=True)
    N1_b  = experiment_number_input(t("lab11_1_N1"),  "шт", key="lab11_1_N1_b",  value=1833.0)
    U2_b  = experiment_number_input(t("lab11_1_U2_b"),"В",  key="lab11_1_U2_b",  value=12.0)
    U1_b  = experiment_number_input(t("lab11_1_U1_b"),"В",  key="lab11_1_U1_b",  value=220.0)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(t("calculate") + " → N2", key="lab11_1_calc2", use_container_width=True, type="primary"):
        try:
            res = compute_lab11_1_N2(N1_b, U2_b, U1_b)
            st.session_state["lab11_1_res2"] = res
        except ZeroDivisionError as e:
            st.error(str(e))

    if "lab11_1_res2" in st.session_state:
        r = st.session_state["lab11_1_res2"]
        c1, c2, c3 = st.columns(3)
        c1.metric("N1жуық", f"{r['N1']:.0f} шт")
        c2.metric("U2 / U1", f"{r['U2']:.1f} / {r['U1']:.1f} В")
        c3.metric("N2жуық", f"{r['N2']:.1f} шт")
        st.markdown(f'<div class="result-box">  N2жуық = U2·N1 / U1 = {r["U2"]:.1f}·{r["N1"]:.0f} / {r["U1"]:.1f} = {r["N2"]:.2f} шт</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────

def page_lab10_7():
    import pandas as pd
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#059669,#34d399)">{t("lab10_7_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab10_7_title')}")
    st.caption(t("lab10_7_caption"))
    st.markdown(
        '<div class="formula-box">'
        'ε = (U₂·I₁ − U₁·I₂) / (I₁ − I₂) &nbsp;|&nbsp; r = (U₁ − U₂) / (I₂ − I₁)'
        '</div>',
        unsafe_allow_html=True,
    )

    if "lab10_7_count" not in st.session_state:
        st.session_state.lab10_7_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab10_7_add", use_container_width=True):
            st.session_state.lab10_7_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab10_7_remove", use_container_width=True,
                     disabled=st.session_state.lab10_7_count <= 1):
            st.session_state.lab10_7_count -= 1

    st.divider()
    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab10_7_count)]
    tabs = st.tabs(tab_labels)
    all_I1, all_U1, all_I2, all_U2 = [], [], [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Өлшем 1 / Измерение 1**")
                I1_v = experiment_number_input(t("lab10_7_I1"), "А", key=f"lab10_7_I1_{i}", value=1.0)
                U1_v = experiment_number_input(t("lab10_7_U1"), "В", key=f"lab10_7_U1_{i}", value=4.0)
            with col_b:
                st.markdown("**Өлшем 2 / Измерение 2**")
                I2_v = experiment_number_input(t("lab10_7_I2"), "А", key=f"lab10_7_I2_{i}", value=2.0)
                U2_v = experiment_number_input(t("lab10_7_U2"), "В", key=f"lab10_7_U2_{i}", value=3.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_I1.append(I1_v); all_U1.append(U1_v)
            all_I2.append(I2_v); all_U2.append(U2_v)

    st.divider()
    if st.button(t("calculate"), key="lab10_7_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (I1, U1_, I2, U2_) in enumerate(zip(all_I1, all_U1, all_I2, all_U2)):
            try:
                results.append(compute_lab10_7(I1, U1_, I2, U2_))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors_eps = calc_errors([r["eps"] for r in results])
            errors_r   = calc_errors([r["r"]   for r in results])
            st.session_state["lab10_7_results"]    = results
            st.session_state["lab10_7_errors_eps"] = errors_eps
            st.session_state["lab10_7_errors_r"]   = errors_r

    if "lab10_7_results" in st.session_state:
        results    = st.session_state["lab10_7_results"]
        errors_eps = st.session_state["lab10_7_errors_eps"]
        errors_r   = st.session_state["lab10_7_errors_r"]

        st.markdown(t("result_header"))

        # Метрики — ε
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ε орт (В)", f"{errors_eps['mean']:.4f}" if errors_eps else "—")
        col2.metric("Δε (В)",    f"{errors_eps['abs_err']:.4f}" if errors_eps else "—")
        col3.metric("r орт (Ом)", f"{errors_r['mean']:.4f}" if errors_r else "—")
        col4.metric("Δr (Ом)",    f"{errors_r['abs_err']:.4f}" if errors_r else "—")

        txt_result = format_result_block(results, errors_eps, format_lab10_7_result, "ε", "В")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)

        # ── График U-I ────────────────────────────────────────────────────────
        st.markdown(f"#### 📈 {t('lab10_7_graph_title')}")
        # Теоретическая прямая U = ε − r·I  +  все экспериментальные точки
        if errors_eps and errors_r:
            eps_mean = errors_eps["mean"]
            r_mean   = errors_r["mean"]

            # Все экспериментальные точки из всех опытов
            exp_points_I = [r["I1"] for r in results] + [r["I2"] for r in results]
            exp_points_U = [r["U1"] for r in results] + [r["U2"] for r in results]

            I_min = max(0.0, min(exp_points_I) * 0.8)
            I_max = max(exp_points_I) * 1.2
            I_line = [I_min + (I_max - I_min) * k / 60 for k in range(61)]
            U_line = [eps_mean - r_mean * I for I in I_line]

            theory_label = "U = ε − r·I"
            exp_label    = "Тәжірибе / Опыт"

            df_theory = pd.DataFrame({
                t("lab10_7_graph_x"): I_line,
                theory_label: U_line,
            }).set_index(t("lab10_7_graph_x"))

            exp_pairs = sorted(zip(exp_points_I, exp_points_U))
            df_exp = pd.DataFrame({
                t("lab10_7_graph_x"): [p[0] for p in exp_pairs],
                exp_label:            [p[1] for p in exp_pairs],
            }).set_index(t("lab10_7_graph_x"))

            df_final = df_theory.join(df_exp, how="outer").sort_index()
            st.line_chart(df_final, use_container_width=True)
            st.caption(
                f"ε = {eps_mean:.4f} В,  r = {r_mean:.4f} Ом  →  U = ε − r·I  "
                f"| Тәжірибелер саны: {len(results)}, өлшем нүктелері: {len(exp_points_I)}"
            )


        # Экспорт
        txt_content = build_txt(t("lab10_7_title"), results, errors_eps, format_lab10_7_result, "ε", "В")
        csv_content = build_csv(
            t("lab10_7_title"), results, errors_eps,
            col_headers=["I1 (А)", "U1 (В)", "I2 (А)", "U2 (В)", "ε (В)", "r (Ом)"],
            value_keys=["I1", "U1", "I2", "U2", "eps", "r"],
            result_key="eps", result_unit="В",
        )
        export_buttons(txt_content, csv_content, "lab10_7", "lab10_7")


# ─────────────────────────────────────────────────────────────────────────────

def page_lab11_4():
    import pandas as pd
    st.markdown(f'<div class="lab-badge" style="background:linear-gradient(135deg,#b45309,#f59e0b)">{t("lab11_4_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### {t('lab11_4_title')}")
    st.caption(t("lab11_4_caption"))
    st.markdown('<div class="formula-box">η = AD / CB</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="warn-box">AD — түскен сәуленің нормальдан горизонталь жол ұзындығы; '
        'CB — сынған сәуленің нормальдан горизонталь жол ұзындығы.</div>',
        unsafe_allow_html=True,
    )

    if "lab11_4_count" not in st.session_state:
        st.session_state.lab11_4_count = 1

    col_add, col_remove, _ = st.columns([1, 1, 6])
    with col_add:
        if st.button(t("add_exp"), key="lab11_4_add", use_container_width=True):
            st.session_state.lab11_4_count += 1
    with col_remove:
        if st.button(t("remove_exp"), key="lab11_4_remove", use_container_width=True,
                     disabled=st.session_state.lab11_4_count <= 1):
            st.session_state.lab11_4_count -= 1

    st.divider()
    tab_labels = [f"{t('exp_label')} {i+1}" for i in range(st.session_state.lab11_4_count)]
    tabs = st.tabs(tab_labels)
    all_AD, all_CB = [], []
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown('<div class="exp-card">', unsafe_allow_html=True)
            AD_v = experiment_number_input(t("lab11_4_AD"), "мм", key=f"lab11_4_AD_{i}", value=30.0)
            CB_v = experiment_number_input(t("lab11_4_CB"), "мм", key=f"lab11_4_CB_{i}", value=20.0)
            st.markdown("</div>", unsafe_allow_html=True)
            all_AD.append(AD_v)
            all_CB.append(CB_v)

    st.divider()
    if st.button(t("calculate"), key="lab11_4_calc", use_container_width=True, type="primary"):
        results, error_occurred = [], False
        for i, (AD, CB) in enumerate(zip(all_AD, all_CB)):
            try:
                results.append(compute_lab11_4(AD, CB))
            except ZeroDivisionError as e:
                st.error(f"{t('exp_label')} {i+1}: {e}")
                error_occurred = True
                break
        if not error_occurred:
            errors = calc_errors([r["eta"] for r in results])
            st.session_state["lab11_4_results"] = results
            st.session_state["lab11_4_errors"]  = errors

    if "lab11_4_results" in st.session_state:
        results = st.session_state["lab11_4_results"]
        errors  = st.session_state["lab11_4_errors"]

        st.markdown(t("result_header"))
        metrics_row(results, errors, "eta", "")

        txt_result = format_result_block(results, errors, format_lab11_4_result, "η", "")
        st.markdown(f'<div class="result-box">{txt_result}</div>', unsafe_allow_html=True)

        # ── График η по опытам ────────────────────────────────────────────────
        if len(results) >= 2:
            st.markdown(f"#### 📈 {t('lab11_4_graph_title')}")
            exp_nums = list(range(1, len(results) + 1))
            eta_vals = [r["eta"] for r in results]
            df = pd.DataFrame({t("lab11_4_graph_x"): exp_nums, t("lab11_4_graph_y"): eta_vals})
            st.line_chart(df.set_index(t("lab11_4_graph_x")), use_container_width=True)
            if errors:
                st.caption(f"η орт = {errors['mean']:.4f},  Δη = {errors['abs_err']:.4f}")

        txt_content = build_txt(t("lab11_4_title"), results, errors, format_lab11_4_result, "η", "")
        csv_content = build_csv(
            t("lab11_4_title"), results, errors,
            col_headers=["AD (мм)", "CB (мм)", "η"],
            value_keys=["AD", "CB", "eta"],
            result_key="eta", result_unit="",
        )
        export_buttons(txt_content, csv_content, "lab11_4", "lab11_4")


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
    def nav_section_header(label: str):
        st.markdown(f"""
        <div style='font-size:11px; opacity:0.55; font-weight:600;
                    letter-spacing:1px; padding: 4px 8px 4px'>
            {label}
        </div>
        """, unsafe_allow_html=True)

    # 9 класс
    nav_section_header(t("grade9_section"))
    for label, key in [
        (t("lab1_nav"), "lab1"),
        (t("lab2_nav"), "lab2"),
        (t("lab3_nav"), "lab3"),
        (t("lab4_nav"), "lab4"),
    ]:
        is_active = st.session_state.active_lab == key
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_lab = key
            st.rerun()

    st.markdown("<div style='margin:4px 0'></div>", unsafe_allow_html=True)

    # 10 класс
    nav_section_header(t("grade10_section"))
    for label, key in [
        (t("lab10_1_nav"), "lab10_1"),
        (t("lab10_2_nav"), "lab10_2"),
        (t("lab10_3_nav"), "lab10_3"),
        (t("lab10_4_nav"), "lab10_4"),
        (t("lab10_7_nav"), "lab10_7"),
    ]:
        is_active = st.session_state.active_lab == key
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_lab = key
            st.rerun()

    st.markdown("<div style='margin:4px 0'></div>", unsafe_allow_html=True)

    # 11 класс
    nav_section_header(t("grade11_section"))
    for label, key in [
        (t("lab11_1_nav"), "lab11_1"),
        (t("lab11_4_nav"), "lab11_4"),
    ]:
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
# 10 класс
elif st.session_state.active_lab == "lab10_1":
    page_lab10_1()
elif st.session_state.active_lab == "lab10_2":
    page_lab10_2()
elif st.session_state.active_lab == "lab10_3":
    page_lab10_3()
elif st.session_state.active_lab == "lab10_4":
    page_lab10_4()
elif st.session_state.active_lab == "lab10_7":
    page_lab10_7()
# 11 класс
elif st.session_state.active_lab == "lab11_1":
    page_lab11_1()
elif st.session_state.active_lab == "lab11_4":
    page_lab11_4()
