import logging, os, telegram
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from utils.gpt import chat_gpt
from utils.log_config import log_config

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

token = os.environ["TG_TOKEN"]
user_list_str = os.environ["USER_LIST"]
user_list_int = list(map(int, user_list_str.split(',')))

async def access_check(update: Update, context: ContextTypes.DEFAULT_TYPE, user_list: list) -> bool:
    if update.effective_user.id in user_list:
        return True
    else:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await access_check(update, context, user_list_int):
        await update.message.reply_text("Hello")
    else:
        await update.message.reply_text("No Access")

async def gpt_request_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("GPT request received")
    if await access_check(update, context, user_list_int):
        response = await chat_gpt(update.message.text)
        logger.info(f"Sending GPT response to user ID: {update.effective_user.id}")
        await update.message.reply_text(response)
    else:
        logger.info("No access to GPT request")
        await update.message.reply_text("No Access")

def main() -> None:
    logger.info("Telegram Bot is Started")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_request_response))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Telegram Bot has been started successfully")
    
if __name__ == "__main__":
    main()