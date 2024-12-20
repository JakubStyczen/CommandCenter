from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from pigeonInterrupts.models import PigeonInterrupt
from datetime import datetime


class PigeonInterruptModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.time = datetime.now()
        cls.pigeon_interrupt = PigeonInterrupt(
            Time=cls.time, PIRSensor=True, CameraSensor=True
        )
        cls.pigeon_interrupt_default = PigeonInterrupt()

    def test_correct_model_creation(self) -> None:
        self.assertEqual(self.time, self.pigeon_interrupt.Time)
        self.assertEqual(True, self.pigeon_interrupt.PIRSensor)
        self.assertEqual(True, self.pigeon_interrupt.CameraSensor)

    def test_defult_model__default_values_creation(self) -> None:
        self.assertEqual(None, self.pigeon_interrupt_default.Time)
        self.assertEqual(False, self.pigeon_interrupt_default.PIRSensor)
        self.assertEqual(False, self.pigeon_interrupt_default.CameraSensor)

    def test_str_conversion(self) -> None:
        str_represetation = f"Data captured at: {self.pigeon_interrupt.Time} with status PIRSensor: {self.pigeon_interrupt.PIRSensor} and CameraSensor: {self.pigeon_interrupt.CameraSensor}"
        self.assertEqual(str(self.pigeon_interrupt), str_represetation)

    def test_date_field_validation_not_raises_exception(self) -> None:
        self.pigeon_interrupt.clean()

    def test_none_date_field_validation_raises_exception(self) -> None:
        with self.assertRaises(ValidationError):
            self.pigeon_interrupt_default.clean()

    # Not available for djondo MongoDB database
    # def test_none_date_field_constraint(self) -> None:
    #     with self.assertRaises(IntegrityError):
    #         self.pigeon_interrupt_default.save()
