from django.urls import path
from .views import create_task, task_status, all_task_status

urlpatterns = [
    path('create_task/', create_task, name='create_task'),
    path('task_status/<int:task_id>/', task_status, name='task_status'),
    path('all_task_status/', all_task_status, name='all_task_status'),
]
