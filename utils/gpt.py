import g4f, logging
from utils.log_config import log_config

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking
logger.info(g4f.Provider.Bing.params)  # Print supported args for Bing

async def chat_gpt(request_text: str) -> str:
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": request_text}],
    )
    logger.info(response)
    return response
