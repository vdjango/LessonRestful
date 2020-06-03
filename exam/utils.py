from django.utils.datetime_safe import datetime

from exam.models import CronTabMain


class SetCronTabMainStatus(object):
    """
    执行 班级考试时间到期 自动更新状态
    """

    def __init__(self):
        self.model = CronTabMain
        self.time = datetime.utcnow().now()
        self.filters = {
            # 查询参数
            'status': 1,
            'time__lt': self.time
        }
        self.orm_set = {
            # 更新参数
            'status': 0
        }

    def __call__(self, *args, **kwargs):
        cron = self.update()
        pass

    def update(self):
        return self.model.objects.filter(**self.filters).update(**self.orm_set)
