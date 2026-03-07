from src.utils import hello, read_excel

import pandas as pd
from unittest.mock import patch, mock_open
from datetime import datetime


@patch("src.views.datetime")
def test_hello_morning(mock_date):
    fake_datetime = datetime(2024, 1, 1, 8, 0, 0)
    mock_date.now.return_value = fake_datetime
    result = hello()

    assert result == "Добрый вечер"


def test_read_excel():
    result = read_excel("operations.xlsx")
    assert isinstance(result["Дата операции"].iloc[0], pd.Timestamp)