"""
    Endpoints for Tasks
"""
from flask import Blueprint, request, jsonify
from models import db, TaskModel
from schemas import TaskSchema
from .utils import paginate_query

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@bp.route("/", methods=["GET"])
def Get_list_tasks():
    query = TaskModel.query.order_by(TaskModel.TaskId)
    result = paginate_query(query, tasks_schema)
    return jsonify(result)

@bp.route("/", methods=["POST"])
def Create_task():
    data = request.get_json(force=True)
    task = task_schema.load(data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201

@bp.route("/<int:id>", methods=["GET"])
def Get_task(id):
    task = db.session.get(TaskModel, id)
    if task is None:
        return jsonify({"Message": f"Task id {id} not found"}), 404
        
    return jsonify(task_schema.dump(task))

@bp.route("/<int:id>", methods=["PUT"])
def Update_task(id):
    task = db.session.get(TaskModel, id)
    if task is None:
        return jsonify({"Message": f"Task id {id} not found"}), 404
        
    data = request.get_json(force=True)
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return jsonify(task_schema.dump(task))

@bp.route("/<int:id>", methods=["DELETE"])
def Delete_task(id):
    task = db.session.get(TaskModel, id)
    if task is None:
        return jsonify({"Message": f"Task id {id} not found"}), 404
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"Message": f"Task id {id} deleted successfully"}), 204
