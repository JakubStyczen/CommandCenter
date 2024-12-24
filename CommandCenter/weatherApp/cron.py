from django_cron import CronJobBase, Schedule
from .models import WeatherConditions
import os
from dotenv import load_dotenv

load_dotenv()


class CleanOldRecordsJob(CronJobBase):
    RUN_EVERY_MINS = int(os.getenv("CRON_SCHEDULE_TIME_MINS"))
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "weatherApp.clean_old_records"

    def do(self):
        MAX_RECORDS = int(os.getenv("MAX_LOGS_STORED"))
        total_records = WeatherConditions.objects.count()
        if total_records > MAX_RECORDS:
            excess_records = total_records - MAX_RECORDS
            WeatherConditions.objects.order_by("created_at")[:excess_records].delete()
