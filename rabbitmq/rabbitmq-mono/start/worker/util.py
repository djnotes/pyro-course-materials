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

    extract_audio = "Extract Audio 🎵"
    make_photo_video = "Make Photo Video 🎵📷📹"

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
    STATE = "_state_"  
    FILE_PATH = "_filepath_"
    TASKS_QUEUE = "tasks_queue"
    
class Values:
    CONFIRM_KB_REMOVAL = "_confirm_kb_removal_"
    CANCEL_KB_REMOVAL = "_cancel_kb_removal_"
    CONFIRM_DOWNLOAD = "_confirm_download_"
    SEND_MUSICVID = "_send_musicvideo_"
    SEND_PHOTO_ALBUM = "_send_photo_album_"
    SEND_MUSIC = "_send_music_"

    
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
            [Buttons.extract_audio, Buttons.make_photo_video]

        ]
    )

    
    


def is_audio(filename:str) -> bool:
    return filename.endswith('.mp3') or filename.endswith('.ogg') or filename.endswith(".wav") or filename.endswith('.m4a')