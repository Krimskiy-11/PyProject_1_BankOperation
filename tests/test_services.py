from unittest.mock import patch
import pandas as pd
import json
from src.services import search_words_in_description


@patch("src.views.pd.read_excel")
def test_search_words_in_description(mock_read_excel):

    fake_df = pd.DataFrame(
        [
            {
                "Дата платежа": "04.10.2020",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -750.0,
                "Описание": "Покупка в магазине Магнит",
                "Категория": "Супермаркеты",
            },
            {
                "Дата платежа": "05.10.2020",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -250.0,
                "Описание": "Оплата такси",
                "Категория": "Транспорт",
            },
            {
                "Дата платежа": "07.10.2020",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -850.0,
                "Описание": "Покупка в магазине Пятерочка",
                "Категория": "Супермаркеты",
            },
        ]
    )

    mock_read_excel.return_value = fake_df

    result_json = search_words_in_description("магазин", "fake_operations.xlsx")
    result = json.loads(result_json)

    assert result[0]["Описание"] == "Покупка в магазине Магнит"
    assert result[1]["Описание"] == "Покупка в магазине Пятерочка"
