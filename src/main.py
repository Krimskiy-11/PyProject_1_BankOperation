import json
import os

from src.utils import hello
from src.views import filter_operations_by_date, get_cards_info, top_five_operations, currency_price, stocks_price

HIGH_PATH = os.path.dirname(os.path.dirname(__file__))
PATH_json = os.path.join(HIGH_PATH, "user_settings.json")

if __name__ == "__main__":
    date = "2021-12-12 12:12:12"
    greeting = hello()
    filter_df = filter_operations_by_date(date)
    cards_info = get_cards_info(filter_df)
    top = top_five_operations(filter_df)
    currency = currency_price(PATH_json)
    stocks = stocks_price(PATH_json)
    result = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top,
        "currency_rates": currency,
        "stock_prices": stocks,
        }

    print(json.dumps(result, ensure_ascii=False, indent=4))