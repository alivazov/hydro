"""
Менеджер настроек приложения
"""

import json
import os
from utils.file_operations import save_json, load_json, ensure_directory_exists

class SettingsManager:
    def __init__(self):
        self.projects_folder = os.path.join(
            os.path.expanduser("~"), 
            "ГидравлическийКалькулятор"
        )
        self.settings_file = os.path.join(self.projects_folder, "app_settings.json")
        
        # Настройки по умолчанию
        self.settings = {
            'auto_save': False,
            'backup_interval': 10,
            'recent_projects': [],
            'window_geometry': '1200x600',
            'default_material': 'Пластик',
            'last_project_folder': self.projects_folder,
            'theme': 'default'
        }
        
        # Создаем папку для проектов если ее нет
        ensure_directory_exists(self.projects_folder)
        
    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(self.settings_file):
                loaded_settings = load_json(self.settings_file)
                if loaded_settings:
                    # Обновляем только существующие ключи, чтобы не потерять новые настройки по умолчанию
                    for key, value in loaded_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
                    print(f"Настройки загружены из {self.settings_file}")
                else:
                    print("Файл настроек пустой или поврежден, используются настройки по умолчанию")
            else:
                print("Файл настроек не найден, используются настройки по умолчанию")
                # Создаем файл с настройками по умолчанию
                self.save_settings()
                
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}, используются настройки по умолчанию")
            
    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            success = save_json(self.settings, self.settings_file)
            if success:
                print(f"Настройки сохранены в {self.settings_file}")
            else:
                print("Ошибка сохранения настроек")
            return success
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            return False
        
    def get_setting(self, key, default=None):
        """Получение значения настройки"""
        return self.settings.get(key, default)
        
    def set_setting(self, key, value):
        """Установка значения настройки"""
        self.settings[key] = value
        # Автоматически сохраняем при изменении
        self.save_settings()
        
    def add_recent_project(self, file_path):
        """Добавление проекта в список недавних"""
        if file_path in self.settings['recent_projects']:
            self.settings['recent_projects'].remove(file_path)
            
        self.settings['recent_projects'].insert(0, file_path)
        self.settings['recent_projects'] = self.settings['recent_projects'][:10]  # Ограничение
        
        # Сохраняем изменения
        self.save_settings()
        
    def remove_recent_project(self, file_path):
        """Удаление проекта из списка недавних"""
        if file_path in self.settings['recent_projects']:
            self.settings['recent_projects'].remove(file_path)
            self.save_settings()
            
    def get_recent_projects(self):
        """Получение списка недавних проектов"""
        return self.settings['recent_projects']
        
    def update_window_geometry(self, geometry):
        """Обновление геометрии окна"""
        self.settings['window_geometry'] = geometry
        self.save_settings()