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
    
    


    