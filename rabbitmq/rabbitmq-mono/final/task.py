from enum import Enum
import uuid
from pyrogram.types import Message


class TaskType(Enum):
    """
    Use to specify different type of tasks sent to rabbitmq queue
    """
    MERGE_VIDEO = 1
    EXTRACT_AUDIO = 2

class Task:
    def __repr__(self):
        return "Task = task_type = {0}, chat_id: {1}, user_id: {2}, msg_id: {3}".format(self.task_type, self.chat_id, self.user_id, self.msg_id)

    def __init__(self, task_id = str(uuid.uuid1()), task_type: TaskType = None, chat_id: int = None, user_id: int = None, msg_id: int = None):
        self.task_id = task_id
        self.task_type = task_type
        self.chat_id = chat_id
        self.user_id = user_id
        self.msg_id = msg_id

