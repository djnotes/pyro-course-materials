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
        return "Task = task_type = {0}, message: {1}".format(self.task_type, self.message)

    def __init__(self, task_id = str(uuid.uuid1()), task_type: TaskType = None, message: Message = None, user_id = None):
        self.task_id = task_id
        self.task_type = task_type
        self.message = message
        self.user_id = user_id
