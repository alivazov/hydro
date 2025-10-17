"""
Диалог выбора интервалов и площадок
"""

import tkinter as tk
from tkinter import ttk
from functions import calculate_lit_per_sec, filling_speed

class SelectionDialog:
    def __init__(self, app, row, column, tree):
        self.app = app
        self.row = row
        self.column = column
        self.tree = tree
        
    def show(self):
        """Показ диалога выбора"""
        self.dialog = tk.Toplevel(self.app.root)
        self.dialog.title("Выбор интервалов и площадок")
        self.dialog.geometry("500x500")
        self.dialog.transient(self.app.root)
        self.dialog.grab_set()
        
        # Центрирование
        self.dialog.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - self.dialog.winfo_width()) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.create_widgets()
        self.setup_bindings()
        
    def get_platforms_data(self):
        """Получение данных площадок"""
        platforms_tab = self.app.main_window.platforms_tab
        if platforms_tab:
            return platforms_tab.get_data()
        return []
        
    def get_intervals_data(self):
        """Получение данных интервалов из таблицы 3"""
        capacity_tab = self.app.main_window.capacity_tab
        intervals = {}
        if capacity_tab and hasattr(capacity_tab, 'tree'):
            for item in capacity_tab.tree.get_children():
                values = capacity_tab.tree.item(item, 'values')
                if values and len(values) > 1 and values[1]:  # values[1] - интервал
                    interval_name = values[1]
                    # Получаем расход для интервала (values[3] - q_day)
                    try:
                        q_day = float(values[3]) if values[3] else 0
                        intervals[interval_name] = q_day
                    except (ValueError, IndexError):
                        intervals[interval_name] = 0
        return intervals
        
    def create_widgets(self):
        """Создание виджетов диалога"""
        # Фрейм для интервалов
        intervals_frame = ttk.LabelFrame(self.dialog, text="Интервалы", padding=10)
        intervals_frame.pack(fill=tk.X, padx=10, pady=5)

        # Получаем данные интервалов
        self.interval_vars = {}
        intervals_data = self.get_intervals_data()
        
        for interval_name, q_day in intervals_data.items():
            var = tk.BooleanVar()
            self.interval_vars[interval_name] = var
            label_text = f"{interval_name} ({q_day:.2f} м3/сут)" if q_day > 0 else interval_name
            cb = ttk.Checkbutton(intervals_frame, text=label_text, variable=var)
            cb.pack(anchor=tk.W, pady=2)
        
        # Фрейм для площадок с прокруткой
        platforms_frame = ttk.LabelFrame(self.dialog, text="Площадки", padding=10)
        platforms_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем canvas для прокрутки
        platform_canvas = tk.Canvas(platforms_frame)
        scrollbar = ttk.Scrollbar(platforms_frame, orient=tk.VERTICAL, command=platform_canvas.yview)
        scrollable_frame = ttk.Frame(platform_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: platform_canvas.configure(scrollregion=platform_canvas.bbox("all"))
        )
        
        platform_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        platform_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Получаем данные площадок
        self.platform_vars = {}
        platforms_data = self.get_platforms_data()
        
        for platform_data in platforms_data:
            if len(platform_data) >= 3:
                platform_num = platform_data[0]
                q_day = float(platform_data[2]) if platform_data[2] else 0  # Среднесуточный расход
                var = tk.BooleanVar()
                self.platform_vars[f"п.{platform_num}"] = (var, q_day)
                label_text = f"п.{platform_num} ({q_day:.2f} м3/сут)" if q_day > 0 else f"п.{platform_num}"
                cb = ttk.Checkbutton(scrollable_frame, text=label_text, variable=var)
                cb.pack(anchor=tk.W, pady=2)
        
        platform_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Применить", command=self.apply_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def setup_bindings(self):
        """Настройка привязок клавиш"""
        self.dialog.bind("<Return>", lambda e: self.apply_selection())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        
    def apply_selection(self):
        """Применение выбора"""
        selected_items = []
        
        # Добавляем выбранные интервалы
        for interval, var in self.interval_vars.items():
            if var.get():
                selected_items.append(interval)
                
        # Добавляем выбранные площадки
        for platform, (var, q_day) in self.platform_vars.items():
            if var.get():
                selected_items.append(platform)
                
        # Формируем строку результата
        result = " + ".join(selected_items) if selected_items else ""
        
        # Обновляем ячейку в таблице
        item = self.tree.item(self.row)
        values = list(item['values'])
        
        while len(values) < 11:  # Максимальное количество столбцов
            values.append("")
            
        values[2] = result  # Столбец platform
        
        # Рассчитываем суммарный расход
        total_q_day = self.calculate_total_flow(selected_items)
        values[3] = f"{total_q_day:.2f}" if total_q_day > 0 else ""
        
        # Пересчитываем остальные значения
        self.update_calculated_values(values, total_q_day)
        
        self.tree.item(self.row, values=values)
        self.dialog.destroy()
        
    def calculate_total_flow(self, selected_items):
        """Расчет суммарного расхода для выбранных площадок и интервалов"""
        total = 0.0
        
        # Получаем данные площадок
        platforms_data = self.get_platforms_data()
        platform_dict = {}
        for platform_data in platforms_data:
            if len(platform_data) >= 3:
                platform_dict[f"п.{platform_data[0]}"] = float(platform_data[2]) if platform_data[2] else 0
        
        # Получаем данные интервалов
        intervals_data = self.get_intervals_data()
        
        # Суммируем выбранные элементы
        for item in selected_items:
            if item in platform_dict:
                # Это площадка
                total += platform_dict[item]
            elif item in intervals_data:
                # Это интервал
                total += intervals_data[item]
        
        return total
        
    def update_calculated_values(self, values, total_q_day):
        """Обновление расчетных значений"""
        if total_q_day > 0:
            # Расчет средне-секундного расхода
            q_sec = total_q_day / 86.4
            values[4] = f"{q_sec:.2f}"
            
            # Расчет коэффициента неравномерности
            q_lit_per_sec, k = calculate_lit_per_sec(total_q_day)
            values[5] = f"{k:.2f}"
            values[6] = f"{q_sec * k:.2f}"
            
            # Если есть диаметр и уклон, пересчитываем наполнение и скорость
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