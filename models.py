from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
import uuid


@dataclass
class Employee:
    """Сущность: Сотрудник"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    full_name: str = ""
    position: str = ""
    department: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Executor:
    """Сущность: Исполнитель"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    full_name: str = ""
    specialization: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Category:
    """Сущность: Категория заявки"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Ticket:
    """Сущность: Заявка"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    employee_id: str = ""
    category_id: str = ""
    executor_id: Optional[str] = None
    title: str = ""
    description: str = ""
    status: str = "Новая"  # Новая / В работе / Выполнена / Отменена
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))
    updated_at: str = ""

    def to_dict(self):
        return asdict(self)

    def update_timestamp(self):
        self.updated_at = datetime.now().strftime("%d.%m.%Y %H:%M")