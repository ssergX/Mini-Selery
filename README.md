Установка зависимостей: pip install -r requirements.txt

Миграции:
python manage.py makemigrations
python manage.py migrate


Основные эндпоинты:
api/ create_task/ 
api/ task_status/<int:task_id>/ 
api/ all_task_status/
