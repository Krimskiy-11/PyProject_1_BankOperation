import json
import os
import re
import pandas as pd

HIGH_PATH = os.path.dirname(os.path.dirname(__file__))
PATH_data = os.path.join(HIGH_PATH, "data")
path_operations = os.path.join(PATH_data, "operations.xlsx")

reading_file = pd.read_excel(path_operations)


def search_words_in_description(search_word: str, file=reading_file):

    reading_file_dict = file.to_dict(orient="records")

    result = []

    for operation in reading_file_dict:

        description = str(operation.get("Описание", ""))
        category = str(operation.get("Категория", ""))

        if re.search(search_word, description, flags=re.IGNORECASE) or \
           re.search(search_word, category, flags=re.IGNORECASE):
            result.append(operation)

    return json.dumps(result, indent=4, ensure_ascii=False)


print(search_words_in_description("OZON"))
