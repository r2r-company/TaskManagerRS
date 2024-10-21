# 🚀 TaskManagerRS

### Завдання та рахунки

TaskManagerRS — це система управління задачами та рахунками, створена на Django.

## 🛠️ Інсталяція

Щоб встановити та запустити проект на вашому комп'ютері, дотримуйтесь наступних кроків:

### 1. Клонування репозиторію

```bash
git clone https://github.com/yourusername/TaskManagerRS.git
cd TaskManagerRS
```

### 2. Створення та активація віртуального середовища (опціонально)
🔧 Рекомендується використовувати віртуальне середовище для ізоляції залежностей проекту:

## Створіть віртуальне середовище
```bash
python -m venv venv
```
## Активуйте його
# Для Windows:
```bash
venv\Scripts\activate
```
# Для MacOS/Linux:
```bash
source venv/bin/activate
```
### 3. Встановлення залежностей
📦 Встановіть усі залежності, зазначені у файлі [requirements.txt](requirements.txt)

```bash
pip install -r requirements.txt
```

### 4. Міграція бази даних
📊 Виконайте міграції для створення бази даних:

```bash
python manage.py migrate
```
### 5. Створення суперкористувача
👤 Створіть суперкористувача для доступу до адмінки Django:

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера розробки
🚀 Запустіть локальний сервер:

```bash
python manage.py runserver
```

Тепер ви можете зайти на http://127.0.0.1:8000/ і переглянути свій проект.

### 📂 Структура проекту

![image](https://github.com/user-attachments/assets/2a017115-58c0-4547-bcb2-6f6e61519251)

