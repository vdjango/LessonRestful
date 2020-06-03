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
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from account.models import SchoolInfo
from . import models


class CronTabMainListSerializer(serializers.ModelSerializer):
    """
    记录班级任务执行情况
    定时任务触发后，添加相关班级记录。此次任务完成后，更新[status]状态至已完成
    """

    class Meta:
        model = models.CronTabMain
        fields = '__all__'


class CronTabMainSerializer(CronTabMainListSerializer):
    class SchoolInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = SchoolInfo
            fields = '__all__'

    school = SchoolInfoSerializer(
        source='key_school', required=False,
        read_only=True, help_text='班级'
    )
    pass


class CronTabUserListSerializer(serializers.ModelSerializer):
    """
    记录学员完成任务情况
    学生登陆系统 检查班级是否有任务可完成，添加任务记录，学员逐步完成任务 更新[status]状态至已完成
    """

    class Meta:
        model = models.CronTabUser
        fields = '__all__'


class CronTabUserSerializer(CronTabUserListSerializer):
    cron_tab_main = CronTabMainSerializer(
        source='key', required=False,
        read_only=True, help_text='记录班级任务执行情况')
    pass
