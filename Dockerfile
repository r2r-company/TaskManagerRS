# 1. Вибір базового образу Python
FROM python:3.8-slim-buster

# 2. Оновлюємо пакети та встановлюємо git для клонування репозиторію
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev gcc python3-dev musl-dev

# 3. Встановлюємо робочу директорію
WORKDIR /app

# 4. Клонуємо проект з GitHub
RUN git clone https://github.com/r2r-company/TaskManagerRS.git /app

# 5. Створюємо віртуальне середовище Python
RUN python -m venv venv

# 6. Активуємо віртуальне середовище і встановлюємо pip
RUN /app/venv/bin/pip install --upgrade pip

# 7. Встановлюємо всі залежності з requirements.txt
RUN /app/venv/bin/pip install -r requirements.txt

# 8. Виконуємо міграції (створення таблиць в базі даних)
RUN /app/venv/bin/python manage.py migrate

# 9. Експортуємо порт (8000 — стандартний порт Django)
EXPOSE 8000

# 10. Запускаємо сервер Django
CMD ["/app/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
