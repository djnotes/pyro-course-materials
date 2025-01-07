from pyrogram import Client 
from pyrogram.types import Message, ReplyKeyboardRemove

from util import Buttons
from util import Keyboards


async def handle_updates(client: Client, message: Message):
    text = message.text
    match text:
        case "/start" | Buttons.home:
            await message.reply("Main Menu", reply_markup=Keyboards.MainMenu)
        case Buttons.settings:
            await message.reply("Setting Menu", reply_markup=Keyboards.SettingsMenu)
        case Buttons.admins:
            await message.reply("Admins Menu", reply_markup=Keyboards.AdminsMenu)
        case Buttons.remove_keyboard:
            await message.reply("You removed the keyboard", reply_markup=ReplyKeyboardRemove())
            
        
        case _:
            await message.reply("Unexpected input")
