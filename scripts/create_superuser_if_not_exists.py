#!/usr/bin/env python
"""
Скрипт для создания суперпользователя, если он не существует.
Используется переменные окружения:
- ADMIN_USERNAME
- ADMIN_EMAIL
- ADMIN_PASSWORD
"""
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barter_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

def create_superuser_if_not_exists():
    """Создаёт суперпользователя, если он ещё не существует"""
    username = os.environ.get('ADMIN_USERNAME')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')
    
    if not all([username, email, password]):
        print("Ошибка: Не установлены переменные окружения для создания суперпользователя")
        print(f"ADMIN_USERNAME: {'Установлена' if username else 'Не установлена'}")
        print(f"ADMIN_EMAIL: {'Установлена' if email else 'Не установлена'}")
        print(f"ADMIN_PASSWORD: {'Установлена' if password else 'Не установлена'}")
        return
    
    try:
        # Проверяем существование пользователя
        if not User.objects.filter(username=username).exists():
            print(f"Создание суперпользователя: {username} ({email})")
            User.objects.create_superuser(
                username=username, 
                email=email, 
                password=password
            )
            print("Суперпользователь успешно создан")
        else:
            print(f"Суперпользователь {username} уже существует")
    except IntegrityError as e:
        print(f"Ошибка при создании суперпользователя: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    create_superuser_if_not_exists()
