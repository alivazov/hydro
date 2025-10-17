"""
Диалоговое окно свойств проекта
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ProjectPropertiesDialog:
    def __init__(self, app):
        self.app = app
        self.project = app.project_manager.current_project
        
    def show(self):
        """Показ диалога свойств проекта"""
        self.dialog = tk.Toplevel(self.app.root)
        self.dialog.title("Свойства проекта")
        self.dialog.geometry("500x430")
        self.dialog.transient(self.app.root)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Центрирование
        self.dialog.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - self.dialog.winfo_width()) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.create_widgets()
        self.load_project_data()
        self.setup_bindings()
        
    def create_widgets(self):
        """Создание виджетов диалога"""
        # Основной фрейм
        main_frame = ttk.Frame(self.dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Свойства проекта", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Наименование проекта
        ttk.Label(main_frame, text="Наименование проекта:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40, font=("Arial", 10))
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Описание проекта
        ttk.Label(main_frame, text="Описание:").grid(row=2, column=0, sticky="nw", pady=5)
        self.desc_text = tk.Text(main_frame, width=40, height=6, font=("Arial", 10))
        self.desc_text.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Информация о проекте (только для чтения)
        info_frame = ttk.LabelFrame(main_frame, text="Информация о проекте", padding=10)
        info_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=15)
        
        # Дата создания
        ttk.Label(info_frame, text="Дата создания:").grid(row=0, column=0, sticky="w", pady=2)
        self.created_label = ttk.Label(info_frame, text="")
        self.created_label.grid(row=0, column=1, sticky="w", pady=2, padx=(10, 0))
        
        # Дата изменения
        ttk.Label(info_frame, text="Дата изменения:").grid(row=1, column=0, sticky="w", pady=2)
        self.modified_label = ttk.Label(info_frame, text="")
        self.modified_label.grid(row=1, column=1, sticky="w", pady=2, padx=(10, 0))
        
        # Версия
        ttk.Label(info_frame, text="Версия:").grid(row=2, column=0, sticky="w", pady=2)
        self.version_label = ttk.Label(info_frame, text="")
        self.version_label.grid(row=2, column=1, sticky="w", pady=2, padx=(10, 0))
        
        # Путь к файлу
        ttk.Label(info_frame, text="Файл:").grid(row=3, column=0, sticky="w", pady=2)
        self.file_label = ttk.Label(info_frame, text="", wraplength=300)
        self.file_label.grid(row=3, column=1, sticky="w", pady=2, padx=(10, 0))
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Сохранить", 
                  command=self.save_properties, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", 
                  command=self.dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # Настройка весов для растягивания
        main_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(1, weight=1)
        
    def load_project_data(self):
        """Загрузка данных проекта в форму"""
        # Наименование
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.project.name)
        
        # Описание
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(1.0, self.project.metadata.description or "")
        
        # Информация
        self.created_label.config(text=self.project.metadata.created_date or "Не указана")
        self.modified_label.config(text=self.project.metadata.modified_date or "Не указана")
        self.version_label.config(text=self.project.metadata.version or "1.0")
        
        file_path = self.project.file_path or "Проект не сохранен"
        self.file_label.config(text=file_path)
        
    def setup_bindings(self):
        """Настройка привязок клавиш"""
        self.dialog.bind("<Return>", lambda e: self.save_properties())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        self.name_entry.focus_set()
        
    def save_properties(self):
        """Сохранение свойств проекта"""
        try:
            # Получаем данные из формы
            name = self.name_entry.get().strip()
            description = self.desc_text.get(1.0, tk.END).strip()
            
            # Валидация
            if not name:
                tk.messagebox.showwarning("Ошибка", "Наименование проекта не может быть пустым")
                self.name_entry.focus_set()
                return
            
            # Обновляем проект
            self.project.name = name
            self.project.metadata.description = description
            self.project.metadata.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.project.is_modified = True
            
            # Обновляем UI
            self.app.main_window.update_project_info()
            
            # Показываем сообщение
            tk.messagebox.showinfo("Успех", "Свойства проекта сохранены")
            
            # Закрываем диалог
            self.dialog.destroy()
            
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Не удалось сохранить свойства проекта: {str(e)}")