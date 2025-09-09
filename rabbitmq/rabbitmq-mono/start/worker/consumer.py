import pika

from config import AppConfig
from task import TaskType
from util import Keys
import dill as pickle
from pyrogram import Client
import os
import ffmpeg
from pika.credentials import PlainCredentials

appConf = AppConfig()

api_id = appConf.api_id
api_hash = appConf.api_hash
bot_token = appConf.bot_token


bot = Client("session/bot2", api_id = api_id, api_hash = api_hash, bot_token = bot_token)

print("Starting {0}...".format(bot.name))

bot.start()
print("Waiting 5 seconds")
import time
time.sleep(5)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host = appConf.rabbitmq_host,
        port = 5672,
        virtual_host=appConf.rabbitmq_vhost,
        # credentials=PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password)
        credentials=PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password)
    )
)

print(f'app conf initialized: {appConf}')

channel = connection.channel()

channel.queue_declare(Keys.TASKS_QUEUE, durable=True)

print("\tWaiting for tasks. To exit press Ctrl + C")


async def cb(ch, method, props, body):
    task = pickle.loads(body)
    print('Received {0}'.format(task.id))
    match(task.task_type):
        case TaskType.EXTRACT_AUDIO:
            message = task.message
            video = await bot.download_media(message)
            index = video.rindex('.')
            outfile = video.strip(video[index:]) + '.mp3' # Strip video extension
            status = ffmpeg.input(video).output(outfile).run()
            if status[1]:
                await message.reply("Problem with extracting audio file")
            await bot.send_audio(chat_id = task.user_id, audio = outfile, caption = "Here is your extracted audio")
            
        case TaskType.MERGE_VIDEO:
            pass
            
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=Keys.TASKS_QUEUE, on_message_callback=cb)

channel.start_consuming()
