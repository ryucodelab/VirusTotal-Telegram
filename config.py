import os

from dotenv import load_dotenv


# ==================================
# LOAD ENV
# ==================================

load_dotenv()





# ==================================
# BOT CONFIG
# ==================================


BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
)





# ==================================
# VIRUSTOTAL CONFIG
# ==================================


VIRUSTOTAL_API_KEY = os.getenv(
    "VIRUSTOTAL_API_KEY",
    ""
)





# ==================================
# STORAGE CONFIG
# ==================================


TEMP_DIR = os.getenv(
    "TEMP_DIR",
    "temp"
)





# ==================================
# LANGUAGE CONFIG
# ==================================


DEFAULT_LANGUAGE = os.getenv(
    "DEFAULT_LANGUAGE",
    "en"
)


SUPPORTED_LANGUAGES = [

    "id",

    "en",

    "pt",

    "ar"

]





# ==================================
# SCANNER CONFIG
# ==================================


SCAN_TIMEOUT = int(
    os.getenv(
        "SCAN_TIMEOUT",
        "180"
    )
)


MAX_FILE_SIZE = int(
    os.getenv(
        "MAX_FILE_SIZE",
        "52428800"
    )
)