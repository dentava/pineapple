#!/usr/bin/env python
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PHOTO, NAME = range(2)

temporary = ""

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Ciao, mandami il nome dell\'utente da aggiungere')
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    global temporary
    temporary = update.message.text
    update.message.reply_text('Ora mandami una sua foto chiara e visibile')

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    photo_file = update.message.photo[-1].get_file()
    name = "pineapple/img/" + temporary + ".jpg"
    photo_file.download(name)
    update.message.reply_text('Utente aggiunto con successo!')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            PHOTO: [MessageHandler(Filters.photo, photo)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
