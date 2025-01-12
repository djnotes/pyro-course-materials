from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

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
    send_video = "Send Video 📹"
    send_audio = "Send Audio 🎧"
    send_voice = "Send Voice 🎤"
    send_document = "Send Document "
    send_poll = "Send Poll 🗳️"
    send_contact = "Send Contact 👤"
    send_animation = "Send Animation 🏃"
    # Slicon Valley 37.3875° N, 122.0575° W
    
    
class Values:
    CONFIRM_KB_REMOVAL = "_confirm_kb_removal_"
    CANCEL_KB_REMOVAL = "_cancel_kb_removal_"
    
class Keyboards:
    MainMenu = ReplyKeyboardMarkup(
        [
            [KeyboardButton(Buttons.settings)],
            [KeyboardButton(Buttons.admins), KeyboardButton(Buttons.channels)],
            [KeyboardButton(Buttons.make_inline_links),KeyboardButton(Buttons.remove_keyboard)]
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
    
    


    