"""
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
"""
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from . import models


class SystemConfigSerializer(serializers.ModelSerializer):
    """
    分页设置
    """

    class Meta:
        model = models.SystemConfig
        fields = '__all__'


class SystemQuestionSerializer(serializers.ModelSerializer):
    """
    刷/考相关设置
    控制前端抓取题库题项数量
    """

    class Meta:
        model = models.SystemQuestion
        fields = '__all__'


class SystemExamControlSerializer(serializers.ModelSerializer):
    """
    考试周期控制
    计时任务
    """

    class Meta:
        model = models.SystemExamControl
        fields = '__all__'
