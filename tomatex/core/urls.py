from django.urls import path

from tomatex.core.views import TaskCreateAPIView, TaskDetailAPIView, TaskPomodoroAPIView

urlpatterns = [
    path("tasks", TaskCreateAPIView.as_view(), name="tasks_resource"),
    path("tasks/<uuid:uid>", TaskDetailAPIView.as_view(), name="tasks_detail_resource"),
    path("tasks/<uuid:uid>/pomodoros", TaskPomodoroAPIView.as_view()),
]
