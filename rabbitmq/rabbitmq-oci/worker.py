import pika

from config import AppConfig
from task import TaskType
from utils import Keys
import dill as pickle
from pyrogram import Client
import os
import ffmpeg
from pika.credentials import PlainCredentials
from pika.exceptions import StreamLostError, AMQPError, AMQPConnectionError
import time
import shutil
from cache import Cache
from utils import Values
from utils import get_my_logger

appConf = AppConfig()

api_id = appConf.api_id
api_hash = appConf.api_hash
bot_token = appConf.bot_token


RECONNECT_DELAY = 5

cache = Cache()

logger = get_my_logger()


proxy_info = ({
    "scheme": appConf.proxy_scheme,
    "hostname": appConf.proxy_host,
    "port": int(appConf.proxy_port)
 } if appConf.proxy_on else None)


def consume_tasks():
    while True:
        connection = None
        try:
            # 1. Attempt to connect
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=appConf.rabbitmq_host, 
                port=5672, 
                virtual_host= appConf.rabbitmq_vhost,
                credentials= pika.PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password),
                heartbeat=Values.DEFAULT_CONN_TIMEOUT
            ))
            channel = connection.channel()
            
            channel.queue_declare(queue=Keys.TASKS_QUEUE, durable=True)
            
            # Set up the consumer callback
            channel.basic_consume(
                queue=Keys.TASKS_QUEUE,
                on_message_callback=process_task, # Your function to handle the message
                auto_ack=False # Or True, depending on your needs
            )

            logger.info("Worker connected and waiting for tasks...")
            # 2. Start blocking consumption (This is where the worker waits)
            channel.start_consuming()

            
        except (StreamLostError, AMQPError, AMQPConnectionError) as e:
            # 3. Handle connection loss (This is the critical part!)
            logger.error(f"Connection lost. Reconnecting in {RECONNECT_DELAY} seconds... Error: {e}")
            
        except KeyboardInterrupt:
            # Clean exit
            logger.info("Exiting worker.")
            break
        
        except Exception as e:
            # Catch any other unexpected errors
            logger.error(f"Unexpected error in consume_tasks: {e}")
        
        finally:
            # 4. Ensure connection is closed cleanly before the loop continues
            if connection is not None:
                try:
                    if not connection.is_closed:
                        connection.close()
                        logger.info("Connection closed.")
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
            
            # Wait before reconnecting
            time.sleep(RECONNECT_DELAY)




bot = Client("session/bot2", api_id = api_id, api_hash = api_hash, bot_token = bot_token, proxy=proxy_info if appConf.proxy_on else None)
logger.info("Starting {0}...".format(bot.name))

bot.start()

info = bot.get_me()
time_str = time.strftime("%H:%M:%S")

bot.send_message(chat_id = int(appConf.bot_admin), text = f"{__name__}:{bot.name}:{info.first_name} launched inside worker file")


logger.info(f'app conf initialized: {appConf}')


def acknowledge_message_with_retry(ch, method, task_id, max_retries=3):
    """
    Attempt to acknowledge a message. If connection is lost, create a temporary
    connection to send the ack. This ensures the message is removed from the queue
    even if the original connection died during processing.
    """
    try:
        ch.basic_ack(delivery_tag = method.delivery_tag)
        logger.debug(f"Message acknowledged for task {task_id}")
        return True
    except Exception as e:
        logger.warning(f"Failed to acknowledge on current channel: {e}. Attempting with new connection...")
        
        # Try with a fresh connection
        for attempt in range(max_retries):
            try:
                temp_conn = pika.BlockingConnection(pika.ConnectionParameters(
                    host=appConf.rabbitmq_host, 
                    port=5672, 
                    virtual_host=appConf.rabbitmq_vhost,
                    credentials=pika.PlainCredentials(appConf.rabbitmq_user, appConf.rabbitmq_password),
                    heartbeat=Values.DEFAULT_CONN_TIMEOUT
                ))
                temp_channel = temp_conn.channel()
                temp_channel.basic_ack(delivery_tag = method.delivery_tag)
                temp_conn.close()
                logger.info(f"Message acknowledged via new connection (attempt {attempt + 1}) for task {task_id}")
                return True
            except Exception as retry_e:
                logger.warning(f"Retry {attempt + 1}/{max_retries} failed: {retry_e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        logger.error(f"Failed to acknowledge message after {max_retries} retries. Message may be requeued.")
        return False


def process_task(ch, method, props, body):
    task = pickle.loads(body)

    logger.info('Received {0}'.format(task))
    try:
        match(task.task_type):
            case TaskType.EXTRACT_AUDIO:
                logger.info("Downloading video...")
                try:
                    message = bot.get_messages(task.user_id, task.msg_id)
                    filepath = bot.download_media(message)
                    # Remove spaces from file name
                    filepath_nospaces = filepath.replace(" ", "-").strip()
                    shutil.move(filepath, filepath_nospaces)
                    _out_filename, _ = os.path.splitext(filepath_nospaces)
                    out_filename = _out_filename + ".mp3"                
                except Exception as e:
                    logger.error("Failed to prepare file: {0}".format(e))
                    raise  # Re-raise to trigger outer except and ack

                try:
                    status = ffmpeg.input(filepath_nospaces).output(out_filename).overwrite_output().run()
                    if status[1]:
                        message.reply("Problem with extracting audio file. Try again")
                        logger.warning("FFmpeg returned error status: {0}".format(status))
                    else:
                        bot.send_audio(chat_id = task.user_id, audio = out_filename, caption = "Here is your extracted audio")
                        logger.info("Audio sent successfully to user {0}".format(task.user_id))

                except Exception as e:
                    logger.error("Error occurred during media conversion: {0}".format(e))
                    raise  # Re-raise to trigger outer except and ack
                    
            case TaskType.MERGE_VIDEO:
                pass
    except Exception as e:
        logger.error("Task processing failed: {0}. Message will be acknowledged to prevent infinite requeue.".format(e))
    finally:
        # CRITICAL: Always acknowledge the message, even on errors
        # This prevents infinite requeue loops. Failed tasks should be logged for manual inspection.
        # If the connection was lost during processing, retry with a new connection.
        acknowledge_message_with_retry(ch, method, task.task_id, max_retries=3)
        
        # mark background process as complete
        try:
            tasks_count = int(cache.get_session_item(task.user_id, Keys.BG_TASKS_RUNNING, 0))
            if tasks_count >= 1:
                tasks_count = tasks_count - 1
            else:
                tasks_count = 0
            cache.update_user_session(task.user_id, Keys.BG_TASKS_RUNNING, tasks_count, tasks_count * Values.MAX_JOB_RUNNING_TIME)
        except Exception as e:
            logger.error(f"Failed to update task count for user {task.user_id}: {e}")

            

consume_tasks()






