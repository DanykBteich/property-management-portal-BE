import unittest
import os
from app import create_app
from models import db, TenantModel, PropertyModel

class TenantTestCase(unittest.TestCase):
    def setUp(self):
        self.version = os.getenv("VERSION_NUMBER", "v1")
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create a property for tenant foreign key
            prop = PropertyModel(PropAddress="Test Property", PropType="Residential", PropStatus="Vacant", PropPurchaseDate="2023-01-01", PropPrice=100000)
            db.session.add(prop)
            db.session.commit()
            self.prop_id = prop.PropId

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_tenant(self):
        data = {
            "TenantName": "John Doe",
            "TenantContactInfo": "john@example.com",
            "TenantLeaseTermStart": "2023-01-01",
            "TenantLeaseTermEnd": "2023-12-31",
            "TenantRentalPaymentStatus": "Paid",
            "PropId": self.prop_id
        }
        response = self.client.post(f"/api/{self.version}/tenants/", json=data)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data["TenantName"], data["TenantName"])

    def test_get_tenants(self):
        response = self.client.get(f"/api/{self.version}/tenants/")
        self.assertEqual(response.status_code, 200)

    def test_update_tenant(self):
        with self.app.app_context():
            tenant = TenantModel(TenantName="Old Name", TenantContactInfo="old@example.com", TenantLeaseTermStart="2023-01-01", TenantLeaseTermEnd="2023-12-31", TenantRentalPaymentStatus="Paid", PropId=self.prop_id)
            db.session.add(tenant)
            db.session.commit()
            tenant_id = tenant.TenantId

        update_data = {"TenantName": "New Name"}
        response = self.client.put(f"/api/{self.version}/tenants/{tenant_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["TenantName"], "New Name")

    def test_delete_tenant(self):
        with self.app.app_context():
            tenant = TenantModel(TenantName="Delete Name", TenantContactInfo="delete@example.com", TenantLeaseTermStart="2023-01-01", TenantLeaseTermEnd="2023-12-31", TenantRentalPaymentStatus="Paid", PropId=self.prop_id)
            db.session.add(tenant)
            db.session.commit()
            tenant_id = tenant.TenantId

        response = self.client.delete(f"/api/{self.version}/tenants/{tenant_id}")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()