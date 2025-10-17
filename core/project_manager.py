"""
Менеджер проектов
"""

import json
import os
from datetime import datetime
from tkinter import messagebox, filedialog
from models.project import Project
from utils.file_operations import save_json, load_json, ensure_directory_exists

class ProjectManager:
    def __init__(self, app):
        self.app = app
        self.current_project = Project()
        self.projects_folder = self.app.settings_manager.projects_folder
        self.ensure_projects_folder()
        
    def ensure_projects_folder(self):
        """Создает папку для проектов если ее нет"""
        ensure_directory_exists(self.projects_folder)
            
    def new_project(self):
        """Создание нового проекта"""
        if self.has_unsaved_changes():
            if not self.ask_save_changes():
                return False
                
        self.current_project = Project()
        self.app.main_window.update_project_info()
        print("Создан новый проект")
        return True
        
    def save_project(self, file_path=None):
        """Сохранение проекта"""
        try:
            if not file_path:
                file_path = self.current_project.file_path
                
            if not file_path:
                return self.save_project_as()
                
            # Собираем данные из UI
            self.collect_ui_data()
            
            # Сохраняем проект
            success = self.current_project.save(file_path)
            if success:
                self.app.main_window.update_project_info()
                
                # Добавляем в недавние проекты
                self.app.settings_manager.add_recent_project(file_path)
                print(f"Проект сохранен: {file_path}")
            else:
                print(f"Ошибка сохранения проекта: {file_path}")
                
            return success
            
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить проект: {str(e)}")
            print(f"Ошибка сохранения проекта: {e}")
            return False
            
    def save_project_as(self):
        """Сохранение проекта как..."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".hydro",
            filetypes=[
                ("Гидравлические проекты", "*.hydro"),
                ("JSON файлы", "*.json"),
                ("Все файлы", "*.*")
            ],
            initialdir=self.app.settings_manager.get_setting('last_project_folder', self.projects_folder)
        )
        
        if file_path:
            # Сохраняем папку для следующего использования
            folder = os.path.dirname(file_path)
            self.app.settings_manager.set_setting('last_project_folder', folder)
            
            return self.save_project(file_path)
        return False
        
    def load_project(self, file_path=None):
        """Загрузка проекта"""
        try:
            if self.has_unsaved_changes():
                if not self.ask_save_changes():
                    return False
                    
            if not file_path:
                file_path = filedialog.askopenfilename(
                    filetypes=[
                        ("Гидравлические проекты", "*.hydro"),
                        ("JSON файлы", "*.json"),
                        ("Все файлы", "*.*")
                    ],
                    initialdir=self.app.settings_manager.get_setting('last_project_folder', self.projects_folder)
                )
                
            if file_path and os.path.exists(file_path):
                # Сохраняем папку для следующего использования
                folder = os.path.dirname(file_path)
                self.app.settings_manager.set_setting('last_project_folder', folder)
                
                self.current_project = Project.load(file_path)
                self.apply_ui_data()
                self.app.main_window.update_project_info()
                
                # Добавляем в недавние проекты
                self.app.settings_manager.add_recent_project(file_path)
                print(f"Проект загружен: {file_path}")
                return True
            else:
                print("Файл не выбран или не существует")
                return False
                
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить проект: {str(e)}")
            print(f"Ошибка загрузки проекта: {e}")
            return False
        
    def has_unsaved_changes(self):
        """Проверяет есть ли несохраненные изменения"""
        return self.current_project.is_modified
        
    def ask_save_changes(self):
        """Спрашивает о сохранении изменений"""
        result = messagebox.askyesnocancel(
            "Несохраненные изменения",
            "Сохранить изменения в текущем проекте?"
        )
        
        if result is None:  # Cancel
            return False
        elif result:  # Yes
            return self.save_project()
            
        return True
        
    def collect_ui_data(self):
        """Собирает данные из UI в модель проекта"""
        try:
            if hasattr(self.app, 'main_window'):
                # Собираем данные из всех вкладок
                self.current_project.data = {
                    "calculations": self.app.main_window.calculations_tab.get_data(),
                    "construction_stages": self.app.main_window.construction_tab.get_data(),
                    "platforms": self.app.main_window.platforms_tab.get_data(),
                    "capacity_check": self.app.main_window.capacity_tab.get_data(),
                    "balance": self.app.main_window.balance_tab.get_data()
                }
                print("Данные собраны из UI")
        except Exception as e:
            print(f"Ошибка сбора данных из UI: {e}")
        
    def apply_ui_data(self):
        """Применяет данные проекта к UI"""
        try:
            if hasattr(self.app, 'main_window'):
                # Применяем данные ко всем вкладкам
                data = self.current_project.data
                
                self.app.main_window.calculations_tab.set_data(data.get("calculations", {}))
                self.app.main_window.construction_tab.set_data(data.get("construction_stages", []))
                self.app.main_window.platforms_tab.set_data(data.get("platforms", []))
                self.app.main_window.capacity_tab.set_data(data.get("capacity_check", []))
                self.app.main_window.balance_tab.set_data(data.get("balance", []))
                
                print("Данные применены к UI")
        except Exception as e:
            print(f"Ошибка применения данных к UI: {e}")