from django.db import models

# Create your models here.
from account.models import User, SchoolInfo

"""
Start 记录班级考试任务进度相关信息
"""


class CronTabMain(models.Model):
    """
    记录班级任务执行情况
    定时任务触发后，添加相关班级记录。此次任务完成后，更新[status]状态至已完成
    """
    status = models.IntegerField(choices=(
        (0, '已结束'),
        (1, '进行中'),
    ), default=1, help_text='当开始执行任务时 进行中，任务已完结时 已完成')
    message = models.TextField(help_text='用于通知学生 当前任务的说明 例如：本期考试开始了，赶快来考试吧')
    number = models.IntegerField(default=0, help_text='当前完成任务人数', verbose_name='计数器')
    key_school = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, help_text='所关联的班级')
    time = models.DateTimeField(null=True, blank=True, help_text='考试结束时间，时间一过，结束考试')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(CronTabMain, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    pass


class CronTabUser(models.Model):
    """
    记录学员完成任务情况
    学生登陆系统 检查班级是否有任务可完成，添加任务记录，学员逐步完成任务 更新[status]状态至已完成
    """
    status = models.IntegerField(choices=(
        (-1, '未完成'),
        (0, '已完成'),
        (1, '进行中'),
        (2, '以登陆系统，未开始'),
    ), default=2, help_text='当前学生的答题状态', verbose_name='状态')
    bool_status = models.BooleanField(default=False, help_text='用于记录 是否更新[CronTabMain]班级任务计数器，任务完成情况下记录')
    key_user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='用户')
    key = models.ForeignKey(CronTabMain, on_delete=models.CASCADE, help_text='班级任务表')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.bool_status and self.status == 0:
            """更新班级任务计数器"""
            self.key.number += 1
            self.key.save()
            self.bool_status = True
            pass

        super(CronTabUser, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    pass


"""
End 记录班级考试任务进度相关信息
"""
