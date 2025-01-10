from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from weatherApp.models import WeatherConditions
from django.utils.http import urlencode
from datetime import datetime


class TestWeatherConditionsAppHomePage(SimpleTestCase):

    def test_weather_app_homepage_uses_correct_templates(self) -> None:
        response = self.client.get(reverse("weatherApp:home"))
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/home.html")

    def test_weather_app_homepage_contains_welcome_message(self) -> None:
        response = self.client.get(reverse("weatherApp:home"))
        self.assertContains(
            response, "Welcome to the weather conditions logs", status_code=200
        )


class TestWeatherConditionsAppDeletePage(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls) -> None:
        WeatherConditions.objects.create(temperature=0)

    def test_weather_app_delete_page_uses_correct_templates(self) -> None:
        """Cheking if endpoint uses proper templates"""
        response = self.client.get(
            reverse("weatherApp:weather_conditions_delete", kwargs={"id": 1})
        )
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/weather_conditions_delete.html")

    def test_weather_app_delete_page_contains_delete_message(
        self,
    ) -> None:
        """Checking if endpoint contains proper data"""
        response = self.client.get(
            reverse("weatherApp:weather_conditions_delete", kwargs={"id": 1})
        )
        self.assertContains(
            response, "Are you sure you want to delete this record ?", status_code=200
        )

    def test_weather_app_delete_interrupt_log(self) -> None:
        weather_app_list_reverse = reverse("weatherApp:weather_conditions_list")
        """Deleting one record and checking if there is no record."""
        response = self.client.get(weather_app_list_reverse)
        self.assertEqual(len(response.context["weather_conditions"]), 1)
        response = self.client.post(
            reverse("weatherApp:weather_conditions_delete", kwargs={"id": 1})
        )
        self.assertRedirects(
            response,
            weather_app_list_reverse,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.get(weather_app_list_reverse)
        self.assertEqual(len(response.context["weather_conditions"]), 0)


class TestWeatherConditionsAppListPage(TestCase):
    databases = "__all__"

    def setUp(self) -> None:
        WeatherConditions.objects.create(temperature=55, additional_info="Testing info")
        WeatherConditions.objects.create(
            temperature=-20, additional_info="Also v2 Testing info"
        )
        for _ in range(4):
            WeatherConditions.objects.create(temperature=4)

    def test_weather_app_list_page_uses_correct_templates(self) -> None:
        """Cheking if endpoint uses proper templates"""
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/weather_conditions_list.html")

    def test_weather_app_list_page_contains_delete_and_update_record_message(
        self,
    ) -> None:
        """Checking if endpoint contains proper message"""
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertContains(response, "Delete", status_code=200)
        self.assertContains(response, "Update", status_code=200)

    def test_weather_app_list_page_check_content(self) -> None:
        """Checking if endpoint contains proper data"""
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertContains(response, "Testing info")
        self.assertContains(response, "Also v2 Testing info")
        self.assertNotContains(response, "No logs recorded")

    def test_weather_app_list_page_empty_content(self) -> None:
        """Clear all interrupts and check page's content"""
        WeatherConditions.objects.all().delete()
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertEqual(len(response.context["weather_conditions"]), 0)
        self.assertContains(response, "No logs recorded")

    def test_weather_app_list_default_record_amount(self) -> None:
        """Check the default amount of records displayed. Should display 5 of 6 records (2 created before test and 4 additional)"""
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertEqual(len(response.context["weather_conditions"]), 5)

    def test_weather_app_list_custom_record_amount(self) -> None:
        """Check proper amount fo records display (2 availabe but only 1 on demand). Adding query parameters"""
        query_kwargs = {"quantity": 1}
        response = self.client.get(
            f"{reverse('weatherApp:weather_conditions_list')}?{urlencode(query_kwargs)}"
        )
        self.assertEqual(len(response.context["weather_conditions"]), 1)
        query_kwargs["quantity"] = 6
        response = self.client.get(
            f"{reverse('weatherApp:weather_conditions_list')}?{urlencode(query_kwargs)}"
        )
        self.assertEqual(len(response.context["weather_conditions"]), 6)


class TestWeatherConditionsAppCreatePage(TestCase):
    databases = "__all__"

    def test_weather_app_create_page_uses_correct_templates(self) -> None:
        """Cheking if endpoint uses proper templates"""
        response = self.client.get(reverse("weatherApp:weather_conditions_create"))
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/weather_conditions_create.html")

    def test_weather_app_create_page_contains_save_record_message(
        self,
    ) -> None:
        """Checking if endpoint contains proper message"""
        response = self.client.get(reverse("weatherApp:weather_conditions_create"))
        self.assertContains(response, "Save record", status_code=200)

    def test_weather_app_create_page_correct_submit(
        self,
    ) -> None:
        form = {
            "temperature": "30",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_create"), data=form
        )
        self.assertRedirects(
            response,
            reverse("weatherApp:weather_conditions_list"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertEqual(len(response.context["weather_conditions"]), 1)


class TestWeatherConditionsAppUpdatePage(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls) -> None:
        WeatherConditions.objects.create(temperature=0)

    def test_weather_app_update_page_uses_correct_templates(self) -> None:
        """Cheking if endpoint uses proper templates"""
        response = self.client.get(
            reverse("weatherApp:weather_conditions_update", kwargs={"id": 1})
        )
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/layout.html")
        self.assertTemplateUsed(response, "weatherApp/weather_conditions_create.html")

    def test_weather_app_update_page_contains_save_record_message(
        self,
    ) -> None:
        """Checking if endpoint contains proper message"""
        response = self.client.get(
            reverse("weatherApp:weather_conditions_update", kwargs={"id": 1})
        )
        self.assertContains(response, "Save record", status_code=200)

    def test_weather_app_update_page_correct_submit(
        self,
    ) -> None:
        form = {
            "temperature": "30",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_update", kwargs={"id": 1}), data=form
        )
        self.assertRedirects(
            response,
            reverse("weatherApp:weather_conditions_list"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.get(reverse("weatherApp:weather_conditions_list"))
        self.assertEqual(len(response.context["weather_conditions"]), 1)
        self.assertContains(response, "Test info")
