from django.db import models
from django.contrib.auth.models import User

# Модель для типів обладнання
class EquipmentType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип обладнання"
        verbose_name_plural = "Тип обладнання"


# Модель для обладнання
class Equipment(models.Model):
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    inventory_number = models.CharField(max_length=100, unique=True, verbose_name="Інвентаризаційний номер")
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, verbose_name="Тип")
    manufacturer = models.CharField(max_length=100, verbose_name="Виробник")
    model = models.CharField(max_length=100, verbose_name="Модель")
    purchase_date = models.DateField(verbose_name="Дата покупки")
    warranty_expiry_date = models.DateField(verbose_name="Гарантія")
    status = models.CharField(max_length=50, choices=[
        ('in_use', 'Використовується'),
        ('in_repair', 'В ремонті'),
        ('on_stock', 'На складі'),
        ('disposed', 'Списане'),
    ], verbose_name="Статус")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Виконавець")

    def __str__(self):
        return f"{self.type.name} - {self.serial_number}"

    class Meta:
        verbose_name = "Обладнання для комплектуючих"
        verbose_name_plural = "Обладнання для комплектуючих"


# Модель для комплектуючих
class Component(models.Model):
    equipment = models.ForeignKey(Equipment, related_name='components', on_delete=models.CASCADE, verbose_name="Компонент")
    component_type = models.CharField(max_length=100, verbose_name="Тип")
    manufacturer = models.CharField(max_length=100, verbose_name="Виробник")
    model = models.CharField(max_length=100, verbose_name="Модель")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Серійний номер")

    def __str__(self):
        return f"{self.component_type} - {self.serial_number}"

    class Meta:
        verbose_name = "Комплектуючі"
        verbose_name_plural = "Комплектуючі"
