from pyrogram import Client 
from pyrogram.types import Message

from util import *

sessions = {}

async def handle_updates(client: Client, message: Message):
    uid = message.from_user.id
    if uid in sessions and Keys.STATE in sessions[uid]:
        match sessions[uid][Keys.STATE]:
            case Values.ENTER_USERNAME:
                sessions[uid][Keys.USERNAME] = message.text
                await message.reply("Choose a password (at least 8 characters):")
                sessions[uid][Keys.STATE] = Values.ENTER_PASSWORD
            case Values.ENTER_PASSWORD:
                sessions[uid][Keys.PASSWORD] = message.text
                username = sessions[uid][Keys.USERNAME]
                password = sessions[uid][Keys.PASSWORD]
                await message.reply("Registration complete:\n username: {0}\npassword: {1}".format(username, password))
                sessions[uid][Keys.STATE] = None

    else:
        match message.text:
            case "/wind":
                await client.send_photo(chat_id = message.from_user.id, photo = "media/wind.jpg", reply_to_message_id=message.id)
            case "/earth":
                await message.reply_photo(photo = "media/earth.jpg", reply_to_message_id=message.id)
            case "/fire":
                await message.reply_photo(photo = "media/fire.jpg", reply_to_message_id=message.id)
            case "/water":
                await message.reply_photo(photo = "media/water.jpg", reply_to_message_id=message.id)
            
            case "/register":
                await message.reply("Choose a username: ")
                sessions[uid] = {Keys.STATE: Values.ENTER_USERNAME}

            case _:
                await message.reply(text = "Command not recognized")
