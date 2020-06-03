from django.shortcuts import render

# Create your views here.
from conf import serializer, models
from hanfurestful.utils.viewsets import ModelViewSet


class SystemConfigViewSet(ModelViewSet):
    """
    分页设置
    """
    serializer_class = serializer.SystemConfigSerializer
    queryset = models.SystemConfig.objects.filter()
    pagination_class = None


class SystemQuestionViewSet(ModelViewSet):
    """
    刷/考相关设置
    控制前端抓取题库题项数量
    """
    serializer_class = serializer.SystemQuestionSerializer
    queryset = models.SystemQuestion.objects.filter()
    pagination_class = None


class SystemExamControlViewSet(ModelViewSet):
    """
    考试周期控制
    计时任务
    """
    serializer_class = serializer.SystemExamControlSerializer
    queryset = models.SystemExamControl.objects.filter()
    pagination_class = None
