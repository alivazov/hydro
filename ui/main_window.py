"""
Главное окно приложения
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from .tabs.calculations_tab import CalculationsTab
from .tabs.construction_tab import ConstructionTab
from .tabs.platforms_tab import PlatformsTab
from .tabs.capacity_tab import CapacityTab
from .tabs.balance_tab import BalanceTab
from .dialogs.project_properties import ProjectPropertiesDialog
from utils.exporters import WordExporter

class MainWindow:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.create_menu()
        self.create_toolbar()
        self.create_notebook()
        self.create_tabs()
        self.update_recent_menu()
        
    def create_menu(self):
        """Создание главного меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый проект", command=self.app.project_manager.new_project)
        file_menu.add_command(label="Открыть...", command=self.app.project_manager.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить", command=self.app.project_manager.save_project)
        file_menu.add_command(label="Сохранить как...", command=self.app.project_manager.save_project_as)
        file_menu.add_separator()
        
        # Подменю "Недавние проекты"
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Недавние проекты", menu=self.recent_menu)
        
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.app.exit_app)
        
        # Меню Проект
        project_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Проект", menu=project_menu)
        project_menu.add_command(label="Свойства проекта", command=self.show_project_properties)
        project_menu.add_separator()
        project_menu.add_command(label="Экспорт в Word", command=self.export_to_word)
        project_menu.add_command(label="Экспорт в PDF")
        project_menu.add_command(label="Экспорт в Excel")
        
    def show_project_properties(self):
        """Показ диалога свойств проекта"""
        dialog = ProjectPropertiesDialog(self.app)
        dialog.show()
        
    def export_to_word(self):
        """Экспорт проекта в Word"""
        try:
            exporter = WordExporter(self.app)
            success = exporter.export_to_word()
            
            if success:
                messagebox.showinfo("Успех", "Проект успешно экспортирован в Word")
            else:
                messagebox.showwarning("Предупреждение", "Экспорт в Word не выполнен")
                
        except ImportError as e:
            messagebox.showerror("Ошибка", 
                f"Не удалось выполнить экспорт в Word:\n{str(e)}\n\n"
                f"Установите библиотеку python-docx:\n"
                f"pip install python-docx")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить экспорт в Word:\n{str(e)}")
        
    def show_project_properties(self):
        """Показ диалога свойств проекта"""
        dialog = ProjectPropertiesDialog(self.app)
        dialog.show()

    def update_recent_menu(self):
        """Обновление меню недавних проектов"""
        self.recent_menu.delete(0, tk.END)
        
        recent_projects = self.app.settings_manager.get_recent_projects()
        
        if recent_projects:
            for file_path in recent_projects:
                if os.path.exists(file_path):
                    display_name = os.path.basename(file_path)
                    self.recent_menu.add_command(
                        label=display_name,
                        command=lambda fp=file_path: self.load_recent_project(fp)
                    )
            self.recent_menu.add_separator()
            self.recent_menu.add_command(label="Очистить список", command=self.clear_recent_projects)
        else:
            self.recent_menu.add_command(label="Нет недавних проектов", state="disabled")
            
    def load_recent_project(self, file_path):
        """Загрузка проекта из списка недавних"""
        if os.path.exists(file_path):
            self.app.project_manager.load_project(file_path)
        else:
            messagebox.showwarning("Файл не найден", f"Файл не существует: {file_path}")
            # Удаляем из списка недавних
            self.app.settings_manager.remove_recent_project(file_path)
            self.update_recent_menu()
            
    def clear_recent_projects(self):
        """Очистка списка недавних проектов"""
        self.app.settings_manager.settings['recent_projects'] = []
        self.app.settings_manager.save_settings()
        self.update_recent_menu()
        
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Новый проект", 
                  command=self.app.project_manager.new_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Сохранить", 
                  command=self.app.project_manager.save_project).pack(side=tk.LEFT, padx=5)
        
        # Информация о проекте
        self.project_info_label = ttk.Label(toolbar, text="Проект: Новый проект")
        self.project_info_label.pack(side=tk.RIGHT, padx=10)
        
    def create_notebook(self):
        """Создание блока с вкладками"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_tabs(self):
        """Создание всех вкладок"""
        self.calculations_tab = CalculationsTab(self.notebook, self.app)
        self.construction_tab = ConstructionTab(self.notebook, self.app)
        self.platforms_tab = PlatformsTab(self.notebook, self.app)
        self.capacity_tab = CapacityTab(self.notebook, self.app)
        self.balance_tab = BalanceTab(self.notebook, self.app)
        
        # Добавление вкладок в notebook
        self.notebook.add(self.calculations_tab.frame, text="Основные расчеты")
        self.notebook.add(self.balance_tab.frame, text="Баланс")
        self.notebook.add(self.construction_tab.frame, text="Этапы строительства")
        self.notebook.add(self.platforms_tab.frame, text="Таблица площадок")
        self.notebook.add(self.capacity_tab.frame, text="Проверка пропускной способности")

        
    def update_project_info(self):
        """Обновление информации о проекте"""
        project = self.app.project_manager.current_project
        name = project.name
        
        # Если есть file_path, используем имя файла
        if project.file_path:
            name = os.path.basename(project.file_path)
        
        title = f"Гидравлический калькулятор - {name}"
        if project.is_modified:
            title += " *"
            
        self.root.title(title)
        self.project_info_label.config(text=f"Проект: {name}")