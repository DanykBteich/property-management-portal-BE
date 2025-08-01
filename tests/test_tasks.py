import unittest
import os
from app import create_app
from models import db, TaskModel, PropertyModel

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.version = os.getenv("VERSION_NUMBER", "v1")
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create a property for task foreign key
            prop = PropertyModel(PropAddress="Test Property", PropType="Residential", PropStatus="Vacant", PropPurchaseDate="2023-01-01", PropPrice=100000)
            db.session.add(prop)
            db.session.commit()
            self.prop_id = prop.PropId

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        data = {
            "TaskDescription": "Fix sink",
            "TaskStatus": "Pending",
            "TaskScheduledDate": "2023-06-01",
            "PropId": self.prop_id
        }
        response = self.client.post(f"/api/{self.version}/tasks/", json=data)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data["TaskDescription"], data["TaskDescription"])

    def test_get_tasks(self):
        response = self.client.get(f"/api/{self.version}/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        with self.app.app_context():
            task = TaskModel(TaskDescription="Old Task", TaskStatus="Pending", TaskScheduledDate="2023-06-01", PropId=self.prop_id)
            db.session.add(task)
            db.session.commit()
            task_id = task.TaskId

        update_data = {"TaskDescription": "Updated Task"}
        response = self.client.put(f"/api/{self.version}/tasks/{task_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["TaskDescription"], "Updated Task")

    def test_delete_task(self):
        with self.app.app_context():
            task = TaskModel(TaskDescription="Delete Task", TaskStatus="Pending", TaskScheduledDate="2023-06-01", PropId=self.prop_id)
            db.session.add(task)
            db.session.commit()
            task_id = task.TaskId

        response = self.client.delete(f"/api/{self.version}/tasks/{task_id}")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()