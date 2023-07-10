from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext

from django.core.exceptions import ValidationError

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User

from task_manager.logger_config import logger


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')

    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               default=None, verbose_name=gettext('Автор'))
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name='executed_tasks', blank=True, null=True,
                                 verbose_name=gettext('Исполнитель'), default='')

    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=False,
                               verbose_name=gettext('Статус'))
    label = models.ManyToManyField(Label, blank=True, null=True,
                                   verbose_name=gettext('Метки'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Label)
def prevent_label_deletion(sender, instance, **kwargs):
    if instance.task_set.exists():
        logger.debug(f'Невозможно удалить метку {instance}')
        raise ValidationError('Невозможно удалить метку, потому что она используется')
