from pyrogram import Client 
from pyrogram.types import Message, ReplyKeyboardRemove
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
        case Buttons.make_inline_links:
            inline_kb = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text = "My Telegram Channel", url = "https://t.me/codewithmehdi")],
                    [InlineKeyboardButton(text = "My YouTube Channel", url = "https://youtube.com/mehdihaghgoo")],
                    [InlineKeyboardButton(text = "My GitHub Profile", url = "https://github.com/djnotes")]
                ]
            )
            await message.reply(text = "My Links", reply_markup=inline_kb)
        
        case _:
            await message.reply("Unexpected input")
