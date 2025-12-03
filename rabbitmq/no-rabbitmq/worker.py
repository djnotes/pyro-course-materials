import functools
import concurrent.futures
import multiprocessing
import time
import os
import ffmpeg
from pyrogram import Client
from utils import get_my_logger
from task import Task
from cache import Cache
from utils import Keys

cache = Cache()


logger= get_my_logger()
# Set up a global pool outside of any request/task function
# Use context to manage the pool lifecycle
executor = concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count() - 1)

def audio_extractor(task):
    """Worker function run by the process pool."""
    logger.info('Audio extraction process started using {0} CPUs'.format(multiprocessing.cpu_count()))
    in_file = task.in_file
    out_file = task.out_file
    user_id = task.user_id
    task_type = task.task_type
    logger.info(f"Process {os.getpid()} starting {task_type} work for user {user_id}")
    success = False
    error = None
    try:
        start = time.time()
        status = ffmpeg.input(in_file).output(out_file).overwrite_output().run()
        end = time.time()
        logger.info("Audio extraction completed in {0} seconds".format(end - start))
        if status[1]:
            logger.warning("FFmpeg returned error status: {0}".format(status))
            error = status[1]
        else:
            success = True
            logger.info("Audio extraction completed inside audio_extractor")

    except Exception as e:
        logger.error("Error occurred during media conversion: {0}".format(e))
        raise  # Re-raise to trigger outer except and ack
    
    result = out_file if success else error
    # NOTE: This function MUST NOT use the Pyrogram client or Redis connection objects
    return result, user_id, success

def send_result_callback_with_client(client: Client, future):
    """
    Callback that explicitly receives the client instance.
    """
    try:
        pass
        # Use the client received as an argument
        result, user_id, success = future.result()
        
        if success:
            client.send_audio(chat_id = user_id, audio = result)
        else:
            client.send_message(chat_id = user_id, text = f"Error during audio extraction: {result}")
        # Update background tasks count in cache
        tasks_count = cache.get_session_item(user_id, Keys.BG_TASKS_RUNNING, 0)
        
        if tasks_count and tasks_count > 0:
            tasks_count -= 1
            cache.update_user_session(user_id, Keys.BG_TASKS_RUNNING, tasks_count)
        else:
            tasks_count = 0
    except Exception as e:
        logger.error("Error occurred in callback: {0}".format(e))
        # Handle exceptions appropriately
        client.send_message(chat_id = user_id, text = f"An error occurred: {e}")
        



def submit_new_task(client: Client, task: Task):
    """ Submits tasks to multiprocessing pool and attaches callback. """
    
    # 1. Start the job
    future = executor.submit(audio_extractor, task)
    
    # 2. Use partial() to lock the client argument into the callback
    ready_callback = functools.partial(send_result_callback_with_client, client)
    
    # 3. Attach the configured callback
    future.add_done_callback(ready_callback)