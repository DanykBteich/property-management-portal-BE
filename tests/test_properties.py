import unittest
import os
from app import create_app
from models import db, PropertyModel

class PropertyTestCase(unittest.TestCase):
    def setUp(self):
        self.version = os.getenv("VERSION_NUMBER", "v1")
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_property(self):
        data = {
            "PropAddress": "123 Test St",
            "PropType": "Residential",
            "PropStatus": "Vacant",
            "PropPurchaseDate": "2023-01-01",
            "PropPrice": 100000
        }
        response = self.client.post(f"/api/{self.version}/properties/", json=data)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data["PropAddress"], data["PropAddress"])

    def test_get_properties(self):
        response = self.client.get(f"/api/{self.version}/properties/")
        self.assertEqual(response.status_code, 200)

    def test_update_property(self):
        with self.app.app_context():
            prop = PropertyModel(PropAddress="Old Address", PropType="Residential", PropStatus="Vacant", PropPurchaseDate="2023-01-01", PropPrice=100000)
            db.session.add(prop)
            db.session.commit()
            prop_id = prop.PropId

        update_data = {"PropAddress": "New Address"}
        response = self.client.put(f"/api/{self.version}/properties/{prop_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["PropAddress"], "New Address")

    def test_delete_property(self):
        with self.app.app_context():
            prop = PropertyModel(PropAddress="Delete Address", PropType="Residential", PropStatus="Vacant", PropPurchaseDate="2023-01-01", PropPrice=100000)
            db.session.add(prop)
            db.session.commit()
            prop_id = prop.PropId

        response = self.client.delete(f"/api/{self.version}/properties/{prop_id}")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()