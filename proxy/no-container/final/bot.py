from logger import AppLogger
from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler 
from myhandler import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
import logging
import configparser

# logging.basicConfig(filename = "log/app.log", format = "%(filename)s - %(lineno)s: %(message)s", level = logging.DEBUG, force = True)

# logger = logging.getLogger()

logger = AppLogger(__name__)

from myhandler import handle_callback_query

import os

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')

proxy_status = os.environ.get('PROXY_STATUS')

if proxy_status == 'ON':
   my_proxy = {
      'scheme': os.environ.get('PROXY_SCHEME'),
      'hostname': os.environ.get('PROXY_HOSTNAME'),
      'port': int(os.environ.get('PROXY_PORT')),
      'username': os.environ.get('PROXY_USERNAME'),
      'password': os.environ.get('PROXY_PASSWORD')
   }
else:
   config_parser = configparser.ConfigParser()
   config_parser.read('env.ini')
   proxy_status = config_parser['proxy']['PROXY_STATUS']
   my_proxy = {
      'scheme': config_parser['proxy']['PROXY_SCHEME'],
      'hostname': config_parser['proxy']['PROXY_HOSTNAME'],
      'port': int(config_parser['proxy']['PROXY_PORT']),
      'username': config_parser['proxy']['PROXY_USERNAME'],
      'password': config_parser['proxy']['PROXY_PASSWORD']
   }
   

app = Client(
    name = "session/myapp",
    api_id = api_id,
    api_hash = api_hash,
    bot_token=bot_token,
    proxy = my_proxy if proxy_status == 'ON' else None 
)


# @app.on_message()
app.add_handler(MessageHandler(handle_updates))
app.add_handler(CallbackQueryHandler(handle_callback_query))

logger.info(f"Starting {app.name}")
app.start()
 
 
info = app.get_me()

logger.info(f"Sending bootstrap message to {info.first_name}")
app.send_message(chat_id = "dev2000xx", text = f"{info.first_name} started")

logger.info("Keeping the bot idle")
idle()

logger.info("Stopping the app")
app.stop()
