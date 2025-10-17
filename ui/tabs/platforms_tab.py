"""
Вкладка таблицы площадок (tab2)
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab
from functions import calculate_lit_per_sec


class PlatformsTab(BaseTab):
    def create_widgets(self):
        # Создание фрейма для таблицы
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        # Создание Treeview
        columns = ("#", "name", "ave_sec", "sec_ave", "coeffic", "sec_expen")
        self.tree = ttk.Treeview(
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
            "name": "Наименование",
            "ave_sec": "Среднесуточный расход, \nм3/сут",
            "sec_ave": "Средне-секундный расход,\nл/сек",
            "coeffic": "Коэффициент \nнеравномерности",
            "sec_expen": "Секундный расчетный расход,\nл/сек"
        }
        widths = {
            "#": 50,
            "name": 300,
            "ave_sec": 150,
            "sec_ave": 150,
            "coeffic": 150,
            "sec_expen": 150
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Размещение
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Кнопки
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            btn_frame, 
            text="Обновить данные", 
            command=self.update_data
        ).pack(side=tk.RIGHT, padx=5)
        
    def get_balance_data(self):
        """Получение данных из вкладки баланса"""
        balance_tab = self.app.main_window.balance_tab
        if balance_tab:
            return balance_tab.get_data()
        return []
        
    def update_data(self):
        """Обновление данных из баланса"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        balance_data = self.get_balance_data()
        if not balance_data:
            return

        # Группируем данные по площадкам
        platforms = {}
        for values in balance_data:
            try:
                if len(values) >= 8:
                    q_day = float(values[5]) if values[5] else 0.0  # Общий расход
                    percent = float(values[6]) if values[6] else 0.0  # %
                    platform = values[2]  # № пл.
                    name = values[4]  # Наименование
                    
                    if platform not in platforms:
                        platforms[platform] = {
                            "names": [],
                            "total_q_day": 0.0,
                            "total_percent": 0.0
                        }
                    platforms[platform]["names"].append(name)
                    platforms[platform]["total_q_day"] += q_day
                    platforms[platform]["total_percent"] += percent
            except (ValueError, IndexError):
                continue

        # Сортируем площадки
        platforms = dict(sorted(platforms.items()))
        
        # Добавляем данные в таблицу
        for i, (platform, data) in enumerate(platforms.items(), start=1):
            q_sec = data["total_q_day"] / 86.4
            q_lit_per_sec, k = calculate_lit_per_sec(data["total_q_day"])
            
            self.tree.insert("", tk.END, values=(
                i,  # №
                f"{' + '.join(data['names'])}",  # Наименование
                f"{data['total_q_day']:.2f}",  # Среднесуточный расход
                f"{q_sec:.2f}", # Средне-секундный расход
                f"{k:.2f}",  # Коэффициент неравномерности
                f"{q_lit_per_sec:.2f}"  # Секундный расход
            ))
        
    def get_data(self):
        return [self.tree.item(item, 'values') for item in self.tree.get_children()]
        
    def set_data(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            self.tree.insert("", tk.END, values=row)