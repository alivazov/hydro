"""
Базовый класс для всех вкладок
"""

import tkinter as tk
from tkinter import ttk

class BaseTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        self.create_widgets()
        
    def create_widgets(self):
        """Создание виджетов вкладки (должен быть реализован в подклассах)"""
        raise NotImplementedError("Метод create_widgets должен быть реализован в подклассе")
        
    def get_data(self):
        """Получение данных из вкладки"""
        return {}
        
    def set_data(self, data):
        """Установка данных во вкладку"""
        pass
        
    def validate_data(self):
        """Валидация данных вкладки"""
        return True