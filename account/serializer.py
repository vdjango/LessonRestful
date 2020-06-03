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

# from question.serializer import UserSemesterListSerializer
from question.serializer import UserSemesterListSerializer
from . import models


class UserBaseSerializer(serializers.ModelSerializer):
    '''
    用户信息序列化
    '''

    def create(self, validated_data):
        instance = super(UserBaseSerializer, self).create(validated_data)
        models.Integral(key=instance).save()
        return instance

    class Meta:
        model = models.User
        exclude = ['password']


"""
Start Auth
"""


class RegisterSerializer(UserBaseSerializer):
    '''
    用户注册序列化
    API： authorization-register
    '''

    class Meta:
        model = UserBaseSerializer.Meta.model
        fields = ['id', 'email', 'first_name', 'password']
        pass


"""
End Auth
"""


class UserInfoSerializer(serializers.ModelSerializer):
    """
    工作表
    第一份工作情况等信息的登记管理。
    """

    class Meta:
        model = models.UserInfo
        fields = '__all__'


class ViolationRecordSerializer(serializers.ModelSerializer):
    """
    违规记录表
    记录违规记录等扣分，实时扣分
    """

    class Meta:
        model = models.ViolationRecord
        fields = '__all__'


class IntegralSerializer(serializers.ModelSerializer):
    """
    学员积分-学分表
    """
    violation = ViolationRecordSerializer(many=True)
    key = UserBaseSerializer()

    class Meta:
        model = models.Integral
        fields = '__all__'


class EducationalListSerializer(serializers.ModelSerializer):
    """
    学校
    """

    class Meta:
        model = models.Educational
        fields = '__all__'


class SchoolInfoListSerializer(serializers.ModelSerializer):
    """
    班级
    """
    key_educational = EducationalListSerializer(required=False, read_only=True, source='key')
    user = serializers.SerializerMethodField(required=False, help_text='当前班级教师，可能会有多个教师')

    def get_user(self, instance):
        return UserBaseSerializer(instance.user_set.filter(stats=1), many=True).data

    class Meta:
        model = models.SchoolInfo
        fields = '__all__'


class EducationalSerializer(EducationalListSerializer):
    """
    学校-下级列表 班级
    """
    key_school_info = SchoolInfoListSerializer(many=True, required=False, read_only=True, source='schoolinfo_set')


class UserSchoolInfoManyListSerializer(serializers.ModelSerializer):
    """
    在授班级
    管理 教师 所教授的班级
    学生所对应的班级以及教师所教授的班级
    """
    school = SchoolInfoListSerializer(required=False, read_only=True, source='school_info')
    user_name = UserBaseSerializer(required=False, read_only=True, help_text='用户名称', source='user')

    class Meta:
        model = models.UserSchoolInfoMany
        fields = '__all__'

    pass


class UserSchoolInfoManySerializer(UserSchoolInfoManyListSerializer):
    user_semester = UserSemesterListSerializer(required=False, read_only=True, source='usersemester_set', many=True)

    def create(self, validated_data):
        if self.Meta.model.objects.filter(
                user=validated_data['user'],
                school_info=validated_data['school_info'],
        ).first():
            raise serializers.ValidationError({
                "detail": "已经添加过啦！"
            })

        return super(UserSchoolInfoManySerializer, self).create(validated_data)

    pass


class SchoolInfoSerializer(SchoolInfoListSerializer):
    """
    班级学生
    """
    user_school_many = UserBaseSerializer(
        source='user_set',
        many=True,
        help_text='班级里面的学生',
        required=False, read_only=True
    )

    pass


class UserSerializer(UserBaseSerializer, WritableNestedModelSerializer):
    '''
    用户序列化
    '''
    users_school_many = UserSchoolInfoManySerializer(many=True, required=False, read_only=True,
                                                     source='userschoolinfomany_set')
    edu = serializers.SerializerMethodField(required=False)

    def _school(self, validated_data):
        """
        更新班级信息
        :param validated_data:
        :return:
        """
        school_info_data = self.context['request'].data.get('school_info', None)
        if school_info_data:
            user_data = school_info_data.get('user', None)
            school_data = school_info_data.get('school_info', None)
            if not user_data or not school_data:
                raise serializers.ValidationError({
                    "detail": "缺少 use, school_info 参数"
                })
                pass

            user_many = models.UserSchoolInfoMany.objects.filter(user=user_data)
            if user_many.first():
                user_many.update(school_info=school_data)
                print('update')
            else:
                print('create')
                user_ser = UserSchoolInfoManySerializer(data={
                    'school_info': school_data,
                    'user': user_data
                })
                user_ser.is_valid()
                user_ser.save()
                # models.UserSchoolInfoMany(user=user_data, school_info=school_data).save()
                pass
            pass

    def create(self, validated_data):
        self._school(validated_data)
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        self._school(validated_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def get_edu(self, instance):
        if instance.key_school_info:
            s = [i.school_info.key.id for i in instance.userschoolinfomany_set.filter()]
            return s
        return None

    pass
