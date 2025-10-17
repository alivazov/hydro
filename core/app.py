"""
Основной класс приложения
"""

import tkinter as tk
from tkinter import ttk
import os
from .project_manager import ProjectManager
from .settings_manager import SettingsManager
from ui.main_window import MainWindow

class HydraulicCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.setup_app()
        
        # Инициализация менеджеров
        self.settings_manager = SettingsManager()
        self.project_manager = ProjectManager(self)
        
        # Загружаем настройки ДО создания UI
        self.load_settings()
        
        # Инициализация UI
        self.main_window = MainWindow(self)
        
        # Применяем настройки к UI
        self.apply_settings()
        
    def setup_app(self):
        """Базовая настройка приложения"""
        self.root.title("Гидравлический калькулятор")
        self.root.geometry("1200x600")
        
    def load_settings(self):
        """Загрузка настроек приложения"""
        self.settings_manager.load_settings()
        
    def save_settings(self):
        """Сохранение настроек приложения"""
        return self.settings_manager.save_settings()
        
    def apply_settings(self):
        """Применение настроек к UI"""
        # Применяем геометрию окна
        geometry = self.settings_manager.get_setting('window_geometry')
        if geometry:
            self.root.geometry(geometry)
            
        # Здесь можно добавить применение других настроек
        # (тема, параметры по умолчанию и т.д.)
        
    def exit_app(self):
        """Корректный выход из приложения"""
        # Сохраняем геометрию окна перед выходом
        self.settings_manager.update_window_geometry(self.root.geometry())
        
        # Сохраняем настройки
        self.save_settings()
        
        # Закрываем приложение
        self.root.quit()