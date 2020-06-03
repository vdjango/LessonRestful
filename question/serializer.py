from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from . import models

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


class ClassQuestionSerializer(serializers.ModelSerializer):
    """书名分类"""

    class Meta:
        model = models.ClassQuestion
        fields = '__all__'


class ClassQuesModelSerializer(serializers.ModelSerializer):
    """模块分类"""

    class_question = ClassQuestionSerializer(source='key_class_question', required=False, read_only=True)

    class Meta:
        model = models.ClassQuesModel
        fields = '__all__'


class ClassQuesChapterSerializer(serializers.ModelSerializer):
    """章节分类"""

    class_ques_model = ClassQuesModelSerializer(source='key_class_ques_model', required=False, read_only=True)

    class Meta:
        model = models.ClassQuesChapter
        fields = '__all__'


"""
End： 分类
"""

"""
Start： 题型分类
    选择题|判断题|简答题|机试题
        答案
"""


class QuestionAnswerTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """[选择题|判断题|简答题|机试题]: 答案"""
    question = QuestionAnswerTestSerializer(source='key_question', required=False, read_only=True,
                                            help_text='题库')

    class Meta:
        model = models.QuestionAnswer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """[选择题|判断题|简答题|机试题]: 题库"""

    class_question = ClassQuestionSerializer(
        source='key_class_question',
        required=False, read_only=True,
        help_text='书名分类'
    )
    class_ques_model = ClassQuesModelSerializer(
        source='key_class_ques_model',
        required=False,
        read_only=True,
        help_text='模块分类'
    )
    class_ques_chapter = ClassQuesChapterSerializer(
        source='key_class_ques_chapter',
        required=False,
        read_only=True,
        help_text='章节分类'
    )

    class Meta:
        model = models.Question
        fields = '__all__'


"""
End： 题型分类 
"""


class UserSemesterListSerializer(serializers.ModelSerializer):
    """
    授课进度-（当前班级）
    当前班级正在学习的课程
    在授班级 所教授的课程进度 [书名-模块-章节]
    """
    class_question = ClassQuestionSerializer(source='key_class_question', required=False, read_only=True)

    class Meta:
        model = models.UserSemester
        fields = '__all__'


"""
Start： 刷题，考题
    选择题|判断题|简答题|机试题
        答案
"""


class ExamQuestionSerializer(serializers.ModelSerializer):
    """
    刷题题库
    """

    class QuestionAnswer(serializers.ModelSerializer):
        class Meta:
            model = models.QuestionAnswer
            fields = '__all__'

    questions = QuestionAnswer(source='questionanswer_set', many=True)

    class Meta:
        model = models.Question
        fields = '__all__'

    pass


class UserSemesterSerializer(UserSemesterListSerializer):
    """
    授课进度
    管理 在授班级 所教授的课程进度
    正在学习的课程
    """

    def create(self, validated_data):
        if self.Meta.model.objects.filter(
                key_class_question=validated_data['key_class_question'],
                key_user_school_info_many=validated_data['key_user_school_info_many'],
        ).first():
            raise serializers.ValidationError({
                "detail": "已经添加过啦！"
            })

        return super(UserSemesterSerializer, self).create(validated_data)

    pass


class ExamStockSerializer(serializers.ModelSerializer):
    """
    章节进度
    管理 授课进度 所教授的章节进度
    当前班级正在学习的章节
    记录当前班级学习进度-通过教师中心管理当前所属班级学习进度
    根据学习进度来把控 抓取的考题所属范围
    后期可以通过指定 抓取的考题所属范围: [书名分类-模块分类-章节分类]
    """
    class_ques_chapter = ClassQuesChapterSerializer(
        source='key_class_ques_chapter',
        required=False,
        read_only=True,
        help_text='章节分类'
    )

    def create(self, validated_data):
        if self.Meta.model.objects.filter(
                key_class_ques_chapter=validated_data['key_class_ques_chapter'],
                key=validated_data['key'],
        ).first():
            raise serializers.ValidationError({
                "detail": "已经添加过啦！"
            })

        return super(ExamStockSerializer, self).create(validated_data)

    class Meta:
        model = models.ExamStock
        fields = '__all__'

    pass
