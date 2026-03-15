import pandas as pd
import json
from src.reports import spending_by_category


def test_spending():

    df = pd.DataFrame({
        "Дата операции": ["01.06.2020", "15.06.2020"],
        "Дата платежа": ["01.06.2020", "15.06.2020"],
        "Категория": ["Супермаркеты", "Супермаркеты"],
        "Сумма платежа": [100, 200],
    })

    result = spending_by_category(df, "Супермаркеты", "02.07.2020")

    assert "Супермаркеты" in result
