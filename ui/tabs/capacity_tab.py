"""
Вкладка проверки пропускной способности (tab3)
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab
from functions import filling_speed, calculate_lit_per_sec
from ui.widgets.editable_treeview import EditableTreeview
from ui.dialogs.selection_dialog import SelectionDialog
from ui.widgets.context_menus import ColumnContextMenu

class CapacityTab(BaseTab):
    def create_widgets(self):
        columns = ("#", "interval", "platform", "q_day", "q_sec", "coeffic", "q_k_sec", 
                  "diametr", "i_uklon", "filling", "speed")

        # Создание редактируемой таблицы
        self.tree = EditableTreeview(
            self.frame, 
            columns=columns, 
            show="headings", 
            height=15,
            app=self.app
        )
        
        headings = {
            "#": "№",
            "interval": "Интервал",
            "platform": "№№ Пл./инт.",
            "q_day": "Ср. сут. расход, м3/сут",
            "q_sec": "Ср. сек. расход, л/сек",
            "coeffic": "К.неравн.",
            "q_k_sec": "Сек. расчетный расход, л/сек",
            "diametr": "Диаметр, мм",
            "i_uklon": "Уклон, i",
            "filling": "Наполнение, h/d",
            "speed": "Скорость, м/с"
        }
        widths = {col: 80 for col in columns}
        widths["#"] = 40
        widths["interval"] = 60
        widths["platform"] = 150
        widths["q_day"] = 120

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

        # Контекстное меню для столбцов
        self.context_menu = ColumnContextMenu(self.app, self.tree)
        self.tree.bind("<Button-3>", self.context_menu.show)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Прокрутка
        scroll_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Кнопки управления
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="Добавить строку", 
                  command=lambda: self.tree.add_row()).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить строку", 
                  command=lambda: self.tree.delete_selected()).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Обновить расчеты", 
                  command=self.update_calculations).pack(side=tk.LEFT, padx=5)

        # Настройка весов
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
    def on_double_click(self, event):
        """Обработка двойного клика"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            
            # Для столбца platform открываем диалог выбора
            if column == "#3":
                self.open_selection_window(event)
            else:
                # Для остальных столбцов - обычное редактирование
                row = self.tree.identify_row(event.y)
                self.context_menu.selected_cell = (row, column)
                self.context_menu.edit_selected_cell()
        
    def open_selection_window(self, event):
        """Открытие окна выбора интервалов и площадок"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            row = self.tree.identify_row(event.y)
            
            if column == "#3":  # Столбец platform
                dialog = SelectionDialog(self.app, row, column, self.tree)
                dialog.show()

    def get_intervals_data(self):
        """Получение данных интервалов из этой таблицы"""
        intervals = {}
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and len(values) > 1 and values[1]:  # values[1] - интервал
                interval_name = values[1]
                try:
                    q_day = float(values[3]) if values[3] else 0  # values[3] - q_day
                    intervals[interval_name] = q_day
                except (ValueError, IndexError):
                    intervals[interval_name] = 0
        return intervals

    def get_platforms_data(self):
        """Получение данных из вкладки площадок"""
        platforms_tab = self.app.main_window.platforms_tab
        if platforms_tab:
            return platforms_tab.get_data()
        return []
        
    def update_calculations(self):
        """Обновление всех расчетов в таблице"""
        # Получаем данные из таблицы площадок
        platforms_data = self.get_platforms_data()
        
        # Создаем словарь с данными площадок
        platform_dict = {}
        for values in platforms_data:
            if len(values) >= 3:
                platform_dict[f"п.{values[0]}"] = float(values[2]) if values[2] else 0

        # Обновляем каждую строку
        for item in self.tree.get_children():
            values = list(self.tree.item(item, 'values'))
            if len(values) >= 3:
                platform_str = values[2]  # Строка с площадками/интервалами
                if platform_str:
                    # Разбиваем строку на элементы
                    elements = platform_str.replace(" ", "").split('+')
                    total_q_day = 0

                    # Суммируем данные по всем площадкам
                    for elem in elements:
                        if elem in platform_dict:
                            total_q_day += platform_dict[elem]
                    
                    # Обновляем расчетные значения
                    values[3] = f"{total_q_day:.2f}" if total_q_day > 0 else ""
                    
                    if total_q_day > 0:
                        q_sec = total_q_day / 86.4
                        values[4] = f"{q_sec:.2f}"
                        
                        q, k_sec = calculate_lit_per_sec(total_q_day)
                        values[5] = f"{k_sec:.2f}"
                        values[6] = f"{q_sec * k_sec:.2f}"

                        # Пересчитываем наполнение и скорость если есть диаметр и уклон
                        if len(values) > 8 and values[7] and values[8]:
                            try:
                                Q = float(values[6])
                                d = float(values[7])
                                i = float(values[8])
                                h_d_relative, v_final = filling_speed(Q=Q, d=d, i=i, n=0.014)
                                values[9] = f"{h_d_relative:.2f}"
                                values[10] = f"{v_final:.2f}"
                            except (ValueError, IndexError):
                                values[9] = ""
                                values[10] = ""
                    
                    self.tree.item(item, values=values)
        
    def get_data(self):
        return self.tree.get_all_data()
        
    def set_data(self, data):
        self.tree.set_all_data(data)