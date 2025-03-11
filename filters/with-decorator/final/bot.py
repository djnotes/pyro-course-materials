from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from handlers import handle_audio, handle_visual, handle_audio_in_group, handle_start, handle_stats_cmd

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


app.add_handler(MessageHandler(handle_audio, filters.audio & filters.caption))

app.add_handler(MessageHandler(handle_visual, filters.photo | filters.video | filters.animation))

app.add_handler(MessageHandler(handle_audio_in_group, filters.audio & ~filters.private))

app.add_handler(MessageHandler(handle_start, filters.command("start")))


app.add_handler(MessageHandler(handle_stats_cmd, filters.command("stats")))

#+18001231234
@app.on_message(filters.regex(r"\+?\d{11}"))
async def handle_phone_number(client, message):
    await message.reply("You sent me a phone number")



app.start()
info = app.get_me()
 
app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

idle()

app.stop()
