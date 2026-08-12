import json
import os


# ==================================
# LOCALES DIRECTORY
# ==================================


LOCALES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "locales"
)


_cache = {}




# ==================================
# LOAD LOCALE FILE
# ==================================


def load_locale(
    language: str
):

    if language in _cache:

        return _cache[language]


    path = os.path.join(
        LOCALES_DIR,
        f"{language}.json"
    )


    if not os.path.exists(path):

        path = os.path.join(
            LOCALES_DIR,
            "en.json"
        )


    with open(path, "r", encoding="utf-8") as file:

        data = json.load(file)


    _cache[language] = data

    return data




# ==================================
# GET TEXT BY KEY
# ==================================


def get_text(
    language: str,
    key: str
):

    data = load_locale(language)

    return data.get(key, key)
