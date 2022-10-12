import unittest
from fastapi.testclient import TestClient
from prediction_api.app import app


client = TestClient(app)


class Root(unittest.TestCase):
    def test_get(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { "message": "Hello World" })

class Upload(unittest.TestCase):
    def test_upload_file(self):
        with open("./tests/test_files/text.txt", "rb") as f:
            files = { "file_upload": f}
            response = client.post("/upload", files=files)
            # self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), "35")

