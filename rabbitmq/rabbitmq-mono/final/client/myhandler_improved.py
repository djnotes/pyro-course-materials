import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import asyncio

from pyrogram import Client
from pyrogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import ffmpeg

from util import Buttons, is_audio, Keyboards, Values, Keys
from cache import Cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DOWNLOADS_DIR = Path("downloads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
SUPPORTED_AUDIO_FORMATS = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

# Error messages
ERROR_MESSAGES = {
    'wrong_input_video': "Wrong input. Please send a valid music video file.",
    'wrong_input_photo': "Wrong input. Please send a valid photo file or photo album.",
    'wrong_input_audio': "Wrong input. Please send a valid music file.",
    'audio_extraction_failed': "Failed to extract audio from the video file.",
    'video_creation_failed': "Failed to create music video.",
    'file_too_large': f"File is too large. Maximum size allowed is {MAX_FILE_SIZE // (1024*1024)}MB.",
    'unsupported_format': "Unsupported file format.",
}

cache = Cache()


class MediaProcessor:
    """Handles media processing operations using FFmpeg."""
    
    @staticmethod
    async def extract_audio_from_video(video_path: str, output_path: str) -> bool:
        """Extract audio from video file."""
        try:
            (
                ffmpeg
                .input(video_path)
                .output(output_path, acodec='mp3', audio_bitrate='192k')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            logger.info(f"Audio extracted successfully: {output_path}")
            return True
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error during audio extraction: {e.stderr.decode()}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during audio extraction: {e}")
            return False

    @staticmethod
    async def create_music_video(image_path: str, audio_path: str, output_path: str) -> bool:
        """Create music video from image and audio."""
        try:
            # Get audio duration
            probe = ffmpeg.probe(audio_path)
            duration = float(probe['format']['duration'])
            
            # Create video from image and audio
            video_stream = ffmpeg.input(image_path, loop=1, t=duration)
            audio_stream = ffmpeg.input(audio_path)
            
            output = ffmpeg.output(
                video_stream,
                audio_stream,
                output_path,
                vcodec='libx264',
                acodec='aac',
                pix_fmt='yuv420p',
                r=30,  # Frame rate
                shortest=None
            )
            
            output.overwrite_output().run(capture_stdout=True, capture_stderr=True)
            logger.info(f"Music video created successfully: {output_path}")
            return True
            
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error during video creation: {e.stderr.decode()}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during video creation: {e}")
            return False


class FileValidator:
    """Validates file types and sizes."""
    
    @staticmethod
    def validate_file_size(file_path: str) -> bool:
        """Check if file size is within limits."""
        try:
            file_size = os.path.getsize(file_path)
            return file_size <= MAX_FILE_SIZE
        except OSError:
            return False
    
    @staticmethod
    def validate_file_format(file_path: str, allowed_formats: set) -> bool:
        """Check if file format is supported."""
        file_extension = Path(file_path).suffix.lower()
        return file_extension in allowed_formats
    
    @staticmethod
    def validate_video_file(file_path: str) -> bool:
        """Validate video file."""
        return (FileValidator.validate_file_size(file_path) and 
                FileValidator.validate_file_format(file_path, SUPPORTED_VIDEO_FORMATS))
    
    @staticmethod
    def validate_audio_file(file_path: str) -> bool:
        """Validate audio file."""
        return (FileValidator.validate_file_size(file_path) and 
                FileValidator.validate_file_format(file_path, SUPPORTED_AUDIO_FORMATS))
    
    @staticmethod
    def validate_image_file(file_path: str) -> bool:
        """Validate image file."""
        return (FileValidator.validate_file_size(file_path) and 
                FileValidator.validate_file_format(file_path, SUPPORTED_IMAGE_FORMATS))


class KeyboardFactory:
    """Factory for creating keyboard markups."""
    
    @staticmethod
    def create_confirmation_keyboard() -> InlineKeyboardMarkup:
        """Create confirmation keyboard for removing keyboard."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Yes", callback_data=Values.CONFIRM_KB_REMOVAL),
                    InlineKeyboardButton(text="No", callback_data=Values.CANCEL_KB_REMOVAL)
                ]
            ]
        )
    
    @staticmethod
    def create_links_keyboard() -> InlineKeyboardMarkup:
        """Create inline keyboard with social media links."""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="My Telegram Channel", url="https://t.me/codewithmehdi")],
            [InlineKeyboardButton(text="My YouTube Channel", url="https://youtube.com/mehdihaghgoo")],
            [InlineKeyboardButton(text="My GitHub Profile", url="https://github.com/djnotes")]
        ])


class MessageHandler:
    """Handles different types of messages."""
    
    def __init__(self):
        self.media_processor = MediaProcessor()
        self.file_validator = FileValidator()
    
    async def handle_menu_commands(self, message: Message, text: str) -> bool:
        """Handle menu-related commands."""
        menu_handlers = {
            "/start": lambda: message.reply("Main Menu", reply_markup=Keyboards.MainMenu),
            Buttons.home: lambda: message.reply("Main Menu", reply_markup=Keyboards.MainMenu),
            Buttons.settings: lambda: message.reply("Settings Menu", reply_markup=Keyboards.SettingsMenu),
            Buttons.admins: lambda: message.reply("Admins Menu", reply_markup=Keyboards.AdminsMenu),
            Buttons.media: lambda: message.reply("Media Menu", reply_markup=Keyboards.MediaMenu),
        }
        
        if text in menu_handlers:
            await menu_handlers[text]()
            return True
        return False
    
    async def handle_keyboard_commands(self, message: Message, text: str) -> bool:
        """Handle keyboard-related commands."""
        if text == Buttons.remove_keyboard:
            confirm_kb = KeyboardFactory.create_confirmation_keyboard()
            await message.reply("Are you sure you want to remove the keyboard?", reply_markup=confirm_kb)
            return True
        elif text == Buttons.make_inline_links:
            links_kb = KeyboardFactory.create_links_keyboard()
            await message.reply("My Links", reply_markup=links_kb)
            return True
        return False
    
    async def handle_media_commands(self, message: Message, text: str, uid: int) -> bool:
        """Handle media processing commands."""
        if text == Buttons.extract_audio:
            await message.reply("Send a music video file")
            cache.update_user_session(uid, Keys.STATE, Values.SEND_MUSICVID)
            return True
        elif text == Buttons.make_photo_video:
            await message.reply("Send a photo album for generating the music video")
            cache.update_user_session(uid, Keys.STATE, Values.SEND_PHOTO_ALBUM)
            return True
        return False
    
    async def handle_audio_extraction(self, client: Client, message: Message, uid: int) -> None:
        """Handle audio extraction from video."""
        if not message.media:
            await message.reply(ERROR_MESSAGES['wrong_input_video'])
            return
        
        try:
            # Download video file
            video_path = await client.download_media(message)
            
            # Validate video file
            if not self.file_validator.validate_video_file(video_path):
                await message.reply(ERROR_MESSAGES['unsupported_format'])
                self._cleanup_file(video_path)
                return
            
            # Generate output filename
            video_file = Path(video_path)
            output_path = str(video_file.with_suffix('.mp3'))
            
            # Extract audio
            success = await self.media_processor.extract_audio_from_video(video_path, output_path)
            
            if success:
                await message.reply_audio(audio=output_path, caption="Your extracted audio file")
            else:
                await message.reply(ERROR_MESSAGES['audio_extraction_failed'])
            
            # Cleanup
            self._cleanup_file(video_path)
            if success:
                self._cleanup_file(output_path)
                
        except Exception as e:
            logger.error(f"Error in audio extraction: {e}")
            await message.reply(ERROR_MESSAGES['audio_extraction_failed'])
    
    async def handle_photo_upload(self, client: Client, message: Message, uid: int) -> None:
        """Handle photo upload for music video creation."""
        if not message.media:
            await message.reply(ERROR_MESSAGES['wrong_input_photo'])
            return
        
        try:
            photo_path = await client.download_media(message)
            
            if not self.file_validator.validate_image_file(photo_path):
                await message.reply(ERROR_MESSAGES['unsupported_format'])
                self._cleanup_file(photo_path)
                return
            
            cache.update_user_session(uid, Keys.FILE_PATH, photo_path)
            cache.update_user_session(uid, Keys.STATE, Values.SEND_MUSIC)
            await message.reply("Send a music file for creating the music video")
            
        except Exception as e:
            logger.error(f"Error in photo upload: {e}")
            await message.reply(ERROR_MESSAGES['wrong_input_photo'])
    
    async def handle_music_upload(self, client: Client, message: Message, uid: int) -> None:
        """Handle music upload and video creation."""
        if not message.media:
            await message.reply(ERROR_MESSAGES['wrong_input_audio'])
            return
        
        try:
            audio_path = await client.download_media(message)
            
            if not self.file_validator.validate_audio_file(audio_path):
                await message.reply(ERROR_MESSAGES['unsupported_format'])
                self._cleanup_file(audio_path)
                return
            
            image_path = cache.get_session_item(uid, Keys.FILE_PATH)
            if not image_path or not os.path.exists(image_path):
                await message.reply("Image file not found. Please start over.")
                self._cleanup_file(audio_path)
                return
            
            # Create output directory if it doesn't exist
            DOWNLOADS_DIR.mkdir(exist_ok=True)
            output_path = DOWNLOADS_DIR / f"{uid}-musicvideo.mp4"
            
            # Create music video
            success = await self.media_processor.create_music_video(
                image_path, audio_path, str(output_path)
            )
            
            if success:
                await message.reply_video(str(output_path), caption="Your merged video")
            else:
                await message.reply(ERROR_MESSAGES['video_creation_failed'])
            
            # Cleanup
            self._cleanup_file(audio_path)
            self._cleanup_file(image_path)
            if success:
                # Optionally cleanup the output video after sending
                # self._cleanup_file(str(output_path))
                pass
            
            # Clear user session
            cache.update_user_session(uid, Keys.STATE, None)
            cache.update_user_session(uid, Keys.FILE_PATH, None)
            
        except Exception as e:
            logger.error(f"Error in music video creation: {e}")
            await message.reply(ERROR_MESSAGES['video_creation_failed'])
    
    @staticmethod
    def _cleanup_file(file_path: str) -> None:
        """Safely remove a file."""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except OSError as e:
            logger.warning(f"Failed to cleanup file {file_path}: {e}")


async def handle_updates(client: Client, message: Message) -> None:
    """Main handler for incoming messages."""
    uid = message.from_user.id
    text = message.text
    state = cache.get_session_item(uid, Keys.STATE)
    
    handler = MessageHandler()
    
    # Handle text commands
    if text:
        # Try menu commands first
        if await handler.handle_menu_commands(message, text):
            return
        
        # Try keyboard commands
        if await handler.handle_keyboard_commands(message, text):
            return
        
        # Try media commands
        if await handler.handle_media_commands(message, text, uid):
            return
    
    # Handle state-based processing
    if state == Values.SEND_MUSICVID:
        await handler.handle_audio_extraction(client, message, uid)
    elif state == Values.SEND_PHOTO_ALBUM:
        await handler.handle_photo_upload(client, message, uid)
    elif state == Values.SEND_MUSIC:
        await handler.handle_music_upload(client, message, uid)


async def handle_callback_query(client: Client, query: CallbackQuery) -> None:
    """Handle callback queries from inline keyboards."""
    uid = query.from_user.id
    
    try:
        if query.data == Values.CONFIRM_KB_REMOVAL:
            await client.send_message(
                chat_id=uid,
                text="You removed the keyboard",
                reply_markup=ReplyKeyboardRemove()
            )
        elif query.data == Values.CANCEL_KB_REMOVAL:
            await client.send_message(chat_id=uid, text="You selected No")
        elif query.data == Values.CONFIRM_DOWNLOAD:
            media_msg = cache.get_session_item(uid, Keys.MEDIA_MESSAGE)
            if media_msg:
                msg = await query.message.reply("Download started")
                await client.download_media(
                    media_msg,
                    progress=download_progress,
                    progress_args=(msg,)
                )
                await client.send_message(chat_id=uid, text="Download complete")
            else:
                await client.send_message(chat_id=uid, text="No media found to download")
        
        # Answer the callback query to remove loading state
        await query.answer()
        
    except Exception as e:
        logger.error(f"Error handling callback query: {e}")
        await query.answer("An error occurred", show_alert=True)


async def send_progress(current: int, total: int, *args) -> None:
    """Progress callback for sending files."""
    msg = args[0]
    try:
        progress_percent = (current / total) * 100
        await msg.edit(f"Sending {current // 1000} of {total // 1000} KB ({progress_percent:.1f}%)")
        
        if current >= total:
            await msg.edit("Transfer complete")
    except Exception as e:
        logger.error(f"Error updating send progress: {e}")


async def download_progress(current: int, total: int, *args) -> None:
    """Progress callback for downloading files."""
    msg = args[0]
    try:
        progress_percent = (current / total) * 100
        await msg.edit(f"Downloading {current // 1000} of {total // 1000} KB ({progress_percent:.1f}%)")
        
        if current >= total:
            await msg.edit("Download to server complete")
    except Exception as e:
        logger.error(f"Error updating download progress: {e}")
