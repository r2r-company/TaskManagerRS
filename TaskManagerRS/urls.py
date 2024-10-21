from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Імпортуємо функцію redirect

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # Це URL для Grappelli
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('admin/')),  # Переадресація з головної сторінки на адмінку
]
