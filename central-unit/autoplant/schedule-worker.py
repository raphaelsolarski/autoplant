import os
import django
import time
from django.conf import settings

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoplant.settings")
    django.setup()
    from centralunit.scheduler import Scheduler
    scheduler = Scheduler()
    while True:
        scheduler.check_and_schedule()
        time.sleep(settings.SCHEDULE_WORKER_TICK_SEC)
