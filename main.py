import logging


from telegram import Update

from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters
)


from config import BOT_TOKEN, MAX_FILE_SIZE

from modules.language import get_text

from modules.start import get_handlers

from modules.detector import detect_message

from modules.downloader import download_document

from modules.virustotal import scan_file

from modules.url_scanner import scan_url

from modules.formatter import format_scan, format_url_scan

from modules.cleaner import clean_temp





# ==================================
# LOGGING
# ==================================


logging.basicConfig(

    format="%(asctime)s | %(levelname)s | %(message)s",

    level=logging.INFO

)


logger = logging.getLogger(
    "SecurityBot"
)







# ==================================
# FILE SCANNER
# ==================================


async def scanner(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    message = update.message



    if not message:

        return





    detected = detect_message(
        message
    )



    if not detected:

        return





    # ==============================
    # FILE
    # ==============================


    if detected["type"] == "file":



        language = context.user_data.get(

            "language",

            "en"

        )



        if detected["size"] and detected["size"] > MAX_FILE_SIZE:



            await message.reply_text(

                get_text(

                    language,

                    "file_too_large"

                ).replace(

                    "{max_size}",

                    str(MAX_FILE_SIZE // (1024 * 1024))

                )

            )

            return



        status = await message.reply_text(

            "⌛ File detected, performing security scan..."

        )




        download = await download_document(

            message,

            context

        )



        if not download["success"]:


            await status.edit_text(

                "❌ Failed to download file."

            )

            return




        file_path = download["path"]





        result = await scan_file(

            file_path

        )





        clean_temp(

            file_path

        )






        if not result.get(
            "success"
        ):


            await status.edit_text(

                "❌ Security scan failed."

            )

            return





        language = context.user_data.get(

            "language",

            "en"

        )





        text, report = format_scan(

            result,

            language

        )





        await status.edit_text(

            text,

            parse_mode="HTML"

        )








    # ==============================
    # URL
    # ==============================


    elif detected["type"] == "url":


        status = await message.reply_text(

            "⌛ Link detected, performing security scan..."

        )


        result = await scan_url(

            detected["url"]

        )


        if not result.get("success"):

            await status.edit_text(

                "❌ URL scan failed."

            )

            return


        language = context.user_data.get(

            "language",

            "en"

        )


        text, report = format_url_scan(

            result,

            language

        )


        await status.edit_text(

            text,

            parse_mode="HTML"

        )









# ==================================
# MAIN
# ==================================


def main():


    if not BOT_TOKEN:

        raise ValueError(

            "BOT_TOKEN is missing in .env"

        )





    app = (

        Application

        .builder()

        .token(

            BOT_TOKEN

        )

        .build()

    )






    # START HANDLER

    for handler in get_handlers():


        app.add_handler(

            handler

        )







    # AUTO SCANNER


    app.add_handler(

        MessageHandler(

            filters.ALL,

            scanner

        )

    )






    logger.info(

        "Bot started"

    )




    app.run_polling()







if __name__ == "__main__":

    main()