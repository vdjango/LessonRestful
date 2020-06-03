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
router.register('class-question', views.ClassQuestionViewSet, base_name='class-question')
router.register('class-question-model', views.ClassQuesModelViewSet, base_name='class-question-model')
router.register('class-question-chapter', views.ClassQuesChapterViewSet, base_name='class-question-chapter')
router.register('question', views.QuestionViewSet, base_name='question')
router.register('question-answer', views.QuestionAnswerViewSet, base_name='question-answer')
router.register('question-exam', views.ExamQuestionsVIewSet, base_name='question-exam')
router.register('user-semester', views.UserSemesterViewSet, base_name='user-semester')
router.register('user-exam-stock', views.ExamStockViewSet, base_name='user-exam-stock')

urlpatterns = [
    path('', include(router.urls))
]
