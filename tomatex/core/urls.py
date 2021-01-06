from django.urls import path

from tomatex.core.views import TaskCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path('tasks', TaskCreateAPIView.as_view(), name='tasks_resource'),
    path('tasks/<uuid:uid>', TaskDetailAPIView.as_view(),
         name='tasks_detail_resource'),
]
