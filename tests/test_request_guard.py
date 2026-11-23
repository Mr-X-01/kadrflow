"""Local API browser boundary regression tests."""
import os
import unittest
from unittest import mock

from kadrflow.request_guard import trusted_request


class RequestGuardTests(unittest.TestCase):
    def test_local_ui_and_non_browser_client(self):
        self.assertTrue(trusted_request("127.0.0.1:8765", "http://127.0.0.1:8765", "POST"))
        self.assertTrue(trusted_request("localhost:8765", None, "POST"))

    def test_foreign_page_cannot_submit_form(self):
        self.assertFalse(trusted_request("127.0.0.1:8765", "https://evil.example", "POST"))
        self.assertFalse(trusted_request("127.0.0.1:8765", "https://127.0.0.1:8765", "POST"))
        self.assertFalse(trusted_request("127.0.0.1:8765", "null", "POST"))
        self.assertFalse(trusted_request("127.0.0.1:8765", None, "POST", "cross-site"))

    def test_rebinding_hostname_is_rejected(self):
        self.assertFalse(trusted_request("evil.example:8765", "http://evil.example:8765", "POST"))
        self.assertFalse(trusted_request("evil.example:8765", None, "GET"))

    def test_host_aliases_and_ports(self):
        self.assertFalse(trusted_request("localhost:8765", "http://localhost:9000", "POST"))
        self.assertFalse(trusted_request("user@localhost:8765", None, "GET"))
        self.assertFalse(trusted_request("localhost:bad", None, "GET"))
        self.assertTrue(trusted_request("[::1]:8765", "http://[::1]:8765", "POST"))

    def test_explicit_lan_bind(self):
        with mock.patch.dict(os.environ, {"KADRFLOW_BIND_HOST": "0.0.0.0"}):
            self.assertTrue(trusted_request("192.168.1.5:8765", "http://192.168.1.5:8765", "POST"))
            self.assertFalse(trusted_request("evil.example:8765", None, "GET"))


if __name__ == "__main__":
    unittest.main()
