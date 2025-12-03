from pyrogram import Client 
import shutil
from pyrogram.types import Message, ReplyKeyboardRemove
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import AppConfig
from utils import Buttons, is_audio
from utils import Keyboards
from utils import Values
from cache import Cache
from utils import Keys
import ffmpeg
from pyrogram.types import CallbackQuery
from utils import get_my_logger
from worker import submit_new_task
import os


appConf = AppConfig()

logger = get_my_logger()

logger.info(f"myhandler: app conf initialized: ${appConf}")

from task import *


cache = Cache()



async def handle_updates(client: Client, message: Message):
    uid = message.from_user.id
    text = message.text
    media = message.media
    state = cache.get_session_item(uid, Keys.STATE)

    
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
            await message.reply(text = "Media Menu", reply_markup= Keyboards.MediaMenu)
        case Buttons.extract_audio:
            await message.reply(text = "Send a music video file")
            cache.update_user_session(uid, key = Keys.STATE, value = Values.SEND_MUSICVID)
        case Buttons.make_photo_video:
            await message.reply("Send a photo album for generating the music video")
            cache.update_user_session(uid, key = Keys.STATE, value = Values.SEND_PHOTO_ALBUM)

    match state:
        case Values.SEND_MUSICVID:
            if not media:
                await message.reply("Wrong input. Expecting music video file")
                return
            
            # Query task from queue
            tasks_count = int(cache.get_session_item(uid, Keys.BG_TASKS_RUNNING, 0))
            if tasks_count >= 1:
                await message.reply("Your queue is busy. Please wait...")
                return
            else:

                # Prepare task
                logger.info("Received media message. Downloading file...")
                status_msg = await message.reply("Download started...")
                filepath = await client.download_media(message, progress = download_progress, progress_args = (status_msg,))
                filepath_nospaces = filepath.replace(" ", "-").strip()
                # Remove spaces from file name
                shutil.move(filepath, filepath_nospaces)
                _out_filename, _ = os.path.splitext(filepath_nospaces)
                out_filename = _out_filename + ".mp3"                
                
                task = Task(task_type = TaskType.EXTRACT_AUDIO, in_file = filepath_nospaces , out_file= out_filename, user_id = uid)

                # Send task to background process without RabbitMQ
                tasks_count = tasks_count + 1
                # Set appropriate timeout for the task given the number of tasks
                cache.update_user_session(uid, Keys.BG_TASKS_RUNNING, tasks_count, tasks_count * Values.MAX_JOB_RUNNING_TIME)
                
                await message.reply("Download complete. Starting audio extraction... \nPlease wait...")

                submit_new_task(client, task)
                
            
        case Values.SEND_PHOTO_ALBUM:
            if not media:
                await message.reply("Wrong input. Expecting photo file or photo album")
                return
            path = await client.download_media(message)
            cache.update_user_session(uid, Keys.FILE_PATH, path)
            cache.update_user_session(uid, Keys.STATE, Values.SEND_MUSIC)
            await message.reply("Send a music file for creating the music video")
        case Values.SEND_MUSIC:
            if not media:
                await message.reply("Wrong input. Expecting music file")
                return
            audio_path = await client.download_media(message)
            image_path = cache.get_session_item(uid, Keys.FILE_PATH)
            outfile = 'downloads/{0}-musicvideo.mp4'.format(uid)

            try:
                # Get audio duration
                probe = ffmpeg.probe(audio_path)
                audio_info = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
                duration = float(probe['format']['duration'])

                # Create video from image
                video = ffmpeg.input(image_path, loop=1, t=duration)
                audio = ffmpeg.input(audio_path)

                # Combine video and audio
                output = ffmpeg.output(
                    video,
                    audio,
                    outfile,
                    vcodec='libx264',  # Use H.264 codec for video
                    acodec='aac',      # Use AAC codec for audio
                    pix_fmt='yuv420p', # Pixel format for better compatibility
                    shortest=None      # End when the shortest input ends
                )

                # Run the FFmpeg command
                output.overwrite_output().run()
                logger.info(f"Video successfully created: {outfile}")

            except ffmpeg.Error as e:
                logger.info(f"An error occurred: {e.stderr.decode()}")
            except Exception as e:
                logger.info("Error: {0}".format(e))
            await message.reply_video(outfile, caption = 'Your merged video')            
        



async def handle_callback_query(client: Client, query: CallbackQuery):
    uid = query.from_user.id
    match query.data:
        case Values.CONFIRM_KB_REMOVAL:
            await client.send_message(chat_id = query.from_user.id, text = "You removed the keyboard", reply_markup=ReplyKeyboardRemove())
        case Values.CANCEL_KB_REMOVAL:
            await client.send_message(chat_id = query.from_user.id, text = "You selected No")
        case Values.CONFIRM_DOWNLOAD:
            media_msg = cache.get_session_item(uid, Keys.MEDIA_MESSAGE)
            msg = await query.message.reply("Download started")
            await client.download_media(media_msg, progress = download_progress, progress_args= (msg, ))
            await client.send_message(chat_id = uid, text = "Download complete")


async def send_progress(current, total, *args):
    msg = args[0]
    await msg.edit("Sending {0} of {1} KB".format(current / 1_000, total / 1_000))
    if current >= total:
        await msg.edit("Transfer complete")


async def download_progress(current, total, *args):
    msg = args[0]
    await msg.edit("Downloading {0} of {1} KB".format(current / 1_000, total / 1_000))
    if current >= total:
        await msg.edit("Download to server complete")