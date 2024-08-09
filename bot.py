from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

app = Flask(__name__)

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

dispatcher.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)