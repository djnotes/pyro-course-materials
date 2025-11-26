from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import pika
from pika.credentials import PlainCredentials
from config import AppConfig
from task import Task
import dill as pickle
from pika.exceptions import AMQPConnectionError, StreamLostError
import logging



appConf = AppConfig()

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
    TASKS_QUEUE = "media_tasks_queue"
    BG_TASKS_RUNNING = "bg_tasks" # Key to keep track of background tasks
    DEFAULT_LOGGER = "default_logger"
    DEFAULT_LOG_FILENAME = "bot.log"
    
class Values:
    CONFIRM_KB_REMOVAL = "_confirm_kb_removal_"
    CANCEL_KB_REMOVAL = "_cancel_kb_removal_"
    CONFIRM_DOWNLOAD = "_confirm_download_"
    SEND_MUSICVID = "_send_musicvideo_"
    SEND_PHOTO_ALBUM = "_send_photo_album_"
    SEND_MUSIC = "_send_music_"
    MAX_JOB_RUNNING_TIME = 1 * 60 # (1 minue)
    DEFAULT_CONN_TIMEOUT = 600 # Rabbitmq connection heartbeat


def get_my_logger():
    """
    Returns a basic logger for the app
    """
    # Set up logger
    logger = logging.Logger(Keys.DEFAULT_LOGGER)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler(Keys.DEFAULT_LOG_FILENAME))
    logger.setLevel(logging.DEBUG)    

    return logger

# define a basic loggervariable
logger = get_my_logger()


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


def send_task_to_rabbitmq(task):
    connection = None
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=appConf.rabbitmq_host,
                port=5672,
                virtual_host=appConf.rabbitmq_vhost,
                credentials=PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password),
                heartbeat=Values.DEFAULT_CONN_TIMEOUT
            )
        )

        channel = connection.channel()
        channel.queue_declare(Keys.TASKS_QUEUE, durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key=Keys.TASKS_QUEUE,
            body=pickle.dumps(task)
        )
        logger.info("Task published successfully.")

    except Exception as e:
        logger.info(f"Failed to publish task: {e}")
        raise e # Re-raise if you want the caller to handle it
        
    finally:
        # CRITICAL: Close the connection no matter what happens
        if connection and not connection.is_closed:
            connection.close()



