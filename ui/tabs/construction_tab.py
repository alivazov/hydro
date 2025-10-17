"""
Вкладка этапов строительства (tab1)
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab

class ConstructionTab(BaseTab):
    def create_widgets(self):
        # Создание таблицы
        columns = ("name", "q_day", "q_mid")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        
        headings = {
            "name": "Наименование потребителя (Хоз.-быт. канализация)",
            "q_day": "Qсут, м3/сут",
            "q_mid": "qср, л/с"
        }
        widths = {"name": 500, "q_day": 100, "q_mid": 100}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

        # Прокрутка
        scroll_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Кнопки
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Button(
            btn_frame,
            text="Обновить данные",
            command=self.update_data
        ).pack(side=tk.RIGHT, padx=5)

        # Настройка весов
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
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

        # Обработка данных как в оригинальном коде
        tab4_data = []
        for values in balance_data:
            try:
                if len(values) >= 6:
                    q_mid = float(values[5]) / 86.4  # q_day -> q_mid
                    tab4_data.append({
                        "number_phase": values[3],
                        "name": values[4],
                        "q_day": float(values[5]),
                        'q_mid': q_mid
                    })
            except (ValueError, IndexError):
                continue

        # Сортировка и группировка данных
        if not tab4_data:
            return
            
        sorted_data = sorted(tab4_data, key=lambda x: x['number_phase'])
        
        self.tree.insert("", tk.END, values=(
            "Проектируемая застройка",
            "",
            ""
        ))

        number_phase = 0
        q_d, q_s = 0, 0
        count = 0
        q_d_all = 0
        q_s_all = 0
        name = ''

        for item in sorted_data:
            count += 1
            if name != item['name']:
                name = item['name']
                q_d_all += item["q_day"]
                q_s_all += item["q_mid"]
                if number_phase != item["number_phase"] and number_phase != 0:
                    self.tree.insert("", tk.END, values=(
                        f"Итого по {number_phase} этапу строительства",
                        q_d,
                        f"{q_s:.2f}"
                    ))
                    q_d, q_s = item["q_day"], item["q_mid"]
                else:
                    q_d += item["q_day"]
                    q_s += item["q_mid"]
                    
                if number_phase != item["number_phase"]:                   
                    self.tree.insert("", tk.END, values=(
                        f"{item['number_phase']} этап строительства.",
                        " ",
                        " "
                    ))

                self.tree.insert("", tk.END, values=(
                    f"{item['name']}",
                    f"{item['q_day']}",
                    f"{item['q_mid']:.2f}"
                ))
                number_phase = item["number_phase"]
                
            if count == len(sorted_data):
                self.tree.insert("", tk.END, values=(
                    f"Итого по {number_phase} этапу строительства",
                    q_d,
                    f"{q_s:.2f}"
                ))

        self.tree.insert("", tk.END, values=(
            "ИТОГО ПО ПРОЕКТУ:",
            q_d_all,
            f"{q_s_all:.2f}"
        ))
        
    def get_data(self):
        """Получение данных таблицы"""
        return [self.tree.item(item, 'values') for item in self.tree.get_children()]
        
    def set_data(self, data):
        """Установка данных в таблицу"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in data:
            self.tree.insert("", tk.END, values=row)