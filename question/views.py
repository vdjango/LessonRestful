import django_filters
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from hanfurestful.utils.LimitOffsetPagination import Pagination
from hanfurestful.utils.viewsets import ModelViewSet
from question import serializer, models

"""
Start： 分类

计算机与网络（书名分类） -
    第一模块： 硬件 （模块分类） -
        第一章： 综合布线 （章节分类） -
            选择题(ABCD)|判断题(AB)|简答题(T)|机试题(T)
                答案

        第二章： 服务器 -
            选择题(ABCD)|判断题(AB)|简答题(T)|机试题(T)
                答案

    第二模块： 软件 -
        第一章： Word的操作使用 -
            选择题(ABCD)|判断题(AB)|简答题(T)|机试题(T)
                答案

        第二章： Excel的操作使用 -
            选择题(ABCD)|判断题(AB)|简答题(T)|机试题(T)
                答案
"""


class ClassQuestionViewSet(ModelViewSet):
    """书名分类"""
    pagination_class = Pagination
    serializer_class = serializer.ClassQuestionSerializer
    queryset = models.ClassQuestion.objects.filter()
    filterset_fields = ['id', 'name']
    pass


class ClassQuesModelViewSet(ModelViewSet):
    """模块分类"""
    pagination_class = Pagination
    serializer_class = serializer.ClassQuesModelSerializer
    queryset = models.ClassQuesModel.objects.filter()
    filterset_fields = ['id', 'name', 'key_class_question']
    pass


class ClassQuesChapterViewSet(ModelViewSet):
    """章节分类"""

    class ClassQuesChapterFilter(django_filters.FilterSet):
        class Meta:
            model = models.ClassQuesChapter
            fields = {
                "name": ['exact', 'icontains'],
                "key_class_ques_model": ['exact', ],
                "key_class_question": ['exact', ],
            }

    pagination_class = Pagination
    serializer_class = serializer.ClassQuesChapterSerializer
    queryset = models.ClassQuesChapter.objects.filter()
    # filterset_fields = ['id', 'name', 'key_class_question', 'key_class_ques_model']
    filter_class = ClassQuesChapterFilter
    pass


"""
End： 分类
"""

"""
Start： 题型分类
    选择题|判断题|简答题|机试题
        答案
"""


class QuestionAnswerViewSet(ModelViewSet):
    """[选择题|判断题|简答题|机试题]: 答案"""
    pagination_class = Pagination
    serializer_class = serializer.QuestionAnswerSerializer
    queryset = models.QuestionAnswer.objects.filter()
    filterset_fields = ['id', 'score', 'solu', 'choice_gid', 'key_question']
    pass


class QuestionViewSet(ModelViewSet):
    """[选择题|判断题|简答题|机试题]: 题库"""
    pagination_class = Pagination
    serializer_class = serializer.QuestionSerializer
    queryset = models.Question.objects.filter()
    # filterset_fields = ['name', 'text', 'verify', 'browse', 'user']
    pass


"""
End： 题型分类
"""


class UserSemesterViewSet(ModelViewSet):
    """
    授课进度
    管理 在授班级 所教授的课程进度
    正在学习的课程
    """
    pagination_class = Pagination
    serializer_class = serializer.UserSemesterSerializer
    serializer_list_class = serializer.UserSemesterListSerializer
    queryset = models.UserSemester.objects.filter()
    filterset_fields = ['key_class_question', 'key_user_school_info_many']
    pass


"""
Start： 刷题，考题
    选择题|判断题|简答题|机试题
        答案
"""


class ExamQuestionsVIewSet(ModelViewSet):
    """
    刷题 随机抓取题目
    """
    serializer_class = serializer.ExamQuestionSerializer
    queryset = models.Question.objects.filter().order_by('?')
    filterset_fields = ['state', 'key_class_question', 'key_class_ques_model', 'key_class_ques_chapter']

    # def list(self, request, *args, **kwargs):
    #     key_class_ques_chapter = self.request.query_params.get('key_class_ques_chapter', None)
    #
    #     queryset = self.queryset.filter(key_class_ques_chapter=key_class_ques_chapter)
    #
    #     multiple = None
    #
    #     serializers = self.get_serializer_list(queryset, many=True)
    #     return Response(serializers.data)


class ExamStockViewSet(ModelViewSet):
    """
    章节进度
    管理 授课进度 所教授的章节进度
    当前班级正在学习的章节
    记录当前班级学习进度-通过教师中心管理当前所属班级学习进度
    根据学习进度来把控 抓取的考题所属范围
    后期可以通过指定 抓取的考题所属范围: [书名分类-模块分类-章节分类]
    """
    queryset = models.ExamStock.objects.filter()
    serializer_class = serializer.ExamStockSerializer
    filterset_fields = ['key_class_question', 'key_class_ques_chapter', 'key', 'status']
