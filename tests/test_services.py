import pandas as pd
import json
import pytest
from src.services import search_words_in_description


@pytest.mark.parametrize(
    "search_word, expected_count",
    [
        ("OZON", 2),
        ("магазин", 1),
        ("супермаркеты", 1),
        ("amazon", 0),
    ],
)
def test_search_words(search_word, expected_count):

    df = pd.DataFrame({
        "Описание": [
            "Покупка OZON",
            "Оплата в магазине",
            "OZON доставка"
        ],
        "Категория": [
            "Маркетплейсы",
            "Супермаркеты",
            "Онлайн покупки"
        ],
        "Сумма платежа": [1000, 500, 2000]
    })

    result = search_words_in_description(search_word, df)
    result_dict = json.loads(result)

    assert len(result_dict) == expected_count