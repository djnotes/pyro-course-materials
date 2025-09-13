from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler 
from config import AppConfig
from myhandler import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler

from myhandler import handle_callback_query
from db import Db as Cache

import os

appConfig = AppConfig()

cache = Cache()

# api_id = os.environ.get('api_id')
# api_hash = os.environ.get('api_hash')
# bot_token = os.environ.get('bot_token')
# proxy_on = os.environ.get('PROXY_ON')

api_id = appConfig.api_id
api_hash = appConfig.api_hash
bot_token = appConfig.bot_token
proxy_on = appConfig.proxy_on
proxy_scheme = appConfig.proxy_scheme
proxy_host = appConfig.proxy_host
proxy_port = appConfig.proxy_port

if proxy_on:
#     proxy_scheme=os.environ.get('PROXY_SCHEME')
#     proxy_host=os.environ.get('PROXY_HOST')
#     proxy_port=int(os.environ.get('PROXY_PORT'))
    proxy_info = {
        "scheme": appConfig.proxy_scheme,
        "hostname": appConfig.proxy_host,
        "port": int(appConfig.proxy_port)
    }
    

app = Client(
    name = "session/bot1",
    api_id = appConfig.api_id,
    api_hash = appConfig.api_hash,
    bot_token=appConfig.bot_token,
    proxy = proxy_info if proxy_on else None
)


# @app.on_message()
app.add_handler(MessageHandler(handle_updates))
app.add_handler(CallbackQueryHandler(handle_callback_query))

import time
app.start()
 
info = app.get_me()

app.send_message(chat_id = appConfig.bot_admin, text = f"{app.name}:{info.first_name} started")

idle()

app.stop()
