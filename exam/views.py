from django.shortcuts import render

# Create your views here.
from . import models
from . import serializer
from hanfurestful.utils.viewsets import ModelViewSet


class CronTabMainViewSet(ModelViewSet):
    """
    # 记录班级任务执行情况

    > 定时任务触发后，添加相关班级记录。此次任务完成后，更新[status]状态至已完成
    """
    serializer_class = serializer.CronTabMainSerializer
    queryset = models.CronTabMain.objects.filter()
    filterset_fields = ['status', 'key_school']


class CronTabUserViewSet(ModelViewSet):
    """
    # 记录学员完成任务情况

    > 学生登陆系统 检查班级是否有任务可完成，添加任务记录，学员逐步完成任务 更新[status]状态至已完成
    """
    serializer_class = serializer.CronTabUserSerializer
    queryset = models.CronTabUser.objects.filter()
    filterset_fields = ['status', 'key_user', 'key']
