import json
import os
from models import Employee, Executor, Category, Ticket


DATA_FILE = "data.json"


class Storage:
    """Класс для работы с хранилищем данных (JSON)"""

    def __init__(self):
        self.data = {
            "employees": [],
            "executors": [],
            "categories": [],
            "tickets": []
        }
        self._load()

    def _load(self):
        """Загрузка данных из файла"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self._init_defaults()
            self._save()

    def _save(self):
        """Сохранение данных в файл"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _init_defaults(self):
        """Инициализация данных по умолчанию"""
        self.data["categories"] = [
            Category(name="IT", description="Технические проблемы").to_dict(),
            Category(name="HR", description="Кадровые вопросы").to_dict(),
            Category(name="АХО", description="Административно-хозяйственный отдел").to_dict(),
            Category(name="Бухгалтерия", description="Финансовые вопросы").to_dict(),
        ]
        self.data["executors"] = [
            Executor(full_name="Иванов И.И.", specialization="IT-специалист").to_dict(),
            Executor(full_name="Петрова А.С.", specialization="HR-менеджер").to_dict(),
            Executor(full_name="Сидоров В.П.", specialization="Инженер АХО").to_dict(),
            Executor(full_name="Козлова Е.М.", specialization="Бухгалтер").to_dict(),
        ]

    # ===== CRUD для заявок =====

    def get_all_tickets(self):
        return self.data["tickets"]

    def get_tickets_by_employee(self, employee_id):
        return [t for t in self.data["tickets"] if t["employee_id"] == employee_id]

    def get_ticket(self, ticket_id):
        for t in self.data["tickets"]:
            if t["id"] == ticket_id:
                return t
        return None

    def create_ticket(self, ticket: Ticket):
        self.data["tickets"].append(ticket.to_dict())
        self._save()

    def update_ticket(self, ticket_id, **kwargs):
        ticket = self.get_ticket(ticket_id)
        if ticket:
            for key, value in kwargs.items():
                if hasattr(ticket, key) or key in ticket:
                    ticket[key] = value
            ticket["updated_at"] = __import__("datetime").datetime.now().strftime("%d.%m.%Y %H:%M")
            self._save()
            return True
        return False

    def cancel_ticket(self, ticket_id):
        return self.update_ticket(ticket_id, status="Отменена")

    # ===== Справочники =====

    def get_categories(self):
        return self.data["categories"]

    def get_executors(self):
        return self.data["executors"]

    def get_employees(self):
        return self.data["employees"]

    def add_employee(self, employee: Employee):
        self.data["employees"].append(employee.to_dict())
        self._save()

    def find_employee(self, full_name):
        for e in self.data["employees"]:
            if e["full_name"].lower() == full_name.lower():
                return e
        return None