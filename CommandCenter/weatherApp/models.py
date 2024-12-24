from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from enum import Enum


class TemperatureRange(Enum):
    """
    Choices class maping temperature info to emoji
    """

    FREEZING = "\U0001F976"
    COLD = "\U0001F628"
    COOL = "\U0001F610"
    MILD = "\U0001F642"
    WARM = "\U0001F604"
    HOT = "\U0001F613"
    SCHORCHING = "\U0001F975"


# Create your models here.
class WeatherConditions(models.Model):
    """
    Model contains:
    - time of weather info captured,
    - temperature,
    - additional information.
    """

    condition_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    additional_info = models.CharField(max_length=100, default="")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(time__isnull=False), name="time_is_not_null"
            ),
            models.CheckConstraint(
                check=models.Q(temperature__gt=-55), name="temperature_gt_-55"
            ),
            models.CheckConstraint(
                check=models.Q(temperature__lt=125), name="temperature_lt_125"
            ),
        ]

    def __str__(self) -> str:
        return f"Weather conditions captured at: {self.time}. Temerature: {self.temperature}\N{DEGREE SIGN} {self.temperature_emoji.value}. {self.additional_info}"

    def clean(self) -> None:
        if self.temperature < -55 or self.temperature > 125:
            raise ValidationError("Temperature beyond sensor's range")

    @property
    def temperature_emoji(self) -> TemperatureRange:
        if self.temperature < -10:
            return TemperatureRange.FREEZING
        elif self.temperature < 0:
            return TemperatureRange.COLD
        elif self.temperature < 13:
            return TemperatureRange.COOL
        elif self.temperature < 18:
            return TemperatureRange.MILD
        elif self.temperature < 29:
            return TemperatureRange.WARM
        elif self.temperature < 35:
            return TemperatureRange.HOT
        else:
            return TemperatureRange.SCHORCHING
