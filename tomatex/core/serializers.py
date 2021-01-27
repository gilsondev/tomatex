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
    class Meta:
        model = Pomodoro
        fields = ("id", "started_at", "ended_at", "completed")

    def __init__(self, task, **kwargs):
        self.task = task
        super().__init__(**kwargs)

    def create(self, validated_data):
        return Pomodoro.objects.create(task=self.task, **validated_data)


class PomodorosInfoSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    incompleted = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["completed", "incompleted"]

    def get_completed(self, obj):
        return obj.total_completed()

    def get_incompleted(self, obj):
        return obj.total_incompleted()


class TaskPomodorosSerializer(serializers.ModelSerializer):
    pomodoros = PomodorosInfoSerializer()

    class Meta:
        model = Task
        fields = ["uid", "description", "pomodoros"]
        read_only_fields = ["uid", "description" "pomodoros"]
