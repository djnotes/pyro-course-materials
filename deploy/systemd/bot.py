from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler 
from myhandler import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler

from myhandler import handle_callback_query

from config import AppConfig

# load configuration and credentials via AppConfig
cfg = AppConfig()

# api_id is expected to be an integer for pyrogram Client; convert when present
api_id = int(cfg.api_id) if cfg.api_id else None
api_hash = cfg.api_hash
bot_token = cfg.bot_token

proxy = {
    "scheme": cfg.proxy_scheme,
    "hostname": cfg.proxy_host ,
    "port": int(cfg.proxy_port)
} if cfg.proxy_on else None

app = Client(
    name = "session/myapp",
    api_id = api_id,
    api_hash = api_hash,
    bot_token=bot_token,
    proxy=proxy
)


# @app.on_message()
app.add_handler(MessageHandler(handle_updates))
app.add_handler(CallbackQueryHandler(handle_callback_query))

app.start()
 
info = app.get_me()

app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

idle()

app.stop()
