from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from handlers import handle_audio, handle_photo

import os

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')


app = Client(
    name = "session/myapp",
    api_id = api_id,
    api_hash = api_hash,
    bot_token=bot_token
)


app.add_handler(MessageHandler(handle_audio, filters.audio))

app.add_handler(MessageHandler(handle_photo, filters.photo))



app.start()
info = app.get_me()
 
app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

idle()

app.stop()
