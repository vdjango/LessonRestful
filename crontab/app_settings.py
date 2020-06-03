from django_crontab.app_settings import Settings as DjangoSettings
from . import models


class Settings(DjangoSettings):
    def __init__(self, settings):
        super(Settings, self).__init__(settings)
        cron = models.CronTabConfigs.objects.filter()
        getattr_settings = [(i.times, i.get_run_display()) for i in cron]

        print('getattr_settings', getattr_settings)
        for i in self.CRONJOBS:
            getattr_settings.append(i)

        self.CRONJOBS = getattr_settings

    pass
