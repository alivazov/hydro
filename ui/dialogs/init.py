"""
Пакет диалоговых окон
"""

from .cell_editor import CellEditor
from .selection_dialog import SelectionDialog
from .project_properties import ProjectPropertiesDialog

__all__ = ['CellEditor', 'SelectionDialog', 'ProjectPropertiesDialog']