from django.shortcuts import render

# Create your views here.
from crontab import models, serializer
from hanfurestful.utils.viewsets import ModelViewSet


def a():
    print('----------')
    pass


class CronTabConfigsViewSet(ModelViewSet):
    """
    定时任务
    """
    serializer_class = serializer.CronTabConfigsSerializer
    queryset = models.CronTabConfigs.objects.filter()
    filterset_fields = ['status',]
    pagination_class = None
    pass

# linux crontab log /var/spool/mail/[User]
# mac os crontab log /var/mail/[User]
