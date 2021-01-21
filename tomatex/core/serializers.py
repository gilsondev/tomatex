from rest_framework import serializers

from tomatex.core.models import Pomodoro, Task

POMODORO_UNIT_TIMER = 25
ONE_MINUTE = 60


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["uid", "description", "created_at"]
        read_only_fields = [
            "uid",
            "created_at",
        ]


class TaskPomodoroSerializer(serializers.ModelSerializer):
    # started_at = serializers.DateTimeField()
    # ended_at = serializers.DateTimeField()
    # completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Pomodoro
        fields = ("id", "started_at", "ended_at", "completed")

    def __init__(self, task, **kwargs):
        self.task = task
        super().__init__(**kwargs)

    def create(self, validated_data):
        return Pomodoro.objects.create(task=self.task, **validated_data)
