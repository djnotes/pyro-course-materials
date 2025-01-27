from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler 
from myhandler import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
import debugpy

from myhandler import handle_callback_query


import os

debugpy.listen(("bot", 5678))

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')


app = Client(
    name = "session/myapp",
    api_id = api_id,
    api_hash = api_hash,
    bot_token=bot_token
)


# @app.on_message()
app.add_handler(MessageHandler(handle_updates))
app.add_handler(CallbackQueryHandler(handle_callback_query))

app.start()
 
info = app.get_me()

app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

idle()

app.stop()
