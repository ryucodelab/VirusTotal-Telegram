import re
from urllib.parse import urlparse





# ==================================
# URL REGEX
# ==================================


URL_PATTERN = re.compile(
    r"https?://[^\s]+",
    re.IGNORECASE
)





# ==================================
# DETECT MESSAGE
# ==================================


def detect_message(
    message
):
    """
    Detect message content.

    Return:
    {
        type: file/url,
        data: object
    }

    or None
    """



    # ==========================
    # DOCUMENT / FILE
    # ==========================


    if message.document:


        return {

            "type": "file",

            "file_id":
            message.document.file_id,


            "file_name":
            message.document.file_name,


            "mime_type":
            message.document.mime_type,


            "size":
            message.document.file_size

        }







    # ==========================
    # URL CHECK
    # ==========================


    text = (
        message.text
        or
        message.caption
        or
        ""
    )


    urls = URL_PATTERN.findall(
        text
    )


    if urls:


        return {

            "type": "url",

            "url":
            clean_url(
                urls[0]
            )

        }






    # ==========================
    # IGNORE TEXT
    # ==========================


    return None







# ==================================
# CLEAN URL
# ==================================


def clean_url(
    url
):


    url = url.rstrip(
        ".,!?)]}"
    )


    return url







# ==================================
# CHECK URL VALID
# ==================================


def is_valid_url(
    url
):


    try:

        result = urlparse(
            url
        )


        return all([

            result.scheme in (
                "http",
                "https"
            ),

            result.netloc

        ])


    except Exception:


        return False