"""Exercise the browser boundary through the actual FastAPI middleware."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from kadrflow import main

app = main.app


class RequestGuardApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_cross_origin_post_is_rejected_before_router(self):
        response = self.client.post(
            "/api/youtube/disconnect",
            headers={"host": "127.0.0.1:8765", "origin": "https://evil.example"},
        )
        self.assertEqual(response.status_code, 403)

    def test_rebinding_host_is_rejected_on_read(self):
        response = self.client.get(
            "/api/projects", headers={"host": "evil.example:8765"},
        )
        self.assertEqual(response.status_code, 403)

    def test_same_origin_post_reaches_router(self):
        response = self.client.post(
            "/api/no-such-route",
            headers={"host": "127.0.0.1:8765", "origin": "http://127.0.0.1:8765"},
        )
        self.assertEqual(response.status_code, 404)


class FontUploadTests(unittest.IsolatedAsyncioTestCase):
    async def test_font_is_read_with_size_limit(self):
        file = SimpleNamespace(filename="font.ttf", read=AsyncMock(return_value=b"data"))
        with patch.object(main.custom_fonts, "save", return_value={"key": "saved"}):
            self.assertEqual(await main.font_upload(file), {"key": "saved"})
        file.read.assert_awaited_once_with(main.MAX_FONT_BYTES + 1)


if __name__ == "__main__":
    unittest.main()
