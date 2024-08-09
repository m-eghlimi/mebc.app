from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler

app = Flask(__name__)

TOKEN = "6899423972:AAFHpBMeUtI5PpKjkZLI1i4xTsKcOAA62LU"
bot = Bot(token=TOKEN)

application = Application.builder().token(TOKEN).build()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return 'ok'

def start(update: Update, context):
    update.message.reply_text("Welcome! How can I help you today?")

application.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)