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

from datetime import datetime

# Create your views here.
import django_filters
from django.contrib.auth.hashers import make_password
from rest_framework import status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer, VerifyJSONWebTokenSerializer, \
    RefreshJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from account import models
from account import serializer
from exam.utils import SetCronTabMainStatus
from hanfurestful.utils.LimitOffsetPagination import Pagination
from hanfurestful.utils.viewsets import ModelViewSet

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class JSONWebTokenAPIView(object):
    """
    Base API View that various JWT interactions inherit from.
    """
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (
                        datetime.utcnow() +
                        api_settings.JWT_EXPIRATION_DELTA
                )
                response.set_cookie(
                    api_settings.JWT_AUTH_COOKIE,
                    token,
                    expires=expiration,
                    httponly=True
                )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebTokenView(GenericViewSet, JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer

    def create(self, request, *args, **kwargs):
        return super(ObtainJSONWebTokenView, self).post(request, *args, **kwargs)


class VerifyJSONWebTokenView(GenericViewSet, JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = VerifyJSONWebTokenSerializer

    def create(self, request, *args, **kwargs):
        return super(VerifyJSONWebTokenView, self).post(request, *args, **kwargs)


class RefreshJSONWebTokenView(GenericViewSet, JSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = RefreshJSONWebTokenSerializer

    def create(self, request, *args, **kwargs):
        # 执行 班级考试时间到期 自动更新状态
        SetCronTabMainStatus()()
        return super(RefreshJSONWebTokenView, self).post(request, *args, **kwargs)


class RegisterUserView(JSONWebTokenAPIView, GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    用户注册序列化
    """
    serializer_class = serializer.RegisterSerializer
    queryset = models.User.objects.filter()

    def perform_set(self, serializer):
        # models.Integral.objects.create()
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

    def perform_create(self, serializer):
        self.perform_set(serializer)
        serializer.save()

    def perform_update(self, serializer):
        self.perform_set(serializer)
        serializer.save()

    pass


class UserViewSet(ModelViewSet):
    """
    用户表
    基本信息的管理。例如：姓名、名族、年龄、籍贯、电话、照片、身份证号码、入学时间、毕业时间、第一份工作情况等信息的登记管理。

    school_info: {
                'school_info': this.fromData.formInline.key_school_info,
                'user': this.fromData.formInline.id
              }

    """

    class UserFilter(django_filters.FilterSet):
        class Meta:
            model = models.User
            fields = {
                "sex": ['exact', ],
                "stats": ['exact', ],
                "key_school_info": ['exact', 'icontains'],
                "username": ['exact', 'icontains'],
                "first_name": ['exact', 'icontains'],
                "email": ['exact', 'icontains'],
            }

    permission_classes = (IsAuthenticated,)
    # 标记需要进行jwt验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = Pagination
    serializer_class = serializer.UserSerializer
    queryset = models.User.objects.filter()
    # filterset_fields = ['sex', 'stats', 'key_school_info']
    filter_class = UserFilter



class UserInfoViewSet(ModelViewSet):
    """
    工作表
    第一份工作情况等信息的登记管理。
    """
    pagination_class = Pagination
    serializer_class = serializer.UserInfoSerializer
    queryset = models.UserInfo.objects.filter()
    filterset_fields = ['key', ]


class IntegralViewSet(ModelViewSet):
    """
    学员积分-学分表
    """
    pagination_class = Pagination
    serializer_class = serializer.IntegralSerializer
    queryset = models.Integral.objects.filter()
    filterset_fields = ['key', ]


class ViolationRecordSerializerViewSet(ModelViewSet):
    """
    学员积分-违规记录表
    """
    pagination_class = Pagination
    serializer_class = serializer.ViolationRecordSerializer
    queryset = models.ViolationRecord.objects.filter()


class EducationalViewSet(ModelViewSet):
    """
    学校
    """
    serializer_list_class = serializer.EducationalListSerializer
    serializer_class = serializer.EducationalSerializer
    queryset = models.Educational.objects.filter()
    pagination_class = None


class SchoolInfoViewSet(ModelViewSet):
    """
    班级
    """

    class SchoolInfoFilter(django_filters.FilterSet):
        class Meta:
            model = models.SchoolInfo
            fields = {
                "id": ['exact', ],
                "name": ['exact', 'icontains'],
                "key": ['exact', ],
            }

    serializer_list_class = serializer.SchoolInfoListSerializer
    serializer_class = serializer.SchoolInfoSerializer
    queryset = models.SchoolInfo.objects.filter()
    # filterset_fields = ['key', ]
    filter_class = SchoolInfoFilter
    # pagination_class = None


class UserSchoolInfoManyViewSet(ModelViewSet):
    """
    在授班级
    管理 教师 所教授的班级
    学生所对应的班级以及教师所教授的班级
    """
    serializer_list_class = serializer.UserSchoolInfoManyListSerializer
    serializer_class = serializer.UserSchoolInfoManySerializer
    queryset = models.UserSchoolInfoMany.objects.filter()
    filterset_fields = ['stats', 'user', 'school_info', ]
