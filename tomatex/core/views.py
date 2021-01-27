from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tomatex.core.models import Task
from tomatex.core.serializers import (
    TaskPomodoroSerializer,
    TaskPomodorosSerializer,
    TaskSerializer,
)


class TaskCreateAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    def get(self, request, uid):
        task = get_object_or_404(Task, uid=uid)
        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def put(self, request, uid):
        task = get_object_or_404(Task, uid=uid)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, uid):
        task = get_object_or_404(Task, uid=uid)
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskPomodoroAPIView(APIView):
    def get(self, request, uid):
        task = get_object_or_404(Task, uid=uid)
        serializer = TaskPomodorosSerializer(task)

        return Response(serializer.data)

    def post(self, request, uid):
        task = get_object_or_404(Task, uid=uid)
        serializer = TaskPomodoroSerializer(task=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
