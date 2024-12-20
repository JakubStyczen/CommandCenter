from django.test import SimpleTestCase, TestCase, tag
from django.urls import reverse
from pigeonInterrupts.models import PigeonInterrupt
from django.utils.http import urlencode


class TestPigeonInterruptsAppHomePage(SimpleTestCase):

    def test_pigeon_interrupts_homepage_uses_correct_templates(self) -> None:
        response = self.client.get(reverse("pigeonInterrupts:home"))
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "pigeonInterrupts/layout.html")
        self.assertTemplateUsed(response, "pigeonInterrupts/home.html")

    def test_pigeon_interrupts_homepage_contains_welcome_message(self) -> None:
        response = self.client.get(reverse("pigeonInterrupts:home"))
        self.assertContains(
            response, "Welcome to the pigeon interrupts logs", status_code=200
        )


class TestPigeonInterruptsAppDeletePage(TestCase):
    """
    Numerate test cases to differ them sequence to help choose proper id of record in test case.
    Each test case has cls.pigeon_interrupt but with different id property, incremented.

    Also "databases = '__all__'" must be set to preapare db's for tests
    """

    databases = "__all__"

    @classmethod
    def setUpTestData(cls) -> None:
        PigeonInterrupt.objects.create()

    def test_case_1_pigeon_interrupts_delete_page_uses_correct_templates(self) -> None:
        """Cheking if endpoint uses proper templates"""
        response = self.client.get(
            reverse("pigeonInterrupts:pigeon_interrupt_delete", kwargs={"id": 1})
        )
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "pigeonInterrupts/layout.html")
        self.assertTemplateUsed(
            response, "pigeonInterrupts/pigeon_interrupt_delete.html"
        )

    def test_case_2_pigeon_interrupts_delete_page_contains_welcome_message(
        self,
    ) -> None:
        """Checking if endpoint contains proper data"""
        response = self.client.get(
            reverse("pigeonInterrupts:pigeon_interrupt_delete", kwargs={"id": 2})
        )
        self.assertContains(
            response, "Are you sure you want to delete this product ?", status_code=200
        )

    def test_case_3_pigeon_interrupts_delete_interrupt_log(self) -> None:
        """Deleting one record and checking if there is no record"""
        response = self.client.get(reverse("pigeonInterrupts:pigeon_interrupt_list"))
        self.assertEqual(len(response.context["pigeons_interrupts"]), 1)
        self.client.post(
            reverse("pigeonInterrupts:pigeon_interrupt_delete", kwargs={"id": 3})
        )
        response = self.client.get(reverse("pigeonInterrupts:pigeon_interrupt_list"))
        self.assertEqual(len(response.context["pigeons_interrupts"]), 0)


class TestPigeonInterruptsAppListPage(TestCase):
    databases = "__all__"

    def setUp(self) -> None:
        PigeonInterrupt.objects.create(CameraSensor=False)
        PigeonInterrupt.objects.create(CameraSensor=True)
        PigeonInterrupt.objects.create(CameraSensor=False)
        PigeonInterrupt.objects.create(CameraSensor=True)
        PigeonInterrupt.objects.create(CameraSensor=False)
        PigeonInterrupt.objects.create(CameraSensor=True)

    def test_pigeon_interrupts_list_page_uses_correct_templates(self) -> None:
        """Cheking if endpoint uses proper templates"""
        response = self.client.get(reverse("pigeonInterrupts:pigeon_interrupt_list"))
        self.assertTemplateUsed(response, "mainApp/layout.html")
        self.assertTemplateUsed(response, "pigeonInterrupts/layout.html")
        self.assertTemplateUsed(response, "pigeonInterrupts/pigeon_interrupt_list.html")

    def test_pigeon_interrupts_list_page_contains_delete_interrupt_message(
        self,
    ) -> None:
        """Checking if endpoint contains proper message"""
        response = self.client.get(reverse("pigeonInterrupts:pigeon_interrupt_list"))
        self.assertContains(response, "Delete", status_code=200)

    def test_pigeon_interrupts_list_page_check_content(self) -> None:
        """Checking if endpoint contains proper data"""
        response = self.client.get(
            f"{reverse('pigeonInterrupts:pigeon_interrupt_list')}?"
        )
        self.assertContains(response, "True")
        self.assertContains(response, "False")
        self.assertNotContains(response, "No logs recorded")

    def test_pigeon_interrupts_list_page_empty_content(self) -> None:
        """Clear all interrupts and check page's content"""
        PigeonInterrupt.objects.all().delete()
        response = self.client.get(reverse("pigeonInterrupts:pigeon_interrupt_list"))
        self.assertEqual(len(response.context["pigeons_interrupts"]), 0)
        self.assertContains(response, "No logs recorded")

    def test_pigeon_interrupts_list_default_interrupt_amount(self) -> None:
        """Check the default amount of records displayed. Should display 5 of 6 records (2 created before test and 4 additional)"""
        response = self.client.get(reverse("pigeonInterrupts:pigeon_interrupt_list"))
        self.assertEqual(len(response.context["pigeons_interrupts"]), 5)

    def test_pigeon_interrupts_list_default_interrupt_amount(self) -> None:
        """Check proper amount fo records display (2 availabe but only 1 on demand). Adding query parameters"""
        query_kwargs = {"quantity": 1}
        response = self.client.get(
            f"{reverse('pigeonInterrupts:pigeon_interrupt_list')}?{urlencode(query_kwargs)}"
        )
        self.assertEqual(len(response.context["pigeons_interrupts"]), 1)
        query_kwargs["quantity"] = 6
        response = self.client.get(
            f"{reverse('pigeonInterrupts:pigeon_interrupt_list')}?{urlencode(query_kwargs)}"
        )
        self.assertEqual(len(response.context["pigeons_interrupts"]), 6)

    # @tag('correct')
    # def test_pigeon_interrupts_list_without_quantity_param(self) -> None:
    #     """Check proper amount fo records display (2 availabe but and 2 on demand). Adding query parameters"""
    #     query_kwargs = {'quantity': ''}
    #     response = self.client.get(f"{reverse('pigeonInterrupts:pigeon_interrupt_list')}?{urlencode(query_kwargs)}")
    #     self.assertEqual(len(response.context['pigeons_interrupts']), 2)
