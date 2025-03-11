async def handle_audio(client, message):
    await message.reply("You sent me an audio file")

async def handle_photo(client, message):
    await message.reply("You sent me a photo")