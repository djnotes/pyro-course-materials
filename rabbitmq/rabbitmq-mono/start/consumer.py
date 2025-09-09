import pika

from config import AppConfig
from task import TaskType
from util import Keys
import dill as pickle
from pyrogram import Client
import os
import ffmpeg
from pika.credentials import PlainCredentials
import time
import shutil

appConf = AppConfig()

api_id = appConf.api_id
api_hash = appConf.api_hash
bot_token = appConf.bot_token

proxy = {
    "scheme": appConf.proxy_scheme,
    "hostname": appConf.proxy_host,
    "port": int(appConf.proxy_port)
} if appConf.proxy_on else None

bot = Client("session/bot2", api_id = api_id, api_hash = api_hash, bot_token = bot_token, proxy = proxy)


bot.start()

info = bot.get_me()

bot.send_message(chat_id = appConf.bot_admin, text = f"{bot.name}:{info.first_name} started")

# TODO 1: Create connection


print(f'app conf initialized')

# TODO 2: Create channel

# TODO 3: Create rabbitmq callback

# TODO 4: start consuming