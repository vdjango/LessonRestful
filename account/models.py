'''

Copyright (C) 2019 张珏敏.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from hanfurestful.utils import timezone


class Educational(models.Model):
    """
    学校
    """
    name = models.CharField(max_length=100, help_text='学校名称')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)

    class Meta:
        ordering = ['-id']


class SchoolInfo(models.Model):
    """
    班级
    """
    name = models.CharField(max_length=100, help_text='班级名称')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)
    key = models.ForeignKey(Educational, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class User(AbstractUser):
    """
    用户表
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    stats = models.IntegerField(choices=(
        (0, '学生'),
        (1, '教师'),
    ), default=0, help_text='当前身份')
    email = models.EmailField(_('email address'), unique=True)
    famous_race = models.CharField(help_text='名族', max_length=100, null=True, blank=True)
    native_place = models.CharField(max_length=100, help_text='籍贯', null=True, blank=True)
    age = models.IntegerField(help_text='年龄', null=True, blank=True)
    sex = models.IntegerField(help_text='性别', choices=(
        (0, '男'),
        (1, '女'),
        (2, '保密'),
    ), default=2)
    telephone = models.CharField(max_length=50, help_text='电话', null=True, blank=True)
    image = models.ImageField(help_text='头像', upload_to='', null=True, blank=True)
    id_card = models.CharField(max_length=50, help_text='身份证', null=True, blank=True)
    entrance = models.DateTimeField(help_text='入学时间', null=True, blank=True)
    graduation = models.DateTimeField(help_text='毕业时间', null=True, blank=True)
    key_school_info = models.ManyToManyField(SchoolInfo, blank=True, help_text='班级-学校',
                                             through='UserSchoolInfoMany')

    def save(self, *args, **kwargs):
        if not self.username: self.username = timezone.mktime()
        if not kwargs.get('force_insert', None):
            self.userschoolinfomany_set.update(stats=self.stats)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        if self.last_name: return self.last_name
        return self.username

    class Meta(AbstractUser.Meta):
        ordering = ['-id']
        pass


class UserInfo(models.Model):
    """
    工作表
    第一份工作情况等信息的登记管理。
    """
    unit = models.CharField(max_length=200, help_text='单位')
    entry_time = models.DateTimeField(help_text='入职时间')
    position = models.CharField(max_length=50, help_text='职位')
    work_telephone = models.CharField(max_length=50, help_text='单位电话')
    key = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')

    class Meta:
        ordering = ['-id']


class Integral(models.Model):
    """
    学员积分-学分表
    """
    number = models.DecimalField(default=100, max_digits=5, decimal_places=2, help_text='分数')
    key = models.OneToOneField(User, on_delete=models.CASCADE, related_name='integral')

    class Meta:
        ordering = ['-id']

    pass


class ViolationRecord(models.Model):
    """
    违规记录表
    记录违规记录等扣分，实时扣分
    """
    text = models.TextField(help_text='违规说明')
    number = models.DecimalField(max_digits=5, decimal_places=2, help_text='实扣分值')
    date = models.DateTimeField(auto_now_add=True, help_text='添加时间')
    key = models.ForeignKey(Integral, on_delete=models.CASCADE, related_name='violation')

    def save(self, *args, **kwargs):
        self.key.number += self.number
        self.key.save()
        super(ViolationRecord, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']


class UserSchoolInfoMany(models.Model):
    """
    在授班级
    管理 教师 所教授的班级
    学生所对应的班级以及教师所教授的班级
    """
    school_info = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, help_text='班级')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='用户')
    stats = models.IntegerField(choices=(
        (0, '学生'),
        (1, '教师'),
    ), default=0, help_text='当前人员身份')
    add_time = models.DateTimeField(auto_now_add=True, auto_now=False, help_text='添加时间')
    lately_time = models.DateTimeField(auto_now_add=False, auto_now=True, help_text='最近一次修改', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.stats = self.user.stats
        super(UserSchoolInfoMany, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    pass
