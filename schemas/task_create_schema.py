from marshmallow import Schema, fields, post_load
from models import TaskModel
from validators.statuses import TASK_STATUS

class TaskCreateSchema(Schema):
    TaskDescription = fields.Str(required=True)
    TaskStatus = fields.Str(required=True, validate=TASK_STATUS)
    TaskScheduledDate = fields.Date(required=True)
    PropId = fields.Int(required=True)

    @post_load
    def make_task(self, data, **kwargs):
        """
            Create a Task instance from the deserialized data
        """
        return TaskModel(**data)