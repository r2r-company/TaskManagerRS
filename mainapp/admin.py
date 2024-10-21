from django.contrib import admin
from django.http import FileResponse

from .PDF_create import generate_invoice_template
from .models import TaskModel, Message, InvoiceModel, ServiceModel
from django.contrib.auth.models import User
from django import forms


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # Кількість порожніх форм для нових записів
    readonly_fields = ('created_at',)  # Поле дати лише для читання, автор більше не потрібен
    can_delete = True

    # Оновлюємо метод збереження форми
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Якщо це новий об'єкт, а не редагування
            obj.author = request.user  # Призначаємо автора
        super().save_model(request, obj, form, change)




# Форма для кастомного відображення користувачів
class TaskForm(forms.ModelForm):
    # Змінимо поле виконавця на відображення повного імені
    executor = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select, label="Виконавець")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else obj.username

    class Meta:
        model = TaskModel
        fields = '__all__'

# Оновлюємо адміністрування задачі
class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ('task_name', 'executor_full_name', 'status', 'creation_date')
    inlines = [MessageInline]  # Додаємо переписку як інлайн


class ServiceInline(admin.TabularInline):
    model = ServiceModel
    extra = 1  # Кількість порожніх рядків для додавання


@admin.register(InvoiceModel)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [ServiceInline]
    list_display = ['invoice_number', 'executor', 'creation_date', 'total_amount']
    readonly_fields = ('invoice_number',)
    actions = ['download_pdf']

    # Додаємо дію для завантаження PDF
    def download_pdf(self, request, queryset):
        if queryset.count() == 1:
            invoice = queryset.first()
            buffer = generate_invoice_template(invoice)
            return FileResponse(buffer, as_attachment=True, filename=f'Invoice_{invoice.invoice_number}.pdf')
        else:
            self.message_user(request, "Виберіть лише один рахунок для експорту.", level='error')

    download_pdf.short_description = "Завантажити рахунок у PDF"



admin.site.register(TaskModel, TaskAdmin)
