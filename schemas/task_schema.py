from marshmallow import Schema, fields, post_load
from models import TaskModel
from validators.statuses import TASK_STATUS

class TaskSchema(Schema):
    TaskId = fields.Int(dump_only=True)
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