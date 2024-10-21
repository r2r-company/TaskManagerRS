# Generated by Django 5.1.2 on 2024-10-20 20:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата - виставлення')),
                ('task_name', models.CharField(max_length=255, verbose_name='Назва задачі')),
                ('task_description', models.TextField(verbose_name='Опис задачі')),
                ('task_number', models.CharField(default='00-000-0001', max_length=20, verbose_name='Номер задачі')),
                ('status', models.CharField(choices=[('new', 'Новий'), ('in_progress', 'В роботі'), ('completed', 'Виконано'), ('under_discussion', 'Під обговоренням')], max_length=20, verbose_name='Статус')),
                ('work_type', models.CharField(choices=[('montage', 'Монтаж'), ('remote', 'Віддалені')], max_length=20, verbose_name='Вид роботи')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Виконавець')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачі',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Повідомлення')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mainapp.taskmodel', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Переписка',
                'verbose_name_plural': 'Переписки',
            },
        ),
    ]
