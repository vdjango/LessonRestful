from django.db import models


# Create your models here.

class SystemConfig(models.Model):
    """
    分页设置
    """
    status = models.IntegerField(choices=(
        (0, '系统设置'),
    ), unique=True)
    paging = models.IntegerField(help_text='前端数据分页', default=20)
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改')
    add_time = models.DateTimeField(help_text='添加时间', auto_now_add=True)
    pass


class SystemQuestion(models.Model):
    """
    刷/考相关设置
    控制前端抓取题库题项数量
    """
    status = models.IntegerField(choices=(
        (0, '选择题'),
        (1, '判断题'),
        (2, '简答题'),
        (3, '机试题'),
    ), help_text='', unique=True)
    amount = models.IntegerField(help_text='题数量', default=10)
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改')
    add_time = models.DateTimeField(help_text='添加时间', auto_now_add=True)

    def save(self, *args, **kwargs):
        super(SystemQuestion, self).save(*args, **kwargs)


class SystemExamControl(models.Model):
    """
    考试周期控制 DELETE
    计时任务
    """
    status = models.IntegerField(choices=(
        (0, '考试周期'),
    ), unique=True)
    exam_time = models.IntegerField(help_text='考试周期控制，单位天。一周7天计算')
    add_time = models.DateTimeField(auto_now_add=True)
    now_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    pass


class SystemExamControlInfo(models.Model):
    """
    计时触发记录 DELETE
    考试周期控制
    计时任务
    """
    exam_time = models.IntegerField(help_text='考试周期控制，单位天。一周7天计算')
    add_time = models.DateTimeField(auto_now_add=True)
    now_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    pass
