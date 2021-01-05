from rest_framework import serializers

from tomatex.core.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['uid', 'description', 'created_at']
        read_only_fields = ['uid', 'created_at',]