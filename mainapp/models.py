from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TaskModel(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('in_progress', 'В роботі'),
        ('completed', 'Виконано'),
        ('under_discussion', 'Під обговоренням'),
    ]

    WORK_TYPE_CHOICES = [
        ('montage', 'Монтаж'),
        ('remote', 'Віддалені'),
    ]

    executor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Виконавець")
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Дата - виставлення")
    task_name = models.CharField(max_length=255, verbose_name="Назва задачі")
    task_description = models.TextField(verbose_name="Опис задачі")
    task_number = models.CharField(max_length=20, verbose_name="Номер задачі", default="00-000-0001")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES, verbose_name="Вид роботи")

    def __str__(self):
        return self.task_name

    def executor_full_name(self):
        return f"{self.executor.first_name} {self.executor.last_name}"

    executor_full_name.short_description = 'Виконавець'  # Це буде підпис колонки в адмінці

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачі"


class Message(models.Model):
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='messages', verbose_name="Задача")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Повідомлення")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата створення")

    def __str__(self):
        return f"Повідомлення від {self.author.username} для задачі {self.task.task_name}"

    class Meta:
        verbose_name = "Переписка"
        verbose_name_plural = "Переписки"


class InvoiceModel(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name="Номер рахунку", blank=True)
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Дата створення")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Виконавець")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума", default=0.00)

    def __str__(self):
        return self.invoice_number

    class Meta:
        verbose_name = "Рахунок"
        verbose_name_plural = "Рахунки"

    def calculate_total(self):
        # Перевіряємо, чи є пов'язані послуги (services)
        total = sum(item.price * item.quantity for item in self.services.all())
        return total


# Сигнал для автоматичної генерації номера рахунку
@receiver(pre_save, sender=InvoiceModel)
def generate_invoice_number(sender, instance, **kwargs):
    if not instance.invoice_number:
        last_invoice = InvoiceModel.objects.order_by('id').last()
        if last_invoice:
            last_number = last_invoice.invoice_number.split('-')[-1]
            new_number = int(last_number) + 1
        else:
            new_number = 1
        instance.invoice_number = f"РА-000-00-{new_number}"


class ServiceModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, related_name='services', on_delete=models.CASCADE, verbose_name="Рахунок")
    service_name = models.CharField(max_length=255, verbose_name="Назва послуги")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    time_spent = models.DurationField(blank=True, null=True, verbose_name="Час (необов'язково)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна за одиницю")

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"
