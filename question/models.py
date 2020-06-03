import os
import time
from django.utils import timezone
from django.db import models

# Create your models here.
from account.models import User, SchoolInfo, Educational, UserSchoolInfoMany


class ModelBase(models.Model):
    """
    排序
    """

    class Meta:
        abstract = True
        ordering = ['-id']

    pass


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

一般一个学期N本书名分类，一个学生对因N本书籍。测试或考试 只针对当前N本书籍内容进行
"""


class ClassQuestion(ModelBase):
    """
    书名分类
    """

    def get_upload_to(self, filename):
        now = timezone.now()
        if not timezone.is_naive(now):
            now = timezone.make_naive(now, timezone.utc)

        filename = '{}.{}'.format(
            str(now).split('.')[0],
            filename.split('.')[-1]
        )
        _path = os.path.join(
            'class-question',
            str(time.mktime(now.timetuple())).split('.')[0],
            filename
        )
        return _path

    name = models.CharField(max_length=150, help_text='书名分类名称')
    image = models.ImageField(upload_to=get_upload_to, help_text='封面图', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)
    count = models.IntegerField(help_text='统计当前学员已有学习人数', default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    pass


class ClassQuesModel(ModelBase):
    """
    模块分类
    """
    name = models.CharField(max_length=150, help_text='模块分类名称')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)
    key_class_question = models.ForeignKey(
        ClassQuestion, on_delete=models.CASCADE,
        help_text='书名分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='书名分类'
    )

    def __str__(self):
        return '{} | {}'.format(
            self.key_class_question.name,
            self.name
        )

    class Meta:
        ordering = ['-id']

    pass


class ClassQuesChapter(ModelBase):
    """
    章节分类
    """
    name = models.CharField(max_length=150, help_text='章节分类名称')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)
    key_class_question = models.ForeignKey(
        ClassQuestion, on_delete=models.CASCADE,
        help_text='书名分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='书名分类', null=True, blank=True
    )
    key_class_ques_model = models.ForeignKey(
        ClassQuesModel, on_delete=models.CASCADE,
        help_text='模块分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='模块分类'
    )

    def save(self, *args, **kwargs):
        self.key_class_question = self.key_class_ques_model.key_class_question
        super(ClassQuesChapter, self).save(*args, **kwargs)

    def __str__(self):
        return '{} | {} | {}'.format(
            self.key_class_ques_model.key_class_question.name,
            self.key_class_ques_model.name,
            self.name
        )

    class Meta:
        ordering = ['-id']


"""
End： 分类
"""

"""
Start： 题型分类
    选择题|判断题|简答题|机试题
        答案
"""


class Question(models.Model):
    """
    [选择题|判断题|简答题|机试题]: 题库
    """

    def get_upload_to(self, filename):
        now = timezone.now()
        if not timezone.is_naive(now):
            now = timezone.make_naive(now, timezone.utc)

        filename = '{}.{}'.format(
            str(now).split('.')[0],
            filename.split('.')[-1]
        )
        _path = os.path.join(
            'question-image',
            str(time.mktime(now.timetuple())).split('.')[0],
            filename
        )
        return _path

    name = models.CharField(max_length=150, help_text='题型名称', null=True, blank=True)
    text = models.TextField(help_text='题目描述')
    state = models.IntegerField(choices=(
        (0, '选择题'),
        (1, '判断题'),
        (2, '简答题'),
        (3, '机试题')
    ), default=0, help_text='类型')
    image = models.ImageField(upload_to=get_upload_to, help_text='题型说明图', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)

    key_class_question = models.ForeignKey(
        ClassQuestion, on_delete=models.CASCADE,
        help_text='书名分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='书名分类'
    )
    key_class_ques_model = models.ForeignKey(
        ClassQuesModel, on_delete=models.CASCADE,
        help_text='模块分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='模块分类'
    )
    key_class_ques_chapter = models.ForeignKey(
        ClassQuesChapter, on_delete=models.CASCADE,
        help_text='章节分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='章节分类'
    )

    def __str__(self):
        return '{} | {} | {} | {}'.format(
            self.key_class_question.name,
            self.key_class_ques_model.name,
            self.key_class_ques_chapter.name,
            self.text
        )

    class Meta:
        ordering = ['-id']


class QuestionAnswer(models.Model):
    """
    [选择题|判断题|简答题|机试题]: 答案
    """
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='得分', help_text='得分')
    solu = models.BooleanField(verbose_name='正确答案', help_text='是否是正确答案', default=False)
    choice_gid = models.IntegerField(choices=(
        (0, 'A'), (1, 'B'), (2, 'C'),
        (3, 'D'), (4, 'E'), (5, 'F'),
        (6, 'G'),
    ), help_text='选择题标号', verbose_name='标号', null=True, blank=True)
    choice = models.TextField(help_text='选择题答案', verbose_name='选择题', null=True, blank=True)
    judge = models.IntegerField(choices=(
        (0, '对'),
        (1, '错'),
        (2, '全对'),
        (3, '全错'),
    ), help_text='判断题答案', verbose_name='判断题', null=True, blank=True)
    answer = models.TextField(help_text='简答题答案', verbose_name='简答题', null=True, blank=True)
    machine = models.TextField(help_text='机试题答案', verbose_name='机试题', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)

    key_question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        help_text='答案 [选择题|判断题|简答题|机试题]',
        verbose_name='答案'
    )

    class Meta:
        ordering = ['choice_gid', '-id']

    pass


"""
End： 题型分类 
"""

"""
Start: 考试效果
"""


class UserTimeRecord(models.Model):
    """
    记录用户[练习/考试]最后一次时间 暂时没有派上用场
    """
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='记录用户[练习/考试]最后一次时间')
    key_class_question = models.ForeignKey(
        ClassQuestion, on_delete=models.CASCADE,
        help_text='书名分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='书名分类', null=True, blank=True
    )
    key_class_ques_model = models.ForeignKey(
        ClassQuesModel, on_delete=models.CASCADE,
        help_text='模块分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='模块分类', null=True, blank=True
    )
    key_class_ques_chapter = models.ForeignKey(
        ClassQuesChapter, on_delete=models.CASCADE,
        help_text='章节分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='章节分类'
    )

    def save(self, *args, **kwargs):
        self.key_class_question = self.key_class_ques_chapter.key_class_ques_model.key_class_question
        self.key_class_ques_model = self.key_class_ques_chapter.key_class_ques_model
        super(UserTimeRecord, self).save(*args, **kwargs)


"""
End: 考试效果
"""


class UserSemester(models.Model):
    """
    授课进度
    管理 在授班级 所教授的课程进度
    正在学习的课程
    """

    def get_upload_to(self, filename):
        now = timezone.now()
        if not timezone.is_naive(now):
            now = timezone.make_naive(now, timezone.utc)

        filename = '{}.{}'.format(
            str(now).split('.')[0],
            filename.split('.')[-1]
        )
        _path = os.path.join(
            'class-question',
            str(time.mktime(now.timetuple())).split('.')[0],
            filename
        )
        return _path

    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='开始学习时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次学习')
    end_time = models.DateTimeField(help_text='学习结束时间', null=True, blank=True)
    key_class_question = models.ForeignKey(
        ClassQuestion, on_delete=models.CASCADE,
        help_text='书名分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='书名分类'
    )
    key_user_school_info_many = models.ForeignKey(
        UserSchoolInfoMany, on_delete=models.CASCADE,
        help_text='学生所对应的班级以及教师所教授的班级',
        verbose_name='学生所在班级/教师在授班级'
    )

    def save(self, *args, **kwargs):
        if kwargs.get('force_insert', None):
            # 统计当前学员已有学习人数
            self.key_class_question.count += 1
            self.key_class_question.save()

        super(UserSemester, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 统计当前学员已有学习人数
        self.key_class_question.count -= 1
        self.key_class_question.save()
        return super(UserSemester, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class ExamStock(models.Model):
    """
    章节进度
    管理 授课进度 所教授的章节进度
    当前班级正在学习的章节
    记录当前班级学习进度-通过教师中心管理当前所属班级学习进度
    根据学习进度来把控 抓取的考题所属范围
    后期可以通过指定 抓取的考题所属范围: [书名分类-模块分类-章节分类]
    """
    key_class_question = models.ForeignKey(
        ClassQuestion, on_delete=models.SET_NULL,
        help_text='书名分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]',
        verbose_name='书名分类', null=True, blank=True
    )
    key_class_ques_chapter = models.ForeignKey(
        ClassQuesChapter, verbose_name='章节分类', on_delete=models.SET_NULL, null=True, blank=True,
        help_text='章节分类 [书名分类-模块分类-章节分类:选择题|判断题|简答题|机试题]'
    )
    status = models.IntegerField(choices=(
        (0, '开启'),
        (1, '关闭'),
    ), help_text='把控 是否抓取的当前章节考题', default=0)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='开始学习时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次学习')

    key = models.ForeignKey(UserSemester, on_delete=models.CASCADE, help_text='学生所对应的班级以及教师所教授的班级')

    def save(self, *args, **kwargs):
        self.key_class_question = self.key_class_ques_chapter.key_class_question
        super(ExamStock, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    pass
