"""
Контекстные меню для таблиц с восстановленной логикой для столбца platform
"""

import tkinter as tk
from tkinter import ttk
from ui.dialogs.cell_editor import CellEditor
from ui.dialogs.selection_dialog import SelectionDialog

class ColumnContextMenu:
    def __init__(self, app, tree):
        self.app = app
        self.tree = tree
        self.selected_cell = None
        self.create_menus()
        
    def create_menus(self):
        """Создание разных меню для разных столбцов"""
        # Меню для столбца "Обоснование"
        self.justification_menu = tk.Menu(self.app.root, tearoff=0)
        self.justification_menu.add_command(label="Баланс", command=lambda: self.set_cell_value("Баланс"))
        self.justification_menu.add_command(label="Сущ.пол", command=lambda: self.set_cell_value("Сущ.пол"))
        self.justification_menu.add_command(label="1850ДП-К", command=lambda: self.set_cell_value("1850ДП-К"))
        self.justification_menu.add_command(label="2086ДП-К", command=lambda: self.set_cell_value("2086ДП-К"))
        self.justification_menu.add_command(label="Проект", command=lambda: self.set_cell_value("Проект"))
        self.justification_menu.add_separator()
        self.justification_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        
        # Меню для столбца "№ пл." (номер площадки)
        self.platform_menu = tk.Menu(self.app.root, tearoff=0)
        for i in range(1, 11):
            self.platform_menu.add_command(label=str(i), command=lambda x=i: self.set_cell_value(str(x)))
        self.platform_menu.add_separator()
        self.platform_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        
        # Меню для столбца "№ эт." (номер этапа)
        self.phase_menu = tk.Menu(self.app.root, tearoff=0)
        for i in range(1, 6):
            self.phase_menu.add_command(label=str(i), command=lambda x=i: self.set_cell_value(str(x)))
        self.phase_menu.add_separator()
        self.phase_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        
        # Меню для столбца "platform" в таблице пропускной способности - ОСОБОЕ МЕНЮ
        self.platform_selection_menu = tk.Menu(self.app.root, tearoff=0)
        self.platform_selection_menu.add_command(label="Выбрать площадки/интервалы...", command=self.open_platform_selection)
        self.platform_selection_menu.add_separator()
        self.platform_selection_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        self.platform_selection_menu.add_command(label="Очистить", command=lambda: self.set_cell_value(""))
        
        # Меню для столбцов с расходами (общий режим редактирования)
        self.calculation_menu = tk.Menu(self.app.root, tearoff=0)
        self.calculation_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        self.calculation_menu.add_command(label="Очистить", command=lambda: self.set_cell_value(""))
        
        # Меню для столбца "Диаметр" в таблице пропускной способности
        self.diameter_menu = tk.Menu(self.app.root, tearoff=0)
        diameters = ["100", "150", "200", "250", "300", "350", "400", "450", "500"]
        for diameter in diameters:
            self.diameter_menu.add_command(
                label=diameter, 
                command=lambda d=diameter: self.set_cell_value(d)
            )
        self.diameter_menu.add_separator()
        self.diameter_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        
        # Меню для столбца "Уклон" в таблице пропускной способности
        self.slope_menu = tk.Menu(self.app.root, tearoff=0)
        slopes = ["0.001", "0.002", "0.003", "0.004", "0.005", "0.006", "0.007", "0.008", "0.009", "0.01"]
        for slope in slopes:
            self.slope_menu.add_command(
                label=slope, 
                command=lambda s=slope: self.set_cell_value(s)
            )
        self.slope_menu.add_separator()
        self.slope_menu.add_command(label="Редактировать", command=self.edit_selected_cell)
        
    def show(self, event):
        """Показ соответствующего меню для столбца"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            column_name = self.tree.heading(column)["text"]
            
            self.selected_cell = (row, column)
            
            # ОСОБАЯ ЛОГИКА: для столбца platform в CapacityTab открываем диалог выбора
            if (self.is_capacity_tab_platform_column(column_name, column) and 
                hasattr(self.tree, 'master') and 
                hasattr(self.tree.master, 'open_selection_window')):
                
                # Открываем окно выбора вместо показа меню
                self.tree.master.open_selection_window(event)
                return
            
            # Выбираем меню в зависимости от столбца
            menu = self.get_menu_for_column(column_name, column)
            
            if menu:
                try:
                    menu.tk_popup(event.x_root, event.y_root)
                finally:
                    menu.grab_release()
                    
    def is_capacity_tab_platform_column(self, column_name, column):
        """Проверяет, является ли это столбцом platform в таблице пропускной способности"""
        if not hasattr(self.tree, 'master'):
            return False
            
        # Проверяем, что это вкладка CapacityTab
        if hasattr(self.tree.master, '__class__'):
            tab_class_name = self.tree.master.__class__.__name__
            if tab_class_name == 'CapacityTab':
                # Проверяем название столбца и его позицию
                column_name_lower = column_name.lower()
                if (any(word in column_name_lower for word in ['пл./инт', 'platform', 'площадк']) or 
                    column == "#3"):  # Третий столбец
                    return True
        return False
                    
    def get_menu_for_column(self, column_name, column):
        """Возвращает соответствующее меню для столбца"""
        column_name_lower = column_name.lower()
        
        # ОСОБЫЙ СЛУЧАЙ: для столбца platform в CapacityTab - специальное меню
        if (self.is_capacity_tab_platform_column(column_name, column) and 
            hasattr(self, 'platform_selection_menu')):
            return self.platform_selection_menu
        
        if any(word in column_name_lower for word in ['обоснование', 'тип', 'вид']):
            return self.justification_menu
        elif any(word in column_name_lower for word in ['№ пл', 'площадк', 'platform']) and not self.is_capacity_tab_platform_column(column_name, column):
            return self.platform_menu
        elif any(word in column_name_lower for word in ['№ эт', 'этап', 'phase']):
            return self.phase_menu
        elif any(word in column_name_lower for word in ['диаметр', 'diametr']):
            return self.diameter_menu
        elif any(word in column_name_lower for word in ['уклон', 'slope', 'i_uklon']):
            return self.slope_menu
        elif any(word in column_name_lower for word in ['расход', '%', 'коэффициент', 'наполнение', 'скорость']):
            return self.calculation_menu
        else:
            # Меню по умолчанию
            return self.calculation_menu
            
    def open_platform_selection(self):
        """Открытие диалога выбора площадок и интервалов"""
        if self.selected_cell:
            row, column = self.selected_cell
            # Создаем событие для эмуляции правого клика
            class MockEvent:
                def __init__(self, x_root, y_root):
                    self.x_root = x_root
                    self.y_root = y_root
            
            # Получаем координаты для позиционирования
            if hasattr(self.tree, 'master') and hasattr(self.tree.master, 'open_selection_window'):
                # Используем существующий метод открытия диалога
                self.tree.master.open_selection_window(MockEvent(100, 100))
            else:
                # Альтернатива: открываем диалог напрямую
                dialog = SelectionDialog(self.app, row, column, self.tree)
                dialog.show()
            
    def set_cell_value(self, value):
        """Установка значения в выбранную ячейку"""
        if self.selected_cell:
            row, column = self.selected_cell
            item = self.tree.item(row)
            values = list(item['values'])
            col_idx = int(column[1:]) - 1
            
            # Убеждаемся, что values достаточно длинный
            while len(values) <= col_idx:
                values.append("")
                
            values[col_idx] = value
            self.tree.item(row, values=values)
            
            # Обновляем связанные расчеты
            self.update_related_calculations(row, column, value)
            
    def update_related_calculations(self, row, column, value):
        """Обновление связанных расчетов при изменении ячейки"""
        # Если изменились данные в балансе, обновляем связанные таблицы
        if hasattr(self.tree, 'master') and hasattr(self.tree.master, '__class__'):
            tab_class = self.tree.master.__class__.__name__
            
            if tab_class == 'BalanceTab':
                self.update_balance_calculations(row, column, value)
            elif tab_class == 'CapacityTab':
                self.update_capacity_calculations(row, column, value)
                
    def update_balance_calculations(self, row, column, value):
        """Обновление расчетов в балансе"""
        item = self.tree.item(row)
        values = list(item['values'])
        col_idx = int(column[1:]) - 1
        
        # Если изменились q_day или percent_q, пересчитываем percent_result
        if col_idx in (5, 6):  # Индексы q_day и percent_q
            try:
                q_day = float(values[5]) if values[5] else 0
                percent = float(values[6]) if values[6] else 0
                values[7] = f"{q_day * percent / 100:.2f}"
                self.tree.item(row, values=values)
            except (ValueError, IndexError):
                pass
                
    def update_capacity_calculations(self, row, column, value):
        """Обновление расчетов в таблице пропускной способности"""
        item = self.tree.item(row)
        values = list(item['values'])
        col_idx = int(column[1:]) - 1
        
        # Если изменился диаметр или уклон, пересчитываем наполнение и скорость
        if col_idx in (7, 8) and values[6]:  # diametr, i_uklon
            try:
                from functions import filling_speed
                d = float(values[7]) if values[7] else 0
                i = float(values[8]) if values[8] else 0
                q_calc = float(values[6]) if values[6] else 0
                
                if d > 0 and i > 0 and q_calc > 0:
                    h_d_relative, v_final = filling_speed(Q=q_calc, d=d, i=i, n=0.014)
                    values[9] = f"{h_d_relative:.2f}"
                    values[10] = f"{v_final:.2f}"
                    self.tree.item(row, values=values)
            except (ValueError, IndexError):
                pass
                
    def edit_selected_cell(self):
        """Редактирование выбранной ячейки"""
        if self.selected_cell:
            row, column = self.selected_cell
            editor = CellEditor(self.app, self.tree, row, column)
            editor.show()