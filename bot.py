from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات مربوط به لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# دستور /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! خوش آمدید.')

# دستور /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('چطور می‌تونم کمکتون کنم؟')

# مدیریت پیام‌ها
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main():
    # دریافت توکن ربات از متغیر محیطی
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Please set it in the .env file.")
        return

    # دریافت پورت از متغیر محیطی
    port = int(os.environ.get('PORT', 8443))

    # ساخت یک آپدیتور با توکن ربات و تنظیمات وب‌هوک
    updater = Updater(token, use_context=True)

    # تنظیم وب‌هوک
    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=token)
    updater.bot.setWebhook(f'https://9f813d90875c104f7616f67dac787130.serveo.net/{token}')

    dispatcher = updater.dispatcher

    # اضافه کردن هندلرها
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # شروع سرویس‌دهی
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()