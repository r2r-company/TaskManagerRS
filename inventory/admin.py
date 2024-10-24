from django.contrib import admin
from .models import Equipment, Component, EquipmentType

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('component_type', 'equipment', 'serial_number')
    list_filter = ('equipment',)  # Фільтр за обладнанням
    search_fields = ('component_type', 'serial_number', 'equipment__serial_number', 'equipment__inventory_number', 'equipment__model')

admin.site.register(Equipment)
admin.site.register(Component, ComponentAdmin)
admin.site.register(EquipmentType)
