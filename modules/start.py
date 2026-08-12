from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import SUPPORTED_LANGUAGES

from modules.language import get_text


# ==================================
# LANGUAGE DISPLAY NAMES
# ==================================


LANGUAGE_NAMES = {
    "id": "🇮🇩 Bahasa Indonesia",
    "en": "🇬🇧 English",
    "pt": "🇵🇹 Português",
    "ar": "🇸🇦 العربية"
}


# ==================================
# /start COMMAND
# ==================================


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    language = context.user_data.get(
        "language",
        "en"
    )

    text = get_text(
        language,
        "start_message"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


# ==================================
# /language COMMAND
# ==================================


async def language_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    language = context.user_data.get(
        "language",
        "en"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                LANGUAGE_NAMES.get(code, code),
                callback_data=f"lang_{code}"
            )
        ]
        for code in SUPPORTED_LANGUAGES
    ]

    await update.message.reply_text(
        get_text(language, "choose_language"),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==================================
# LANGUAGE SELECTION CALLBACK
# ==================================


async def language_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    code = query.data.replace("lang_", "")

    if code not in SUPPORTED_LANGUAGES:
        return

    context.user_data["language"] = code

    await query.edit_message_text(
        get_text(code, "language_selected")
    )


# ==================================
# EXPORT HANDLERS
# ==================================


def get_handlers():

    return [
        CommandHandler("start", start_command),
        CommandHandler("language", language_command),
        CallbackQueryHandler(language_callback, pattern="^lang_")
    ]
