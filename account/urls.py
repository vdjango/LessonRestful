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

from django.urls import path, include

from rest_framework import routers

from account import views

router = routers.DefaultRouter()

router.register('authorization', views.ObtainJSONWebTokenView, base_name='authorization')
router.register('authorization-register', views.RegisterUserView, base_name='authorization-register')
router.register('authorization-refresh', views.RefreshJSONWebTokenView, base_name='authorization-refresh')
router.register('authorization-verify', views.VerifyJSONWebTokenView, base_name='authorization-verify')
router.register('user', views.UserViewSet, base_name='user')
router.register('user-info', views.UserInfoViewSet, base_name='user-info')
router.register('user-integral', views.IntegralViewSet, base_name='user-integral')
router.register('user-violation', views.ViolationRecordSerializerViewSet, base_name='user-violation')
router.register('user-edu', views.EducationalViewSet, base_name='user-edu')
router.register('user-school', views.SchoolInfoViewSet, base_name='user-school')
router.register('user-school-many-user', views.UserSchoolInfoManyViewSet, base_name='user-school-many-user')

urlpatterns = [
    path('', include(router.urls))
]
