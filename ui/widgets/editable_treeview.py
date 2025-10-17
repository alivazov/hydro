"""
Кастомный Treeview с поддержкой редактирования
"""

import tkinter as tk
from tkinter import ttk
from ui.dialogs.cell_editor import CellEditor

class EditableTreeview(ttk.Treeview):
    def __init__(self, parent, columns, show='headings', height=15, app=None, **kwargs):
        super().__init__(parent, columns=columns, show=show, height=height, **kwargs)
        self.app = app
        self.setup_editing()
        
    def setup_editing(self):
        """Настройка редактирования двойным кликом"""
        self.bind("<Double-1>", self.on_double_click)
        
    def on_double_click(self, event):
        """Обработка двойного клика для редактирования"""
        region = self.identify("region", event.x, event.y)
        if region == "cell":
            column = self.identify_column(event.x)
            row = self.identify_row(event.y)
            
            # Открываем редактор ячейки
            editor = CellEditor(self.app, self, row, column)
            editor.show()
            
    def add_row(self):
        """Добавление новой строки"""
        values = [""] * len(self["columns"])
        if values:
            values[0] = len(self.get_children()) + 1
        self.insert("", tk.END, values=values)
        
    def delete_selected(self):
        """Удаление выбранных строк"""
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)
        self.renumber_rows()
        
    def renumber_rows(self):
        """Перенумерация строк"""
        for i, item in enumerate(self.get_children(), start=1):
            values = list(self.item(item, 'values'))
            if values:
                values[0] = i
                self.item(item, values=values)
                
    def get_all_data(self):
        """Получение всех данных таблицы"""
        return [self.item(item, 'values') for item in self.get_children()]
        
    def set_all_data(self, data):
        """Установка всех данных таблицы"""
        for item in self.get_children():
            self.delete(item)
        for row in data:
            self.insert("", tk.END, values=row)