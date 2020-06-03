from django.conf import settings
from django_crontab.crontab import Crontab as DjangoCrontab

from crontab.app_settings import Settings


class Crontab(DjangoCrontab):
    def __init__(self, **options):
        super(Crontab, self).__init__(**options)
        self.settings = Settings(settings)
        print('options', options)
        # options {'verbosity': 1, 'settings': None, 'pythonpath': None, 'traceback': False, 'no_color': False, 'subcommand': 'add', 'jobhash': None}
        # options {'verbosity': 1, 'settings': None, 'pythonpath': None, 'traceback': False, 'no_color': False, 'subcommand': 'add', 'jobhash': None}

    pass
