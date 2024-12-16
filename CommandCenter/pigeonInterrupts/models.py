from django.db import models

# Create your models here.
class PigeonInterrupt(models.Model):
    """
    Model contains:
    - time of interrupt captured (or just regular data if there was no interrupt),
    - current sensors status in project: PIRSensor, CameraSensor
    """
    Time = models.DateTimeField()
    PIRSensor = models.BooleanField(default = False)
    CameraSensor = models.BooleanField(default = False)
    
    def __str__(self):
        return f"Data captured at: {self.Time} with status PIRSensor: {self.PIRSensor} and CameraSensor: {self.CameraSensor}"