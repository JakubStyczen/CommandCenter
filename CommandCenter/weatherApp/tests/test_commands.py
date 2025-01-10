from io import StringIO
from django.test import TestCase, tag
from django.core.management import call_command


@tag("only_local")
class TestTemperatureMeasurementsCommand(TestCase):

    def test_command_usage(self):
        out = StringIO()
        call_command("temperature_measurements", displays=["cmd", "lcd"], stdout=out)
        self.assertIn("Succesfully started measurement!", out.getvalue())
