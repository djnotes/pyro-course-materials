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
        return "Task = task_id = {0}, task_type: {1}, in_file: {2}, out_file: {3}, user_id: {4}".format(self.task_type, self.msg_id, self.user_id)

    def __init__(self, task_id = str(uuid.uuid1()), task_type: TaskType = None, in_file: str = None, out_file: str = None, user_id: int = None):
        self.task_id = task_id
        self.task_type = task_type
        self.in_file = in_file
        self.out_file = out_file
        self.user_id = user_id

