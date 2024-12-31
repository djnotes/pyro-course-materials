from pyrogram import Client 
from pyrogram.types import Message

from db import Db
from util import *
from cache import Cache

# sessions = {}
# cache = Cache()

db = Db()

async def handle_updates(client: Client, message: Message):
    uid = message.from_user.id
    state = db.get_session_item(uid, Keys.STATE)
    print('State is: {0}'.format(state))
    # state = cache.get_session_item(uid, Keys.STATE)
    
    # if uid in sessions and Keys.STATE in sessions[uid]:
    if state:
        # match sessions[uid][Keys.STATE]:
        match state:
            case Values.ENTER_USERNAME:
                # sessions[uid][Keys.USERNAME] = message.text
                # cache.update_user_session(uid, Keys.USERNAME, message.text)
                # cache.update_user_session(uid, Keys.STATE, Values.ENTER_PASSWORD)
                db.update_user_session(uid, Keys.USERNAME, message.text)
                db.update_user_session(uid, Keys.STATE, Values.ENTER_PASSWORD)
                await message.reply("Choose a password (at least 8 characters):")
                # sessions[uid][Keys.STATE] = Values.ENTER_PASSWORD
            case Values.ENTER_PASSWORD:
                # sessions[uid][Keys.PASSWORD] = message.text
                password = message.text
                
                # username = cache.get_session_item(uid, Keys.USERNAME)
                username = db.get_session_item(uid, Keys.USERNAME)

                # username = sessions[uid][Keys.USERNAME]
                # password = sessions[uid][Keys.PASSWORD]
                await message.reply("Registration complete:\n username: {0}\npassword: {1}".format(username, password))
                # sessions[uid][Keys.STATE] = None
                # cache.clear_session(uid)
                db.clear_session(uid)

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
                # cache.update_user_session(uid, Keys.STATE, Values.ENTER_USERNAME)
                db.update_user_session(uid, Keys.STATE, Values.ENTER_USERNAME)
                
                # sessions[uid] = {Keys.STATE: Values.ENTER_USERNAME}

            case _:
                await message.reply(text = "Command not recognized")
