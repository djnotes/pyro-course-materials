from pyrogram import Client 
from pyrogram.types import Message, ReplyKeyboardRemove
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from util import Buttons
from util import Keyboards
from util import Values

from pyrogram.types import CallbackQuery


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
            confirm_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text = "Yes", callback_data=Values.CONFIRM_KB_REMOVAL), InlineKeyboardButton(text = "No", callback_data=Values.CANCEL_KB_REMOVAL)]
            ]
            )
            await message.reply("Are you sure you want to remove the keyboard?", reply_markup=confirm_inline_kb)
        case Buttons.make_inline_links:
            inline_kb = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text = "My Telegram Channel", url = "https://t.me/codewithmehdi")],
                    [InlineKeyboardButton(text = "My YouTube Channel", url = "https://youtube.com/mehdihaghgoo")],
                    [InlineKeyboardButton(text = "My GitHub Profile", url = "https://github.com/djnotes")]
                ]
            )
            await message.reply(text = "My Links", reply_markup=inline_kb)
        
        # Handle Media
        case Buttons.media:
            await message.reply(text = "Media Menu", reply_markup= Keyboards.Media)
        case Buttons.send_photo:
            pass
        case Buttons.send_sticker:
            pass
        case Buttons.send_video:
            pass
        case Buttons.send_audio:
            pass
        case Buttons.send_voice:
            pass
        case Buttons.send_document:
            pass
        case Buttons.send_animation:
            pass
        case _:
            await message.reply("Unexpected input")


async def handle_callback_query(client: Client, query: CallbackQuery):
    match query.data:
        case Values.CONFIRM_KB_REMOVAL:
            await client.send_message(chat_id = query.from_user.id, text = "You removed the keyboard", reply_markup=ReplyKeyboardRemove())
        case Values.CANCEL_KB_REMOVAL:
            await client.send_message(chat_id = query.from_user.id, text = "You selected No")