"""
Модель проекта
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

@dataclass
class ProjectMetadata:
    name: str = "Новый проект"
    file_path: str = None
    created_date: str = None
    modified_date: str = None
    version: str = "1.0"
    description: str = ""  # Добавлено поле описания
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.modified_date is None:
            self.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Project:
    def __init__(self):
        self.metadata = ProjectMetadata()
        self.data = {
            "calculations": {},
            "construction_stages": [],
            "platforms": [],
            "capacity_check": [],
            "balance": []
        }
        self.is_modified = False
        
    @property
    def name(self):
        return self.metadata.name
        
    @name.setter
    def name(self, value):
        self.metadata.name = value
        self.is_modified = True
        
    @property
    def file_path(self):
        return self.metadata.file_path
        
    @file_path.setter
    def file_path(self, value):
        self.metadata.file_path = value
        self.is_modified = True
        
    def save(self, file_path):
        """Сохранение проекта в файл"""
        self.metadata.file_path = file_path
        self.metadata.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        project_data = {
            "metadata": asdict(self.metadata),
            "data": self.data
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=4)
                
            self.is_modified = False
            print(f"Проект сохранен: {file_path}")
            return True
        except Exception as e:
            print(f"Ошибка сохранения проекта {file_path}: {e}")
            return False
        
    @classmethod
    def load(cls, file_path):
        """Загрузка проекта из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
                
            project = cls()
            
            # Загружаем метаданные, обрабатывая отсутствующие поля
            metadata_dict = project_data.get("metadata", {})
            project.metadata = ProjectMetadata(
                name=metadata_dict.get("name", "Новый проект"),
                file_path=metadata_dict.get("file_path"),
                created_date=metadata_dict.get("created_date"),
                modified_date=metadata_dict.get("modified_date"),
                version=metadata_dict.get("version", "1.0"),
                description=metadata_dict.get("description", "")
            )
            
            project.data = project_data.get("data", {})
            project.is_modified = False
            
            print(f"Проект загружен: {file_path}")
            return project
            
        except Exception as e:
            print(f"Ошибка загрузки проекта {file_path}: {e}")
            raise