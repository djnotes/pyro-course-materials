from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram import filters

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


@app.on_message(filters.audio)
async def handle_audio(client, message):
    await message.reply("You sent me an audio file")

@app.on_message(filters.photo)
async def handle_photo(client, message):
    await message.reply("You sent me a photo")


app.start()
info = app.get_me()
 
app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

idle()

app.stop()
