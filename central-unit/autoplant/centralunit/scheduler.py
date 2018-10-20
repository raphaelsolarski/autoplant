import os
import sys
import django

class Scheduler:
    def schedule(self):
        pass

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('..'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoplant.settings")
    django.setup()
    Scheduler().schedule()
