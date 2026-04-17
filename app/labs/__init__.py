# app/labs/__init__.py — Реестр лабораторных работ
#
# Чтобы добавить новую работу:
#   1. Создай файл  app/labs/labN.py  с классом LabNFrame(LabFrame)
#   2. Импортируй его ниже
#   3. Добавь строку в список LABS

from app.labs.lab1 import Lab1Frame
from app.labs.lab2 import Lab2Frame
from app.labs.lab3 import Lab3Frame

# (label в сайдбаре,  класс виджета)
LABS: list = [
    ("№1  Теңүдемелі қозғалыс", Lab1Frame),
    ("№2  Горизонталь лақтыру",  Lab2Frame),
    ("№3  Математикалық маятник", Lab3Frame),
]
