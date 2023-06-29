from django.contrib import messages
# from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User

from task_manager.logger_config import logger




class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')

    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT,
                               default=None, verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, 
                                 related_name='executed_tasks', blank=True, null=True, 
                                 verbose_name='Исполнитель')

    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=False, 
                               verbose_name='Статус')
    label = models.ForeignKey(Label, on_delete=models.PROTECT, blank=True, null=True, 
                              verbose_name='Метка')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




# @receiver(pre_delete, sender=User)
# def prevent_user_deletion(sender, instance=modelTask.Task, **kwargs):
#     tasks_count = instance.objects.filter(status=sender)
#     if tasks_count > 0:
#         logger.error(f"Попытка удалить пользователя {sender.name}, связанного с задачей")
#         messages.error(gettext(f"User '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks."))
#         raise Exception(f"User '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks.")
    

# @receiver(pre_delete, sender=Label)
# def prevent_status_deletion(sender, instance=Task, **kwargs):
#     tasks_count = instance.objects.filter(status=sender)
#     if tasks_count > 0:
#         logger.error(gettext(f"Попытка удалить метку {sender.name}, связанного с задачей"))
#         messages.error(gettext(f"Label '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks."))
#         raise Exception(f"Label '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks.")
    
# @receiver(pre_delete, sender=Status)
# def prevent_status_deletion(sender, instance=Task, **kwargs):
#     tasks_count = instance.objects.filter(status=sender)
#     if tasks_count > 0:
#         logger.error(gettext(f"Попытка удалить пользователя {sender.name}, связанного с задачей"))
#         messages.error(gettext(f"Status '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks."))
#         raise Exception(f"Status '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks.")