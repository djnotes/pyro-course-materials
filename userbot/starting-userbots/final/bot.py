from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler 
from myhandler import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
import debugpy

from myhandler import handle_callback_query


import os

# debugpy.listen(("bot", 5678))

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')


app = Client(
    name = "session/myapp",
    api_id = api_id,
    api_hash = api_hash,
    bot_token=bot_token
)

userbot = Client(
    name = "session/userbot1",
    api_id = api_id,
    api_hash = api_hash
)

clients = [
    userbot
]



app.start()
info = app.get_me()
app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

app.add_handler(MessageHandler(handle_updates))
app.add_handler(CallbackQueryHandler(handle_callback_query))  

for client in clients:
    print("Starting {0}".format(client.name))
    client.start()
    info = client.get_me()
    app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")
              
    

# @app.on_message()



# userbot.start()

# u_info = userbot.get_me()
 


# app.send_message(chat_id = "dev2000xx", text = f"{u_info.first_name} started")

idle()


app.stop()
