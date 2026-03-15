import json

from src.views import (
    filter_operations_by_date,
    get_cards_info,
    top_five_operations,
    currency_price,
    stocks_price,
)

import pandas as pd
from unittest.mock import patch, mock_open


@patch("src.views.read_excel")
def test_filter_operations_by_date(mock_read_excel):
    fake_df = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2024-01-05 00:00:00",
                    "2024-01-15 00:00:00",
                    "2024-02-01 00:00:00",
                ]
            )
        }
    )

    mock_read_excel.return_value = fake_df

    result = filter_operations_by_date("2024-01-20 00:00:00")

    assert len(result) == 2


def test_get_cards_info():
    fake_df = pd.DataFrame(
        {
            "Номер карты": ["1111", "1111", "2222"],
            "Сумма платежа": [100, 200, 300],
            "Кэшбэк": [10, 20, 30],
        }
    )

    result = get_cards_info(fake_df)

    expected = [
        {"Номер карты": "1111", "Сумма платежа": 300, "Кэшбэк": 30},
        {"Номер карты": "2222", "Сумма платежа": 300, "Кэшбэк": 30},
    ]

    result_sorted = sorted(result, key=lambda x: x["Номер карты"])
    expected_sorted = sorted(expected, key=lambda x: x["Номер карты"])

    assert result_sorted == expected_sorted


def test_top_five_operations():
    fake_df = pd.DataFrame(
        {
            "Дата платежа": [
                "2024-01-01",
                "2024-01-02",
                "2024-01-03",
                "2024-01-04",
                "2024-01-05",
                "2024-01-06",
            ],
            "Сумма платежа": [500, 200, 800, 100, 400, 600],
            "Категория": ["A", "B", "C", "D", "E", "F"],
            "Описание": ["t1", "t2", "t3", "t4", "t5", "t6"],
        }
    )

    result = top_five_operations(fake_df)

    sums = [x["Сумма платежа"] for x in result]
    assert sums == sorted(sums)[:5]

    expected_sums = [100, 200, 400, 500, 600]
    assert sums == expected_sums


@patch("src.views.requests.get")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps({"user_currencies": ["EUR", "GBP"]}),
)
def test_currency_price(mock_file, mock_get):
    mock_get.return_value.__getitem__.return_value.__getitem__.return_value.json.return_value = (
        150
    )

    result = currency_price("dummy_path.json")

    assert result[0]["stock"] == {"EUR"}
    assert result[1]["stock"] == {"GBP"}


@patch("src.views.requests.get")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps({"user_stocks": ["AAPL", "TSLA"]}),
)
def test_stocks_price(mock_file, mock_get):
    mock_get.return_value.__getitem__.return_value.json.return_value = 1000

    result = stocks_price("dummy_path.json")

    assert result[0]["stock"] == {"AAPL"}
    assert result[1]["stock"] == {"TSLA"}
