import unittest
from http import HTTPStatus

from flask.testing import FlaskClient

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.Testing = True
        self.client: FlaskClient = app.test_client()

    def test_get_root_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(b"hello world", response.data)
        self.assertEqual(HTTPStatus.OK, response.status_code)
