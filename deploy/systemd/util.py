from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

class Buttons:
    home = "Home 🏠"
    settings = "Settings ⚙️"
    admins = "Admins 👥"
    channels = "Channels 📺📺"
    translations = "Languages 📙"
    files = "Files 📁"
    stats = "Stats 📊"  
    info = "Info ℹ️"
    language = "Language 📚"
    add_admin = "Add Admin"
    view_admins = "View Admins"
    remove_admin = "Remove Admin"
    remove_keyboard = "Remove Keyboard"
    make_inline_links = "Make Inline Links"

    #Media Buttons
    send_photo = "Send Photo 📷"
    send_sticker = "Send Sticker 🙂"
    send_video = "Send Video 📹"
    send_audio = "Send Audio 🎧"
    send_voice = "Send Voice 🎤"
    send_document = "Send Document 📓"
    send_animation = "Send Animation 🏃"
    media = "Media ⌨️"
    

class Keys:
    MEDIA_MESSAGE = "_media_message_"    
    
class Values:
    CONFIRM_KB_REMOVAL = "_confirm_kb_removal_"
    CANCEL_KB_REMOVAL = "_cancel_kb_removal_"
    CONFIRM_DOWNLOAD = "_confirm_download_"
    
class Keyboards:
    MainMenu = ReplyKeyboardMarkup(
        [
            [KeyboardButton(Buttons.settings)],
            [KeyboardButton(Buttons.admins), KeyboardButton(Buttons.channels)],
            [KeyboardButton(Buttons.make_inline_links),KeyboardButton(Buttons.remove_keyboard)],
            [KeyboardButton(Buttons.media)] # Media Keyboard
        ]
    )

    SettingsMenu = ReplyKeyboardMarkup(
        [
            [Buttons.language],
            [KeyboardButton(Buttons.home)]
        ]
    )

    AdminsMenu = ReplyKeyboardMarkup (
        [
            [Buttons.add_admin, Buttons.remove_admin],
            [Buttons.view_admins],
            [KeyboardButton(Buttons.home)]
        ]
    )

    MediaMenu = ReplyKeyboardMarkup(
        [
            [Buttons.send_photo, Buttons.send_sticker],
            [Buttons.send_audio, Buttons.send_voice],
            [Buttons.send_video, Buttons.send_animation],
            [Buttons.send_document],
        ]
    )


ABSPATH = None  # better default


def get_abs_path() -> str:
    """Gets the absolute path to the project"""
    global ABSPATH
    if ABSPATH:
        return ABSPATH
    else:
        ABSPATH = os.path.dirname(os.path.abspath(__file__))
        return ABSPATH
