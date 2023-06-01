from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from task_manager.tasks.models import Task
from django.utils.translation import gettext

from task_manager.logger_config import logger




@receiver(pre_delete, sender=User)
def prevent_status_deletion(sender, instance=Task, **kwargs):
    tasks_count = instance.objects.filter(status=sender)
    if tasks_count > 0:
        logger.error("Попытка удалить статус, связанный с задачей")
        messages.error(f"Status '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks.")        
        raise Exception(f"Status '{instance.name}' cannot be deleted as it is associated with {tasks_count} tasks.")