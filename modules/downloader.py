import os
import re

from pathlib import Path

from telegram import File
from telegram.ext import ContextTypes



# ==================================
# TEMP DIRECTORY
# ==================================


TEMP_DIR = "temp"


os.makedirs(
    TEMP_DIR,
    exist_ok=True
)





# ==================================
# CLEAN FILE NAME
# ==================================


def safe_filename(
    filename: str
):


    if not filename:

        filename = "unknown_file"



    filename = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        filename
    )


    return filename







# ==================================
# DOWNLOAD TELEGRAM FILE
# ==================================


async def download_file(
    context: ContextTypes.DEFAULT_TYPE,
    file_id: str,
    file_name: str = None
):


    try:

        telegram_file: File = await context.bot.get_file(
            file_id
        )



        filename = safe_filename(
            file_name
        )



        file_path = os.path.join(
            TEMP_DIR,
            filename
        )



        await telegram_file.download_to_drive(
            custom_path=file_path
        )



        return {

            "success": True,

            "path": file_path,

            "filename": filename

        }



    except Exception as e:


        return {

            "success": False,

            "error": str(e)

        }







# ==================================
# DOWNLOAD FROM MESSAGE OBJECT
# ==================================


async def download_document(
    message,
    context: ContextTypes.DEFAULT_TYPE
):


    if not message.document:


        return {

            "success": False,

            "error": "No document found"

        }



    return await download_file(

        context,

        message.document.file_id,

        message.document.file_name

    )