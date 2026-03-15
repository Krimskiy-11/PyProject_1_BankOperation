import os
from datetime import datetime

import pandas as pd


HIGH_PATH = os.path.dirname(os.path.dirname(__file__))
PATH_data = os.path.join(HIGH_PATH, "data")


def hello() -> str:
    """Функция-приветствия пользователя, ориентируется на нынешнее время"""

    date_now = int(datetime.now().time().strftime("%H"))
    morning = range(6, 12)
    day = range(12, 19)
    evening = range(19, 24)
    night = range(0, 6)
    if date_now in morning:
        say_hello = "Доброе утро"
    elif date_now in day:
        say_hello = "Добрый день"
    elif date_now in evening:
        say_hello = "Добрый вечер"
    elif date_now in night:
        say_hello = "Доброй ночи"
    return say_hello


def read_excel(path):
    """Функция, читающая excel-файл с операциями"""

    PATH_file = os.path.join(PATH_data, path)
    operations_df = pd.read_excel(PATH_file)
    operations_df["Дата операции"] = pd.to_datetime(
        operations_df["Дата операции"], dayfirst=True
    )
    return operations_df