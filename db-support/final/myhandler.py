from pyrogram import Client 
from pyrogram.types import Message
from sqlalchemy import select

from db import Note, get_db
from util import select_notes

async def handle_updates(client: Client, message: Message):
    parts = message.text.split(maxsplit=2)
    cmd = parts[0]
    match cmd:
        # case "/wind":
        #     await client.send_photo(chat_id = message.from_user.id, photo = "media/wind.jpg", reply_to_message_id=message.id)
        # case "/earth":
        #     await message.reply_photo(photo = "media/earth.jpg", reply_to_message_id=message.id)
        # case "/fire":
        #     await message.reply_photo(photo = "media/fire.jpg", reply_to_message_id=message.id)
        # case "/water":
        #     await message.reply_photo(photo = "media/water.jpg", reply_to_message_id=message.id)
        case "/add":
            session = get_db()
            session.add(Note(author_id = message.from_user.id, title = parts[1], text = parts[2]))
            session.commit()
            notesText = select_notes(session, message.from_user.id)
            await message.reply(notesText)
        case "/select":
            session = get_db()
            noteText = select_notes(session, message.from_user.id)
            await message.reply(noteText)
            
        case "/update":
            pass
        case "/delete":
            pass
        case _:
            await message.reply(text = "Command not recognized")

