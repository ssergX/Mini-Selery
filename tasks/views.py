# tasks/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.utils import timezone
import random
import time
import threading
from queue import Queue

task_queue = Queue()

MAX_CONCURRENT_TASKS = 2

# Семафор для ограничения количества одновременно выполняемых задач
semaphore = threading.Semaphore(MAX_CONCURRENT_TASKS)


def process_task(task_id):
    with semaphore:
        task = Task.objects.get(id=task_id)
        task.status = 'Run'
        task.start_time = timezone.now()
        task.save()

        exec_time = random.randint(0, 10)
        time.sleep(exec_time)

        task.status = 'Completed'
        task.exec_time = exec_time
        task.save()


def worker():
    while True:
        task_id = task_queue.get()
        if task_id is None:
            break
        process_task(task_id)
        task_queue.task_done()


def start_workers():
    for _ in range(MAX_CONCURRENT_TASKS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()


start_workers()


@api_view(['POST'])
def create_task(request):
    task = Task.objects.create()
    task_queue.put(task.id)
    return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def task_status(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_task_status(request):
    try:
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)