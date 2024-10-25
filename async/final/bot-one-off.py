from pyrogram import Client, idle
from pyrogram.types import Message
import asyncio

import os

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')





async def myapp():
    app = Client(
        name = "session/myapp",
        api_id = api_id,
        api_hash = api_hash,
        bot_token=bot_token
    )
    await app.start()
    info = await app.get_me()
    await app.send_message("dev2000xx", f"{info.first_name} started in async mode!!!")
    

asyncio.run(myapp())

