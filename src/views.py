import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from src.utils import read_excel

load_dotenv()
API_KEY = os.getenv("API_KEY")

HIGH_PATH = os.path.dirname(os.path.dirname(__file__))
PATH_data = os.path.join(HIGH_PATH, "data")

def filter_operations_by_date(date: str):
    """Функция, фильтрующая таблицу по дате"""

    df_operations = read_excel("operations.xlsx")

    date_start = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime(
        "%Y-%m-01 00:00:00"
    )

    df_filter_operations = df_operations[
        (df_operations["Дата операции"] > date_start)
        & (df_operations["Дата операции"] < date)
    ]
    return df_filter_operations


def get_cards_info(operations_df):
    """Функция, возвращающая список с операциями по картам"""

    cards_df = (
        operations_df[["Номер карты", "Сумма платежа", "Кэшбэк"]]
        .groupby("Номер карты")
        .sum()
        .reset_index()
    )
    return cards_df.to_dict(orient="records")


def top_five_operations(operations_df):
    """Функция, возвращающая Топ-5 транзакций по сумме платежа"""

    transactions = operations_df[
        ["Дата платежа", "Сумма платежа", "Категория", "Описание"]
    ].to_dict(orient="records")
    filter_transactions = sorted(transactions, key=lambda x: x["Сумма платежа"])
    top_five = filter_transactions[0:5]
    return top_five


def currency_price(path):
    """Функция, возвращающая курс валют"""
    with open(path, "r") as f:
        reading = f.read()
        ex = json.loads(reading)
    result = []
    for k, v in ex.items():
        if k == "user_currencies":
            for currency in v:
                url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={currency}&to_symbol=USD&apikey={API_KEY}"
                r = requests.get(url)
                data = r["Meta Data"]["2. high"].json()
                ex = {"stock": {currency}, "price": {data}}
                result.append(ex)
    return result


def stocks_price(path):
    """Функция, возвращающая стоимость акций из S&P500."""
    with open(path, "r") as f:
        reading = f.read()
        ex = json.loads(reading)
    result = []
    for k, v in ex.items():
        if k == "user_stocks":
            for stock in v:
                url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={stock}&market=RUB&apikey={API_KEY}"
                r = requests.get(url)
                data = r["Meta Data"]["2. high"].json()
                ex = {"stock": {stock}, "price": {data}}
                result.append(ex)
    return result
