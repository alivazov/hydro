"""
Операции с файлами
"""

import json
import os
from datetime import datetime

def ensure_directory_exists(path):
    """Проверка существования директории и создание если нужно"""
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"Создана директория: {path}")
        return True
    except Exception as e:
        print(f"Ошибка создания директории {path}: {e}")
        return False

def save_json(data, file_path, indent=4):
    """Сохранение данных в JSON файл"""
    try:
        # Создаем директорию если ее нет
        directory = os.path.dirname(file_path)
        ensure_directory_exists(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent, default=str)
        print(f"Файл сохранен: {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения файла {file_path}: {e}")
        return False

def load_json(file_path):
    """Загрузка данных из JSON файла"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Файл загружен: {file_path}")
            return data
        else:
            print(f"Файл не найден: {file_path}")
            return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Ошибка загрузки файла {file_path}: {e}")
        return None

def get_file_modified_time(file_path):
    """Получение времени изменения файла"""
    if os.path.exists(file_path):
        return datetime.fromtimestamp(os.path.getmtime(file_path))
    return None

def file_exists(file_path):
    """Проверка существования файла"""
    return os.path.exists(file_path) and os.path.isfile(file_path)