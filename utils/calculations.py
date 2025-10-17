"""
Дополнительные расчетные функции
"""

from functions import filling_speed, calculate_lit_per_sec

def calculate_platform_totals(balance_data):
    """Расчет суммарных данных по площадкам"""
    platforms = {}
    
    for item in balance_data:
        if len(item) >= 8:
            platform = item[2]  # № пл.
            name = item[4]      # Наименование
            q_day = float(item[5]) if item[5] else 0.0
            percent = float(item[6]) if item[6] else 0.0
            
            if platform not in platforms:
                platforms[platform] = {
                    "names": [],
                    "total_q_day": 0.0,
                    "total_percent": 0.0
                }
                
            platforms[platform]["names"].append(name)
            platforms[platform]["total_q_day"] += q_day
            platforms[platform]["total_percent"] += percent
            
    return platforms

def update_capacity_calculations(values):
    """Обновление расчетов для таблицы пропускной способности"""
    try:
        if len(values) >= 7:
            # Расчет средне-секундного расхода
            q_day = float(values[3]) if values[3] else 0
            q_sec = q_day / 86.4
            values[4] = f"{q_sec:.2f}"
            
            # Расчет коэффициента неравномерности
            q_lit_per_sec, k = calculate_lit_per_sec(q_day)
            values[5] = f"{k:.2f}"
            values[6] = f"{q_sec * k:.2f}"
            
            # Расчет наполнения и скорости если есть диаметр и уклон
            if len(values) > 8 and values[7] and values[8]:
                d = float(values[7])
                i = float(values[8])
                q_calc = float(values[6])
                h_d_relative, v_final = filling_speed(Q=q_calc, d=d, i=i, n=0.014)
                values[9] = f"{h_d_relative:.2f}"
                values[10] = f"{v_final:.2f}"
                
    except (ValueError, IndexError, ZeroDivisionError):
        pass
        
    return values