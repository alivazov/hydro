"""
Вкладка основных расчетов (tab0)
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab
from functions import filling_speed, calculate_lit_per_sec, MATERIAL

class CalculationsTab(BaseTab):
    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.frame, text="Диаметр трубы (м):").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_d = ttk.Entry(self.frame)
        self.entry_d.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.frame, text="Расход (л/с):").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_q = ttk.Entry(self.frame)
        self.entry_q.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self.frame, text="Уклон (м/м):").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_i = ttk.Entry(self.frame)
        self.entry_i.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(self.frame, text="Расход (м3/сут):").grid(row=1, column=3, sticky="e", pady=5)
        self.entry_q_day_per_m = ttk.Entry(self.frame)
        self.entry_q_day_per_m.grid(row=1, column=4, pady=5, padx=5)

        ttk.Label(self.frame, text="Материал трубы:").grid(row=3, column=0, sticky="e", pady=5)
        self.material_var = tk.StringVar()
        combobox = ttk.Combobox(self.frame, textvariable=self.material_var, 
                                values=[key for key in MATERIAL])
        combobox.grid(row=3, column=1, pady=5, padx=5)
        combobox.current(0)

        # Кнопки
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=4, column=0, columnspan=5, pady=10)
        
        ttk.Button(btn_frame, text="Рассчитать", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)

        # Поле результатов
        self.text_result = tk.Text(self.frame, height=6, width=60, font=("Courier New", 10))
        self.text_result.grid(row=5, column=0, columnspan=5, pady=10)
        self.text_result.insert(tk.END, "Результаты расчета появятся здесь...")
        
    def calculate(self):
        """Выполнение расчетов"""
        result_text = "Результаты:"

        try:
            d = int(self.entry_d.get())
            q = float(self.entry_q.get())
            i = float(self.entry_i.get())
            n = MATERIAL[self.material_var.get()]
            h, v = filling_speed(Q=q, d=d, i=i, n=n)
            result_text = result_text + f"\nНаполнение: {h:.4f} м\nСкорость: {v:.3f} м/c"
            self.text_result.delete(1.0, tk.END)
            self.text_result.insert(tk.END, result_text)
        except Exception as e:
            pass

        try:
            q_day_per_m = float(self.entry_q_day_per_m.get())
            q_l_per_s, k = calculate_lit_per_sec(q_day_per_m)

            result_text += f"\nРасход: {q_l_per_s:.3f} л/c, к.неравн: {k:.2f}"
            self.text_result.delete(1.0, tk.END)
            self.text_result.insert(tk.END, result_text)
        except Exception as e:
            pass
        
    def clear(self):
        self.entry_d.delete(0, tk.END)
        self.entry_q.delete(0, tk.END)
        self.entry_i.delete(0, tk.END)
        self.entry_q_day_per_m.delete(0, tk.END)
        self.text_result.delete(1.0, tk.END)
        self.text_result.insert(tk.END, "Результаты расчета появятся здесь...")