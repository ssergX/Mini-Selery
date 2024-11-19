# tasks/models.py
from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('In Queue', 'In Queue'),
        ('Run', 'Run'),
        ('Completed', 'Completed'),
    ]

    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    exec_time = models.IntegerField(null=True, blank=True)  # Время выполнения в секундах
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Queue')

    def __str__(self):
        return f"Task {self.id} - {self.status}"
