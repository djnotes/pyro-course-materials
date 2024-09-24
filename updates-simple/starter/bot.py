from pyrogram import Client, idle

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

# app.start()

# from pyrogram import Client

# app = Client("session/bot")


@app.on_message()
def my_handler(client, message):
    match message.text:
        case "/wind": 
            message.reply_photo(photo = "media/wind.jpg", caption = "Wind", reply_to_message_id=message.id)
        case "/water":
            message.reply_photo(photo = "media/water.jpg", caption = "Water", reply_to_message_id=message.id)
        case "/fire":
            message.reply_photo(photo = "media/fire.jpg", caption = "Fire", reply_to_message_id=message.id)	     
        case "/earth":
            message.reply_photo(photo = "media/earth.jpg", caption = "Earth", reply_to_message_id=message.id)	     
        case _:
            message.reply(text = "Command not recognized", reply_to_message_id = message.id)

app.start()

app.send_message(chat_id = "dev2000x", text = "Bot started!")

idle()

app.stop()
# app.send_message(chat_id='dev2000x', text = "Bot started 😊")
# app.send_animation(chat_id='dev2000x', animation = "final.tgs", file_name="final.tgs")
# app.send_sticker(chat_id="dev2000x", sticker = "img.webp")
