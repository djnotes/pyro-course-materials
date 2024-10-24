from pyrogram import Client, idle
from pyrogram.types import Message
import asyncio
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

async def main():
    # await app.start()
    user = await app.get_me()
    try:
        await app.send_message('salemgrrr', f'{user.first_name} started')
    except Exception as e:
        print(f'Error occurred: {e}')

    app.add_handler(MessageHandler(handle_updates))
    # idle()
    # await app.stop()
    
    
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

loop.run_forever()



# asyncio.run(main())

