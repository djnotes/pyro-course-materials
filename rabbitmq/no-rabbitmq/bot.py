from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler 
from config import AppConfig
from myhandler import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler

from myhandler import handle_callback_query

from cache import Cache


import debugpy

from utils import get_my_logger

logger = get_my_logger()



debugpy.listen(('bot', 5679))


cache = Cache()


appConfig = AppConfig()




api_id = appConfig.api_id
api_hash = appConfig.api_hash
bot_token = appConfig.bot_token
proxy_on = appConfig.proxy_on
proxy_scheme = appConfig.proxy_scheme
proxy_host = appConfig.proxy_host
proxy_port = appConfig.proxy_port

if proxy_on:
    proxy_info = {
        "scheme": appConfig.proxy_scheme,
        "hostname": appConfig.proxy_host,
        "port": int(appConfig.proxy_port)
    }
    

app = Client(
    name = "session/myapp",
    api_id = appConfig.api_id,
    api_hash = appConfig.api_hash,
    bot_token=appConfig.bot_token,
    proxy = proxy_info if proxy_on else None
)

app.start()
 
info = app.get_me()

app.send_message(chat_id = int(appConfig.bot_admin), text = f"{__name__}:{app.name}:{info.first_name} launched inside the main bot file")

# clear cache on startup
cache.clear_all_sessions()
logger.info("Bot started and session was cleared")

app.add_handler(MessageHandler(handle_updates))
app.add_handler(CallbackQueryHandler(handle_callback_query))

idle()

app.stop()
