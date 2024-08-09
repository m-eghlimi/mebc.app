import os
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Initialize bot
bot = Bot(token=TELEGRAM_TOKEN)

# Mock database for users
users = set()

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in users:
        users.add(user_id)
    
    if user_id == ADMIN_ID:
        update.message.reply_text("Welcome, Admin!")
    else:
        update.message.reply_text("Welcome to the bot!")

def admin(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text("Admin panel:", 
                                  reply_markup=ReplyKeyboardMarkup([['Admin Box', 'User List', 'Broadcast']], resize_keyboard=True))
    else:
        update.message.reply_text("You are not authorized to access this command.")

def admin_box(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text("This is your admin box!")
    else:
        update.message.reply_text("You are not authorized to access this command.")

def user_list(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        user_list_text = "\n".join([str(user) for user in users])
        update.message.reply_text(f"Registered users:\n{user_list_text}")
    else:
        update.message.reply_text("You are not authorized to access this command.")

def broadcast(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        message = " ".join(context.args)
        for user in users:
            bot.send_message(chat_id=user, text=f"Broadcast message:\n{message}")
        update.message.reply_text("Broadcast message sent.")
    else:
        update.message.reply_text("You are not authorized to access this command.")

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main() -> None:
    # Set up the Updater
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Admin Box$'), admin_box))
    dispatcher.add_handler(MessageHandler(Filters.regex('^User List$'), user_list))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast))

    # on non-command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()