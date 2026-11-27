import json
from unittest.mock import patch
from urllib.error import URLError

from django.test import Client, SimpleTestCase, override_settings
from django.urls import reverse


class PortfolioTests(SimpleTestCase):
    def test_homepage_and_contact_page_render(self):
        self.assertContains(self.client.get(reverse("index")), "Software | Engineer")
        self.assertContains(self.client.get(reverse("contact")), "data-open-contact")

    def test_brochure_is_a_pdf_attachment(self):
        response = self.client.get(reverse("download_brochure"))
        self.addCleanup(response.close)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertTrue(next(response.streaming_content).startswith(b"%PDF-"))


@override_settings(
    RESEND_API_KEY="test-only",
    CONTACT_FROM_EMAIL="sender@example.test",
    CONTACT_TO_EMAIL="owner@example.test",
)
class ContactTests(SimpleTestCase):
    data = {
        "name": "Visitor",
        "email": "visitor@example.test",
        "subject": "Hello",
        "message": "A message for the portfolio owner.",
    }

    @patch("home.views.urlopen")
    def test_valid_form_sends_only_to_the_owner_and_redirects(self, send):
        response = self.client.post(reverse("contact"), self.data)
        self.assertRedirects(response, reverse("success"))
        request = send.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload["to"], ["owner@example.test"])
        self.assertEqual(payload["reply_to"], self.data["email"])
        self.assertIn(self.data["message"], payload["text"])
        self.assertEqual(send.call_args.kwargs["timeout"], 5)

    @patch("home.views.urlopen")
    def test_invalid_form_keeps_input_without_sending(self, send):
        data = {**self.data, "email": "invalid"}
        response = self.client.post(reverse("contact"), data)
        self.assertContains(response, "Enter a valid email address.", status_code=400)
        self.assertContains(response, self.data["message"], status_code=400)
        send.assert_not_called()

    @patch("home.views.urlopen", side_effect=URLError("unavailable"))
    def test_delivery_failure_returns_a_friendly_error(self, send):
        with self.assertLogs("home.views", level="WARNING"):
            response = self.client.post(reverse("contact"), self.data)
        self.assertContains(response, "Please try again later.", status_code=503)
        send.assert_called_once()

    @override_settings(RESEND_API_KEY="")
    @patch("home.views.urlopen")
    def test_missing_configuration_returns_unavailable(self, send):
        response = self.client.post(reverse("contact"), self.data)
        self.assertEqual(response.status_code, 503)
        send.assert_not_called()

    @patch("home.views.urlopen")
    def test_contact_requires_csrf(self, send):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse("contact"), self.data).status_code, 403)
        send.assert_not_called()
