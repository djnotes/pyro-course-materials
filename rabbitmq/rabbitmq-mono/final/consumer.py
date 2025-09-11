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
        virtual_host=appConf.rabbitmq_vhost,
        # credentials=PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password)
        credentials=PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password),
        heartbeat=30
    )
)

print(f'app conf initialized')

channel = connection.channel()

channel.queue_declare(Keys.TASKS_QUEUE, durable=True)


def cb(ch, method, props, body):
    task = pickle.loads(body)
    print('Received task {0}. chat_id: {1}, msg_id: {2}'.format(task.task_id, task.chat_id, task.msg_id))
    match(task.task_type):
        case TaskType.EXTRACT_AUDIO:
            try:
                message = bot.get_messages(task.chat_id, task.msg_id)
                filepath = bot.download_media(message)
                filepath_nospaces = filepath.replace(" ", "-").strip()
                shutil.move(filepath, filepath_nospaces)
                _out_filename, _ = os.path.splitext(filepath_nospaces)
                out_filename = _out_filename + ".mp3"                
            except Exception as e:
                print("Failed to prepare file: {0}".format(e))

            try:
                status = ffmpeg.input(filepath_nospaces).output(out_filename).overwrite_output().run()
                if status[1]:
                    message.reply("Problem with extracting audio file")                
                else:
                    bot.send_audio(chat_id = task.chat_id, audio = out_filename, caption = "Here is your extracted audio")

            except Exception as e:
                print("Error occurred during media conversion: {0}\n".format(e))
                

            # message.reply_audio(audio = out_filename, caption = "Here is your extracted audio")
            
        case TaskType.MERGE_VIDEO:
            pass
            
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=Keys.TASKS_QUEUE, on_message_callback=cb)

channel.start_consuming()
