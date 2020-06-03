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
router.register('system-index', views.SystemConfigViewSet, base_name='system-index')
router.register('system-question', views.SystemQuestionViewSet, base_name='system-question')
router.register('system-control', views.SystemExamControlViewSet, base_name='system-control')

urlpatterns = [
    path('', include(router.urls))
]
