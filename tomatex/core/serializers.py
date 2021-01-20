from rest_framework import serializers

from tomatex.core.models import Task

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


class TaskPomodoroSerializer(serializers.Serializer):
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField()
    completed = serializers.BooleanField(read_only=True)

    def validate(self, data):
        started_at = data["started_at"]
        ended_at = data["ended_at"]
        data["completed"] = False

        diff = ended_at - started_at
        total_minutes = diff.seconds / ONE_MINUTE

        if total_minutes >= POMODORO_UNIT_TIMER:
            data["completed"] = True

        return data
