from flask import Flask, request
import telegram

app = Flask(__name__)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telegram.Bot(token=TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text
    bot.sendMessage(chat_id=chat_id, text="You said: " + text)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)