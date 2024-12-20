from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class PigeonInterrupt(models.Model):
    """
    Model contains:
    - time of interrupt captured (or just regular data if there was no interrupt),
    - current sensors status in project: PIRSensor, CameraSensor
    """

    Time = models.DateTimeField()
    PIRSensor = models.BooleanField(default=False)
    CameraSensor = models.BooleanField(default=False)

    # Not available for djondo MongoDB database
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=models.Q(Time__isnull=False),
    #             name="Time_is_not_null"
    #         )
    #     ]

    def __str__(self) -> str:
        return f"Data captured at: {self.Time} with status PIRSensor: {self.PIRSensor} and CameraSensor: {self.CameraSensor}"

    def clean(self):
        if self.Time is None:
            raise ValidationError("Date must be not None")
