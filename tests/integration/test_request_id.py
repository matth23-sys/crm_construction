from django.test import TestCase
from django.urls import reverse


class RequestIDMiddlewareTests(TestCase):
    def test_response_contains_request_id_header(self):
        response = self.client.get(reverse("login"))
        self.assertIn("X-Request-ID", response.headers)
        self.assertTrue(response.headers["X-Request-ID"])