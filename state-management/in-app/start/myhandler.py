from pyrogram import Client 
from pyrogram.types import Message

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
