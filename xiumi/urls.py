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

from . import views

router = routers.DefaultRouter()
router.register('access_login', views.AccessLoginViewSet, base_name='access_login')
router.register('access_token', views.AccessTokenViewSet, base_name='access_token')
router.register('text_image', views.SomePathForArticlesViewSet, base_name='text_image')
router.register('file_image', views.SomePathForImageViewSet, base_name='file_image')

urlpatterns = [
    path('', include(router.urls))
]
