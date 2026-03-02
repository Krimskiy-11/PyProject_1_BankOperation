import json
import logging
import os
import re

import pandas as pd

HIGH_PATH = os.path.dirname(os.path.dirname(__file__))
PATH_data = os.path.join(HIGH_PATH, "data")


def search_words_in_description(search_word: str, file):
    path_operations = os.path.join(PATH_data, file)
    reading_file = pd.read_excel(path_operations)
    reading_file_dict = reading_file.to_dict(orient="records")

    result = []
    for operation in reading_file_dict:
        if operation["Описание"]:
            if re.search(search_word, operation["Описание"], flags=re.IGNORECASE):
                result.append(operation)

        elif operation["Категория"]:
            if re.search(search_word, operation["Категория"], flags=re.IGNORECASE):
                result.append(operation)

    return json.dumps(result, indent=4, ensure_ascii=False)


# print(search_words_in_description("OZON", "operations.xlsx"))
