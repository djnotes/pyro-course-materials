from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

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


async def handle_updates(client: Client, message: Message):
    match message.text:
        case "/wind":
            await client.send_photo(chat_id = message.from_user.id, photo = "media/wind.jpg", reply_to_message_id=message.id)
        case "/earth":
            await message.reply_photo(photo = "media/earth.jpg", reply_to_message_id=message.id)
        case "/fire":
            await message.reply_photo(photo = "media/fire.jpg", reply_to_message_id=message.id)
        case "/water":
            await message.reply_photo(photo = "media/water.jpg", reply_to_message_id=message.id)
        
        case _:
            await message.reply(text = "Command not recognized")


app.start()

app.send_message(chat_id = "dev2000xx", text = f"{app.name} started")

app.add_handler(MessageHandler(handle_updates))

idle()
app.stop()
