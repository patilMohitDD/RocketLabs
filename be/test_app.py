from fastapi.testclient import TestClient
from main import app 
import unittest

class TestRocketEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    # At this point of time we should have valid objects in the Database
    def test_get_rocket_details_rocket_present(self):
        rocket_id = 1  # Adjust the ID as needed
        response = self.client.get(f"/rocket/{rocket_id}")

        self.assertEqual(response.status_code, 200)

    def test_get_rocket_details_specific_key(self):
        rocket_id = 1  # Adjust the ID as needed
        response = self.client.get(f"/rocket/{rocket_id}")

        self.assertIn("Stage1", response.json())
        self.assertIn("Height", response.json())
    
    def test_get_rocket_not_present(self):
        rocket_id = 10  # Adjust the ID as needed
        response = self.client.get(f"/rocket/{rocket_id}")

        self.assertEqual(response.status_code, 404)
    
    def test_get_rocket_children_present(self):
        rocket_id = 1  # Adjust the ID as needed

        path = "Stage1"
        response = self.client.get(f"/rocket/{rocket_id}/{path}") # Height should be there in db(case sensitive)
        self.assertEqual(response.status_code, 200)
    
    def test_get_rocket_children_present_multilevel(self):
        rocket_id = 1  # Adjust the ID as needed

        path = "Stage1/Engine1/ISP"
        response = self.client.get(f"/rocket/{rocket_id}/{path}") # Height should be there in db(case sensitive)
        self.assertEqual(response.status_code, 200)
    
    def test_get_rocket_children_not_present(self):
        rocket_id = 1  # Adjust the ID as needed

        path = "Stage1/Engine100/ISP"
        response = self.client.get(f"/rocket/{rocket_id}/{path}") 
        self.assertEqual(response.status_code, 404)
    

    
    

