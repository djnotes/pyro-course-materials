from pyrogram import Client
from pyrogram.types import Message

from util import EMOJI


async def handle_user_updates(client: Client, message: Message):
    caption = message.caption
    uid = message.from_user.id
    text = message.text
    
    if message.media and caption and caption == "Set Profile":
        media = await client.download_media(message)
        success = await client.set_profile_photo(photo = media)
        if success:
            await message.reply("Profile photo set successfully")
        
    if text and text == "Hello" or text == "hello":
        await client.send_reaction(chat_id = uid, message_id=message.id, emoji = EMOJI.heart)
    else:
        await client.send_reaction(chat_id = uid, message_id = message.id, emoji = EMOJI.fire)

        
        
        