import os
from http import HTTPStatus
from unittest import TestCase, mock

from flask.testing import FlaskClient

from app import app


class AppTests(TestCase):
    def setUp(self):
        app.Testing = True
        self.client: FlaskClient = app.test_client()

    def test_get_root_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(b"hello world", response.data)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(HTTPStatus.OK, response.status_code)

    @mock.patch.dict(
        os.environ,
        {
            "VERSION": "fake_version",
            "LAST_COMMIT_SHA": "fake_sha",
        },
    )
    def test_get_metadata_endpoint(self):
        response = self.client.get("/metadata")
        json_data = response.get_json()

        self.assertEqual("fake_version", json_data["version"])
        self.assertIn("description", json_data)
        self.assertEqual("fake_sha", json_data["lastcommitsha"])
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @mock.patch.dict(
        os.environ,
        {
            "LAST_COMMIT_SHA": "fake_sha",
        },
    )
    def test_get_metadata_endpoint_when_version_not_set(self):
        response = self.client.get("/metadata")
        json_data = response.get_json()

        self.assertEqual("version not found", json_data["version"])

    @mock.patch.dict(
        os.environ,
        {
            "VERSION": "fake_version",
        },
    )
    def test_get_metadata_endpoint_when_last_commit_sha_not_set(self):
        response = self.client.get("/metadata")
        json_data = response.get_json()

        self.assertEqual("last commit sha not found", json_data["lastcommitsha"])
