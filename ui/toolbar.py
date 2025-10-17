"""
Панель инструментов (дополнительный модуль)
"""

import tkinter as tk
from tkinter import ttk
from .dialogs.project_properties import ProjectPropertiesDialog


class Toolbar:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_toolbar()
        
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = ttk.Frame(self.parent)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Кнопки
        ttk.Button(toolbar, text="Новый проект", 
                  command=self.app.project_manager.new_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Открыть", 
                  command=self.app.project_manager.load_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Сохранить", 
                  command=self.app.project_manager.save_project).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        ttk.Button(toolbar, text="Свойства проекта", 
                  command=self.show_project_properties).pack(side=tk.LEFT, padx=2)
        
        # Информация о проекте (справа)
        self.project_info_label = ttk.Label(toolbar, text="Проект: Новый проект")
        self.project_info_label.pack(side=tk.RIGHT, padx=10)
        
    def show_project_properties(self):
        """Показ свойств проекта"""
        dialog = ProjectPropertiesDialog(self.app)
        dialog.show()
        
    def update_project_info(self, project_name):
        """Обновление информации о проекте"""
        self.project_info_label.config(text=f"Проект: {project_name}")