from django.test import SimpleTestCase
from django.urls import reverse


class TestMainAppHomePage(SimpleTestCase):

    def test_homepage_uses_correct_templates(self) -> None:
        response = self.client.get(reverse("mainApp:home"))
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "mainApp/home.html")

    def test_homepage_contains_welcome_message(self) -> None:
        response = self.client.get(reverse("mainApp:home"))
        self.assertContains(response, "Welcome to the Command Center", status_code=200)
