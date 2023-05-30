from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, related_name='authored_tasks')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='executed_tasks')
    # label = models.ForeignKey(Label, on_delete=models.SET_DEFAULT, default=None)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
