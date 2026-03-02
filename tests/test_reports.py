from unittest.mock import patch, mock_open
import pandas as pd
from src.reports import report_decorator

def test_report_decorator_minimal():
    @report_decorator("test.json")
    def f():
        return pd.DataFrame({"A": [1,2]})

    with patch("builtins.open", mock_open()) as m:
        df = f()
        assert df.shape == (2,1)
