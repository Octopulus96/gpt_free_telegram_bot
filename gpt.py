import g4f, logging
from log_config import log_config

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

async def chat_gpt(request_text: str) -> str:

    try:
        response = await g4f.ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request_text}],
            provider=g4f.Provider.Aura,
        )
        chat_gpt_response = response
    except Exception as e:
        logging.error(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    return chat_gpt_response