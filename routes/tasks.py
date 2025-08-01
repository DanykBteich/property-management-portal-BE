"""
    Endpoints for Tasks
"""
import os
from flask import Blueprint, request, jsonify
from models import db, TaskModel
from schemas import TaskSchema, TaskCreateSchema
from .utils import paginate_query
from flasgger import swag_from

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

task_schema = TaskSchema()
task_create_schema = TaskCreateSchema()
tasks_schema = TaskSchema(many=True)

SPEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "specs", "tasks"))

@bp.route("/", methods=["GET"])
@swag_from(os.path.join(SPEC_DIR, "tasks_list.yaml"), methods=["GET"])
def Get_list_tasks():
    query = TaskModel.query.order_by(TaskModel.TaskId)
    result = paginate_query(query, tasks_schema)
    return jsonify(result)

@bp.route("/", methods=["POST"])
@swag_from(os.path.join(SPEC_DIR, "tasks_create.yaml"), methods=["POST"])
def Create_task():
    data = request.get_json(force=True)
    task = task_create_schema.load(data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_create_schema.dump(task)), 201

@bp.route("/<int:TaskId>", methods=["GET"])
@swag_from(os.path.join(SPEC_DIR, "tasks_get.yaml"), methods=["GET"])
def Get_task(TaskId):
    task = db.session.get(TaskModel, TaskId)
    if task is None:
        return jsonify({"Message": f"Task id {TaskId} not found"}), 404
        
    return jsonify(task_schema.dump(task))

@bp.route("/<int:TaskId>", methods=["PUT"])
@swag_from(os.path.join(SPEC_DIR, "tasks_update.yaml"), methods=["PUT"])
def Update_task(TaskId):
    task = db.session.get(TaskModel, TaskId)
    if task is None:
        return jsonify({"Message": f"Task id {TaskId} not found"}), 404
        
    data = request.get_json(force=True)
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return jsonify(task_create_schema.dump(task))

@bp.route("/<int:TaskId>", methods=["DELETE"])
@swag_from(os.path.join(SPEC_DIR, "tasks_delete.yaml"), methods=["DELETE"])
def Delete_task(TaskId):
    task = db.session.get(TaskModel, TaskId)
    if task is None:
        return jsonify({"Message": f"Task id {TaskId} not found"}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"Message": f"Task id {TaskId} deleted successfully"}), 204
