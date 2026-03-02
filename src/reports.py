import json
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

import pandas as pd

HIGH_PATH = os.path.dirname(os.path.dirname(__file__))
PATH_data = os.path.join(HIGH_PATH, "data")
PATH_file = os.path.join(PATH_data, "operations.xlsx")
operations_df = pd.read_excel(PATH_file)


def report_decorator(filename: Optional[str] = None):
    """Декоратор для сохранения отчетов в файл."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result_dict = result.to_dict(orient="records")

            if filename:
                filename_1 = filename
            else:
                filename_1 = (
                    f'Report_{func.__name__}_{datetime.now().strftime("%d.%m.%Y")}.json'
                )

            with open(filename_1, "w") as f:
                json.dump(result_dict, f, indent=4, ensure_ascii=False)

            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца."""

    operations = transactions[
        ["Дата операции", "Дата платежа", "Категория", "Сумма платежа"]
    ]
    filter_by_category = operations[operations["Категория"] == category]
    filter_by_category["Дата операции"] = pd.to_datetime(
        operations_df["Дата операции"], dayfirst=True
    )

    if date:
        date_start = datetime.strptime(date, "%d.%m.%Y") - timedelta(days=90)
        date_end = datetime.strptime(date, "%d.%m.%Y")
    else:
        date_end = datetime.now()
        date_start = datetime.now() - timedelta(days=90)

    df_filter_operations = filter_by_category[
        (filter_by_category["Дата операции"] > date_start)
        & (filter_by_category["Дата операции"] < date_end)
    ]

    return df_filter_operations[["Дата платежа", "Категория", "Сумма платежа"]]


# print(json.dumps(spending_by_category(operations_df, "Супермаркеты", "02.07.2020").to_dict(orient='records'),
#                  indent=4,
#                  ensure_ascii=False))
