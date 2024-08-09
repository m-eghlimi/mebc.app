from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

app = Flask(__name__)

# وارد کردن توکن ربات تلگرام خود
TOKEN = "6899423972:AAFHpBMeUtI5PpKjkZLI1i4xTsKcOAA62LU"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def start(update, context):
    update.message.reply_text("Welcome! How can I help you today?")

def echo(update, context):
    update.message.reply_text(update.message.text)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)