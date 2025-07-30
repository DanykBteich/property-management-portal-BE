import unittest
from app import create_app
from models import db, Property, Tenant, Task
from models.ingestion import ingest_data

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
        properties = Property.query.all()
        tenants = Tenant.query.all()
        tasks = Task.query.all()

        self.assertGreater(len(properties), 0)
        self.assertGreater(len(tenants), 0)
        self.assertGreater(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()