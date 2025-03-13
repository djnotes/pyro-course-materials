async def handle_audio(client, message):
    await message.reply("You sent me an audio file")

async def handle_visual(client, message):
    await message.reply("You sent me visual media")

async def handle_audio_in_group(client, message):
    await message.reply("You sent me an audio in group")