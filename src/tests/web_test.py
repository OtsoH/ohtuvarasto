import unittest
from web.app import create_app
from web.storage import warehouse_storage


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()
        warehouse_storage.clear()

    def test_index_empty(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouses", response.data)
        self.assertIn(b"No warehouses yet", response.data)

    def test_create_warehouse(self):
        response = self.client.post("/warehouse/create", data={
            "name": "Test Warehouse",
            "capacity": 100
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Warehouse", response.data)
        self.assertIn(b"created successfully", response.data)

    def test_view_warehouse(self):
        warehouse_storage.create("View Test", 50)
        response = self.client.get("/warehouse/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"View Test", response.data)

    def test_view_nonexistent_warehouse(self):
        response = self.client.get("/warehouse/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse not found", response.data)

    def test_edit_warehouse(self):
        warehouse_storage.create("Edit Test", 100)
        response = self.client.post("/warehouse/1/edit", data={
            "name": "Updated Name",
            "capacity": 200
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated Name", response.data)
        self.assertIn(b"updated successfully", response.data)

    def test_add_items_success(self):
        warehouse_storage.create("Add Test", 100)
        response = self.client.post("/warehouse/1/add", data={
            "amount": 50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Items added successfully", response.data)
        self.assertIn(b"50", response.data)

    def test_add_items_exceeds_capacity(self):
        warehouse_storage.create("Add Test", 100)
        response = self.client.post("/warehouse/1/add", data={
            "amount": 150
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Not enough space", response.data)

    def test_remove_items_success(self):
        warehouse_storage.create("Remove Test", 100, 50)
        response = self.client.post("/warehouse/1/remove", data={
            "amount": 30
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Items removed successfully", response.data)

    def test_remove_items_exceeds_balance(self):
        warehouse_storage.create("Remove Test", 100, 20)
        response = self.client.post("/warehouse/1/remove", data={
            "amount": 50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Not enough items", response.data)

    def test_delete_warehouse(self):
        warehouse_storage.create("Delete Test", 100)
        response = self.client.post(
            "/warehouse/1/delete",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"deleted successfully", response.data)
        self.assertIn(b"No warehouses yet", response.data)
