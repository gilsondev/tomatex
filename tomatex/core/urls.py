from django.urls import path

from tomatex.core.views import TaskCreateAPIView

urlpatterns = [
    path('api/tasks', TaskCreateAPIView.as_view(), name='create_task_resource')
]
