import unittest
from app import create_app
from models import db, PropertyModel, TenantModel, TaskModel, ingest_data

class IngestionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_ingest_data(self):
        ingest_data()
        properties = PropertyModel.query.all()
        tenants = TenantModel.query.all()
        tasks = TaskModel.query.all()

        self.assertGreater(len(properties), 0)
        self.assertGreater(len(tenants), 0)
        self.assertGreater(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()