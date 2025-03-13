from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from handlers import handle_audio, handle_visual, handle_audio_in_group

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

@app.on_message(filters.command("start"))
async def handle_start_cmd(client, message):
    await message.reply("The bot started")

@app.on_message(filters.command("stats"))
async def handle_stats_cmd(client, message):
    await message.reply("The bot stats are:\nTotal Users: 110\nNew Users: 50")

@app.on_message(filters.regex(r"\+?\d{11}"))
async def handle_phone(client, message):
    await message.reply("You entered a valid phone number")


app.start()
info = app.get_me()
 
app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

idle()

app.stop()
