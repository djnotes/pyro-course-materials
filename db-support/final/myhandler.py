from pyrogram import Client 
from pyrogram.types import Message
from sqlalchemy import select

from db import Note, get_db

async def handle_updates(client: Client, message: Message):
    parts = message.text.split(maxsplit=1)
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
            session.add(Note(author_id = message.from_user.id, text = parts[1]))
            session.commit()
            await message.reply("Note added")
        case "/note":
            session = get_db()
            stmt = select(Note).where(Note.author_id == message.from_user.id)
            notesText = ""
            for note in session.scalars(stmt):
                notesText += note.text + '\n'
            await message.reply(notesText)
            
        case "/update":
            pass
        case "/delete":
            pass
        
        case _:
            await message.reply(text = "Command not recognized")
