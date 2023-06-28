# Generated by Django 4.2.2 on 2023-06-14 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_initial'),
        ('tasks', '0004_alter_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='authored_tasks', to='users.myuser'),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executed_tasks', to='users.myuser'),
        ),
    ]