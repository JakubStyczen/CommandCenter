from django.test import TestCase
from django.urls import reverse
from weatherApp.models import WeatherConditions


class WeatherConditionsFormTest(TestCase):
    databases = "__all__"

    def test_create_weather_conditions_valid_form(self):
        form = {
            "temperature": "30",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_create"), data=form
        )
        self.assertEqual(response.status_code, 302)  # check redirect
        self.assertTrue(WeatherConditions.objects.filter(temperature="30").exists())

    def test_update_weather_conditions_valid_form(self):
        WeatherConditions.objects.create(temperature=0)
        form = {
            "temperature": "30",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_update", kwargs={"id": 1}), data=form
        )
        self.assertEqual(response.status_code, 302)  # check redirect
        self.assertTrue(WeatherConditions.objects.filter(temperature=30).exists())

    def test_not_create_weather_conditions_invalid_form(self):
        # lower band
        form = {
            "temperature": "-55.01",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_create"), data=form
        )
        self.assertEqual(
            response.status_code, 200
        )  # correct resonse with error prompts
        self.assertContains(response, "temperature_gt_-55")

        # upper band
        form = {
            "temperature": "125.01",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_create"), data=form
        )
        self.assertEqual(
            response.status_code, 200
        )  # correct resonse with error prompts
        self.assertContains(response, "temperature_lt_125")
        self.assertFalse(WeatherConditions.objects.filter(temperature=125.01).exists())
        self.assertFalse(WeatherConditions.objects.filter(temperature=-55.01).exists())
        self.assertFalse(WeatherConditions.objects.exists())

    def test_not_create_weather_conditions_invalid_form(self):
        WeatherConditions.objects.create(temperature=0)
        # lower band
        form = {
            "temperature": "-55.01",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_update", kwargs={"id": 1}), data=form
        )
        self.assertEqual(
            response.status_code, 200
        )  # correct resonse with error prompts
        self.assertContains(response, "temperature_gt_-55")

        # upper band
        form = {
            "temperature": "125.01",
            "additional_info": "Test info",
        }
        response = self.client.post(
            reverse("weatherApp:weather_conditions_update", kwargs={"id": 1}), data=form
        )
        self.assertEqual(
            response.status_code, 200
        )  # correct resonse with error prompts
        self.assertContains(response, "temperature_lt_125")
        self.assertFalse(WeatherConditions.objects.filter(temperature=125.01).exists())
        self.assertFalse(WeatherConditions.objects.filter(temperature=-55.01).exists())
        self.assertTrue(WeatherConditions.objects.filter(temperature=0).exists())
