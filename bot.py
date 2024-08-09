from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler

app = Flask(__name__)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
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
dispatcher.add_handler(CommandHandler("echo", echo))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)