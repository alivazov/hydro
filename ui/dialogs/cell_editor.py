"""
Диалоговое окно редактирования ячейки
"""

import tkinter as tk
from tkinter import ttk

class CellEditor:
    def __init__(self, app, tree, row, column):
        self.app = app
        self.tree = tree
        self.row = row
        self.column = column
        
        # Получаем данные ячейки
        item = self.tree.item(row)
        self.values = list(item['values'])
        self.col_idx = int(column[1:]) - 1
        self.current_value = self.values[self.col_idx] if self.col_idx < len(self.values) else ""
        self.column_name = self.tree.heading(column)["text"]
        
    def show(self):
        """Показ диалога редактирования"""
        self.dialog = tk.Toplevel(self.app.root)
        self.dialog.title(f"Редактирование: {self.column_name}")
        self.dialog.geometry("350x120")
        self.dialog.transient(self.app.root)
        self.dialog.grab_set()
        
        # Центрирование
        self.dialog.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - self.dialog.winfo_width()) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Создание элементов
        self.create_widgets()
        self.setup_bindings()
        
    def create_widgets(self):
        """Создание виджетов диалога"""
        ttk.Label(self.dialog, text="Новое значение:").pack(padx=10, pady=5)
        
        # Определяем тип поля ввода
        is_numeric = any(keyword in self.column_name.lower() for keyword in 
                        ['расход', '%', 'итог', 'коэффициент', 'уклон', 'скорость', 
                         'наполнение', 'диаметр', 'секундный'])
        
        if is_numeric:
            from utils.validators import validate_float
            vcmd = (self.dialog.register(validate_float), '%P')
            self.entry = ttk.Entry(self.dialog, width=30, validate="key", validatecommand=vcmd)
        else:
            self.entry = ttk.Entry(self.dialog, width=30)
            
        self.entry.pack(padx=10, pady=5)
        self.entry.insert(0, self.current_value)
        self.entry.select_range(0, tk.END)
        self.entry.focus_set()
        
        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def setup_bindings(self):
        """Настройка привязок клавиш"""
        self.dialog.bind("<Return>", lambda e: self.save())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        
    def save(self):
        """Сохранение изменений"""
        new_value = self.entry.get()
        
        # Обновляем значение в списке
        while len(self.values) <= self.col_idx:
            self.values.append("")
        self.values[self.col_idx] = new_value
        
        # Обновляем запись в таблице
        self.tree.item(self.row, values=self.values)
        
        # Обновляем связанные расчеты
        self.update_related_calculations()
        
        self.dialog.destroy()
        
    def update_related_calculations(self):
        """Обновление связанных расчетов"""
        # Определяем какая таблица редактируется и обновляем соответствующие данные
        if hasattr(self.tree, 'master') and hasattr(self.tree.master, 'update_calculations'):
            self.tree.master.update_calculations()