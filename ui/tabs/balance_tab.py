"""
Вкладка баланса водопотребления и водоотведения (tab4)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_tab import BaseTab
from ui.dialogs.cell_editor import CellEditor
from ui.widgets.context_menus import ColumnContextMenu

class BalanceTab(BaseTab):

    def create_widgets(self):
        # Создание фрейма для таблицы
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создание Treeview с прокруткой
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        columns = ("#", "justification", "number_platform", "number_phase", 
                  "name", "q_day", "percent_q", "percent_result")
        
        self.balance_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=10
        )
        
        # Настройка колонок
        headings = {
            "#": "№",
            "justification": "Обоснование",
            "number_platform": "№ пл.",
            "number_phase": "№ эт.",
            "name": "Наименование",
            "q_day": "Общий расход",
            "percent_q": "%",
            "percent_result": "Итог %",
        }
        
        widths = {
            "#": 40,
            "justification": 150,
            "number_platform": 60,
            "number_phase": 60,
            "name": 250,
            "q_day": 80,
            "percent_q": 60,
            "percent_result": 60,
        }
        
        for col in columns:
            self.balance_tree.heading(col, text=headings[col])
            self.balance_tree.column(col, width=widths[col], anchor=tk.CENTER)
        
        scroll_y.config(command=self.balance_tree.yview)
        scroll_x.config(command=self.balance_tree.xview)
        
        self.balance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Контекстное меню
        self.context_menu = ColumnContextMenu(self.app, self.balance_tree)
        self.balance_tree.bind("<Button-3>", self.context_menu.show)
        self.balance_tree.bind("<Double-1>", self.edit_cell)
        
        # Форма ввода данных
        self.create_input_form()
        
        # Кнопки управления
        self.create_buttons()
        
    def create_input_form(self):
        """Создание формы ввода данных"""
        self.form_frame = ttk.LabelFrame(self.frame, text="Добавить/Редактировать данные", padding=10)
        self.form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Обоснование:").grid(row=0, column=0, sticky=tk.W)
        self.justification_entry = ttk.Entry(self.form_frame, width=30)
        self.justification_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(self.form_frame, text="№ пл.:").grid(row=0, column=2, sticky=tk.W)
        self.platform_entry = ttk.Entry(self.form_frame, width=10)
        self.platform_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(self.form_frame, text="№ эт.:").grid(row=0, column=4, sticky=tk.W)
        self.phase_entry = ttk.Entry(self.form_frame, width=10)
        self.phase_entry.grid(row=0, column=5, padx=5, pady=2)
        
        ttk.Label(self.form_frame, text="Наименование:").grid(row=1, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(self.form_frame, width=30)
        self.name_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(self.form_frame, text="Общий расход:").grid(row=1, column=2, sticky=tk.W)
        self.q_day_entry = ttk.Entry(self.form_frame, width=10)
        self.q_day_entry.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(self.form_frame, text="%:").grid(row=1, column=4, sticky=tk.W)
        self.percent_q_entry = ttk.Entry(self.form_frame, width=10)
        self.percent_q_entry.grid(row=1, column=5, padx=5, pady=2)

    def create_buttons(self):
        """Создание кнопок управления"""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            button_frame, 
            text="Загрузить тестовые данные", 
            command=self.load_test_data
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame, 
            text="Добавить запись", 
            command=self.add_record
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame, 
            text="Удалить выбранное", 
            command=self.delete_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Очистить таблицу", 
            command=self.clear_table
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Рассчитать итоги", 
            command=self.calculate_totals
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame, 
            text="Дублировать строку", 
            command=self.duplicate_selected
        ).pack(side=tk.LEFT, padx=5)
        
    def add_record(self):
        """Добавление новой записи"""
        try:
            justification = self.justification_entry.get()
            platform = self.platform_entry.get()
            phase = self.phase_entry.get()
            name = self.name_entry.get()
            q_day = self.q_day_entry.get()
            percent_q = self.percent_q_entry.get()
            
            if not name:
                messagebox.showwarning("Ошибка", "Поле 'Наименование' обязательно")
                return
                
            record_num = len(self.balance_tree.get_children()) + 1
            
            # Расчет итогового процента
            percent_result = ""
            if q_day and percent_q:
                try:
                    total = float(q_day)
                    percent = float(percent_q)
                    percent_result = f"{(total * percent / 100):.2f}"
                except ValueError:
                    pass
            
            self.balance_tree.insert("", tk.END, values=(
                record_num, justification, platform, phase, name, 
                q_day, percent_q, percent_result
            ))
            
            self.clear_form()
             
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись: {str(e)}")
            
    def edit_cell(self, event):
        """Редактирование ячейки по двойному клику"""
        region = self.balance_tree.identify("region", event.x, event.y)
        if region == "cell":
            row = self.balance_tree.identify_row(event.y)
            column = self.balance_tree.identify_column(event.x)
            self.edit_cell_dialog(row, column)

    def edit_cell_dialog(self, row, column):
        """Открытие диалога редактирования ячейки"""
        editor = CellEditor(self.app, self.balance_tree, row, column)
        editor.show()
        
    def delete_selected(self):
        """Удаление выбранной строки"""
        selected = self.balance_tree.selection()
        if selected:
            self.balance_tree.delete(selected)
            self.renumber_rows()
            
    def clear_table(self):
        """Очистка таблицы"""
        for item in self.balance_tree.get_children():
            self.balance_tree.delete(item)
            
    def calculate_totals(self):
        """Расчет общих итогов"""
        total_q = 0.0
        for item in self.balance_tree.get_children():
            values = self.balance_tree.item(item, 'values')
            try:
                total_q += float(values[5]) if values[5] else 0
            except ValueError:
                pass
        
        messagebox.showinfo("Итоги", f"Общий расход: {total_q:.2f} м3/сут")
        
    def duplicate_selected(self):
        """Дублирование выбранной строки"""
        selected = self.balance_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите строку для дублирования")
            return
        
        selected_item = selected[0]
        values = list(self.balance_tree.item(selected_item, 'values'))
        values[0] = ""  # Очищаем номер
        
        all_items = list(self.balance_tree.get_children())
        selected_index = all_items.index(selected_item)
        
        if selected_index + 1 < len(all_items):
            self.balance_tree.insert("", selected_index + 1, values=values)
        else:
            self.balance_tree.insert("", tk.END, values=values)
        
        self.renumber_rows()
        
    def renumber_rows(self):
        """Перенумерация строк"""
        for i, item in enumerate(self.balance_tree.get_children(), start=1):
            values = list(self.balance_tree.item(item, 'values'))
            if values:
                values[0] = i
                self.balance_tree.item(item, values=values)
                
    def clear_form(self):
        """Очистка формы ввода"""
        self.justification_entry.delete(0, tk.END)
        self.platform_entry.delete(0, tk.END)
        self.phase_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.q_day_entry.delete(0, tk.END)
        self.percent_q_entry.delete(0, tk.END)
        
    def load_test_data(self):
        """Загрузка тестовых данных"""
        self.clear_table()
        
        test_data = [
            (1, "Баланс", "3", "1", "Жилой дом", "150.5", "100", "15.05"),
            (2, "Баланс", "2", "2", "Офисное здание", "200.0", "100", "30.00"),
            (3, "1850ДП-К", "1", "1", "Торговый центр", "350.75", "100", "70.15"),
            (4, "2086ДП-К", "2", "2", "Кафе", "80.25", "100", "4.01"),
            (5, "Баланс", "3", "1", "Спортивный комплекс", "420.0", "100", "105.00")
        ]
        
        for data in test_data:
            self.balance_tree.insert("", tk.END, values=data)
        
        messagebox.showinfo("Тестовые данные", "Тестовые данные загружены!")
        
    def get_data(self):
        return [self.balance_tree.item(item, 'values') for item in self.balance_tree.get_children()]
        
    def set_data(self, data):
        self.clear_table()
        for row in data:
            self.balance_tree.insert("", tk.END, values=row)