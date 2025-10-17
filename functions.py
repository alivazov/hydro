"""
Функции для гидравлических расчетов
"""
import math


# Существующие функции из вашего кода
MGSN = [[0, 5], [5, 10], [10, 20], [20, 50], [50, 100], [100, 300], [300, 500], [500, 1000], [1000, 5000], [5000, 5000000]]
K_MGSN = [[6, 6], [4.6, 3.5], [3.5, 2.9], [2.9, 2.3], [2.3, 2], [2, 1.85], [1.85, 1.81], [1.81, 1.75], [1.75, 1.52], [1.52, 1.52]]
MATERIAL = {"Чугун (n=0.014)": 0.014,
             "ПЭ (n=0.013)": 0.013
            }

DIAMETR = {
    "Пластик": ['100', '150', '200', '300', '400'],
    "Бетон": ['300', '400', '500', '600', '800'],
    "Сталь": ['150', '200', '250', '300', '350', '400'],
    "Чугун": ['100', '150', '200', '250', '300']
}

def filling_speed(Q, d, i, n):
    d = d/1000  # (в метрах)
    Q = Q/1000  # (в м³/с)
    tolerance = 0.0001  # Допустимая погрешность расхода (м³/с)
    max_iter = 100      # Максимальное количество итераций
    iter_count = 0       # Счетчик итераций

    h_min = 0.001 * d
    h_max = 0.99 * d
    h = (h_min + h_max) / 2  # Начальное приближение
    error = float('inf')     # Инициализируем ошибку бесконечностью

    while error > tolerance and iter_count < max_iter:
        iter_count += 1
        
        theta = 2 * math.acos(1 - (2 * h / d))
        omega = (d**2 / 8) * (theta - math.sin(theta))
        P_wet = (d / 2) * theta
        R = omega / P_wet

        sqrt_n = math.sqrt(n)
        sqrt_R = math.sqrt(R)
        y = 2.5 * sqrt_n - 0.13 - 0.75 * sqrt_R * (sqrt_n - 0.10)
        C = (1 / n) * (R ** y)

        Q_theor = omega * C * math.sqrt(R * i)
        error = abs(Q_theor - Q)

        if error <= tolerance:
            break

        if Q_theor < Q:
            h_min = h  # Требуется большее h
        else:
            h_max = h  # Требуется меньшее h
            
        h = (h_min + h_max) / 2

    if iter_count >= max_iter:
        print(f"Внимание: достигнут лимит {max_iter} итераций!")
        print(f"Текущая погрешность: {error:.6f} м³/с (требуемая: {tolerance})")

    theta_final = 2 * math.acos(1 - (2 * h / d))
    omega_final = (d**2 / 8) * (theta_final - math.sin(theta_final))
    v_final = Q / omega_final
    h_d_relative = h / d
    return h_d_relative, v_final


def calculate_lit_per_sec(Q):
    q = Q/86.4
    q_lit_per_sec = 0
    k, k_1, k_2 = 0, 0, 0
    for a in range(0, len(MGSN)):
        if MGSN[a][0] < q <= MGSN[a][1]:
            k_1 = K_MGSN[a][0]
            k_2 = K_MGSN[a][1]
            # k = k_1 + (k_2 - k_1)*(q - k_1)/(k_2 - k_1)
            k = K_MGSN[a][0] + (K_MGSN[a][1] - K_MGSN[a][0])*(q - MGSN[a][0])/(MGSN[a][1] - MGSN[a][0])
            q_lit_per_sec = q*k
            return q_lit_per_sec, k