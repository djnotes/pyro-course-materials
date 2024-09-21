from pyrogram import Client

import os

api_id = os.environ.get("api_id")
api_hash = os.environ.get("api_hash")
bot_token = os.environ.get("bot_token")

app = Client(
    name = "session/bot",
    api_id= api_id,
    api_hash = api_hash,
    bot_token = bot_token
)


app.start()


try:

    app.send_message(
        chat_id = "dev2000x",
        text = "Hello Pyrogram Developer! I've got a surprise sticker for you!"
    )
    app.send_sticker(
        chat_id = "dev2000x",
        sticker = "sticker.webp"
    )

except Exception as e:
    print(f"An error occurred sending message: {e}")


