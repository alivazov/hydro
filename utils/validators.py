"""
Валидация вводимых данных
"""

def validate_float(P):
    """Валидация чисел с плавающей точкой"""
    if P == "" or P == "-":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False

def validate_integer(P):
    """Валидация целых чисел"""
    if P == "":
        return True
    return P.isdigit()

def validate_percentage(P):
    """Валидация процентов"""
    if P == "":
        return True
    try:
        value = float(P)
        return 0 <= value <= 100
    except ValueError:
        return False

def validate_positive_float(P):
    """Валидация положительных чисел"""
    if P == "":
        return True
    try:
        value = float(P)
        return value >= 0
    except ValueError:
        return False