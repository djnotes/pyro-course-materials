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


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host = appConf.rabbitmq_host,
        port = 5672,
        virtual_host= appConf.rabbitmq_vhost,
        credentials= pika.PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password)
    )
)

channel = connection.channel()

channel.queue_declare(Keys.TASKS_QUEUE, durable=True)

print(f'app conf initialized')


def cb(ch, method, props, body):
    task = pickle.loads(body)
    match task.task_type:
        case TaskType.EXTRACT_AUDIO:
            try:
                message = bot.get_messages(task.chat_id, task.msg_id)
                file = bot.download_media(message)
                file_nospace = file.replace(' ', '-').strip()
                shutil.move(file, file_nospace)
                filename, _ = os.path.splitext(file_nospace)
                outfilename = filename + ".mp3"
                status = ffmpeg.input(file_nospace).output(outfilename).overwrite_output().run()
                if status[1]: 
                    bot.send_message(chat_id=task.chat_id, text = "Failed to extract media file")
                else:
                    bot.send_audio(chat_id = task.chat_id, audio = outfilename, caption = "Here is your extracted audio")    
            
            except Exception as e:
                bot.send_message(chat_id = task.chat_id, text = "Failed to perform audio extraction")
        case _:
            pass
    
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=Keys.TASKS_QUEUE, on_message_callback=cb)

channel.start_consuming()
