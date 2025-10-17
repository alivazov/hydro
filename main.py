#!/usr/bin/env python3
"""
Главный файл гидравлического калькулятора
"""

import tkinter as tk
from core.app import HydraulicCalculatorApp

def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = HydraulicCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()