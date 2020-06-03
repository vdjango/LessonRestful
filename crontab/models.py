from django.db import models

from crontab.crontab import Crontab


# Create your models here.


class CronTabConfigs(models.Model):
    """
    定时任务
    """
    times = models.CharField(max_length=20, help_text='定时任务crontab的时间设置格式')
    status = models.IntegerField(choices=(
        (0, '考试周期'),
        (1, '测试周期'),
    ), null=True, blank=True)
    run = models.IntegerField(choices=(
        (0, 'crontab.run.CronTabExam.run'),
        (1, 'crontab.run.CronTabTest.run'),
    ), help_text='')
    state = models.IntegerField(choices=(
        (0, '定时添加成功'),
        (1, '定时添加失败'),
    ), default=0)
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改')
    add_time = models.DateTimeField(help_text='添加时间', auto_now_add=True)

    def add_crontab(self, sa=True):
        """
        添加计时任务
        :return:
        """
        try:
            with Crontab(verbosity=0) as crontab:  # initialize a Crontab class with any specified options
                crontab.remove_jobs()  # remove all jobs specified in settings from the crontab
                crontab.add_jobs()  # and add them back
        except:
            self.state = 1
            self.save()

    def delete(self, *args, **kwargs):
        super(CronTabConfigs, self).delete(*args, **kwargs)
        self.add_crontab(sa=False)

    def save(self, *args, **kwargs):
        self.run = self.status
        self.state = 0
        super(CronTabConfigs, self).save(*args, **kwargs)
        self.add_crontab()

    pass
