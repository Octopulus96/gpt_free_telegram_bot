import logging, os
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from gpt import chat_gpt
from log_config import log_config

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

token = os.environ["TG_TOKEN"]
user_list_str = os.environ["USER_LIST"]
user_list_int = list(map(int, user_list_str.split(',')))

async def access_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_user.id in user_list_int:
        await update.message.reply_text("Добро пожаловать! Вы имеете доступ к боту.")
        return True
    else:
        await update.message.reply_text("К сожалению, у вас нет доступа к боту.")
        logger.info(f"Неудачная попытка подключения {update.effective_chat.id}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if await access_check(update, context):
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await access_check(update, context):
        await update.message.reply_text(await chat_gpt(update.message.text))

def main() -> None:
    logger.info("Telegram Bot is Started")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()