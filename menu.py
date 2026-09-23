from models import Employee, Ticket
from storage import Storage


class App:
    """Главное приложение"""

    def __init__(self):
        self.storage = Storage()
        self.current_employee = None

    def run(self):
        """Запуск приложения"""
        print("=" * 60)
        print("  СИСТЕМА ВНУТРЕННИХ ЗАЯВОК СОТРУДНИКОВ")
        print("=" * 60)

        while True:
            if not self.current_employee:
                self._auth_menu()
            else:
                self._main_menu()

    def _auth_menu(self):
        """Меню авторизации"""
        print("\n--- Авторизация ---")
        print("1. Войти как существующий сотрудник")
        print("2. Зарегистрироваться")
        print("0. Выйти")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            self._login()
        elif choice == "2":
            self._register()
        elif choice == "0":
            print("До свидания!")
            exit()
        else:
            print("Неверный выбор.")

    def _register(self):
        """Регистрация нового сотрудника"""
        print("\n--- Регистрация ---")
        full_name = input("ФИО: ").strip()
        if not full_name:
            print("ФИО не может быть пустым!")
            return

        if self.storage.find_employee(full_name):
            print("Сотрудник с таким ФИО уже существует!")
            return

        position = input("Должность: ").strip()
        department = input("Отдел: ").strip()

        employee = Employee(full_name=full_name, position=position, department=department)
        self.storage.add_employee(employee)
        self.current_employee = employee.to_dict()
        print(f"\n✅ Добро пожаловать, {full_name}!")

    def _login(self):
        """Вход в систему"""
        full_name = input("\nВведите ваше ФИО: ").strip()
        employee = self.storage.find_employee(full_name)

        if employee:
            self.current_employee = employee
            print(f"\n✅ Добро пожаловать, {employee['full_name']}!")
        else:
            print(" Сотрудник не найден. Зарегистрируйтесь.")

    def _main_menu(self):
        """Главное меню"""
        print(f"\n{'=' * 60}")
        print(f"  Вы вошли как: {self.current_employee['full_name']}")
        print(f"  Отдел: {self.current_employee['department']}")
        print(f"{'=' * 60}")
        print("1.  Создать заявку")
        print("2. 📋 Просмотреть мои заявки")
        print("3. ✏️  Редактировать заявку")
        print("4.  Отменить заявку")
        print("0. 🚪 Выйти из аккаунта")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            self._create_ticket()
        elif choice == "2":
            self._view_tickets()
        elif choice == "3":
            self._edit_ticket()
        elif choice == "4":
            self._cancel_ticket()
        elif choice == "0":
            self.current_employee = None
            print("Вы вышли из аккаунта.")
        else:
            print("Неверный выбор.")

    def _create_ticket(self):
        """Создание заявки"""
        print("\n--- Создание заявки ---")

        # Выбор категории
        categories = self.storage.get_categories()
        print("\nКатегории:")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat['name']} — {cat['description']}")

        cat_choice = input("\nНомер категории: ").strip()
        if not cat_choice.isdigit() or int(cat_choice) < 1 or int(cat_choice) > len(categories):
            print("Неверный номер категории.")
            return
        category = categories[int(cat_choice) - 1]

        # Выбор исполнителя
        executors = self.storage.get_executors()
        print("\nИсполнители:")
        for i, exc in enumerate(executors, 1):
            print(f"  {i}. {exc['full_name']} ({exc['specialization']})")

        exc_choice = input("\nНомер исполнителя (или 0 — не назначать): ").strip()
        executor_id = None
        if exc_choice.isdigit() and 1 <= int(exc_choice) <= len(executors):
            executor_id = executors[int(exc_choice) - 1]["id"]

        title = input("\nКраткое описание проблемы: ").strip()
        if not title:
            print("Описание не может быть пустым!")
            return

        description = input("Подробное описание: ").strip()

        ticket = Ticket(
            employee_id=self.current_employee["id"],
            category_id=category["id"],
            executor_id=executor_id,
            title=title,
            description=description,
        )
        self.storage.create_ticket(ticket)
        print(f"\n✅ Заявка #{ticket.id} успешно создана!")

    def _view_tickets(self):
        """Просмотр своих заявок"""
        tickets = self.storage.get_tickets_by_employee(self.current_employee["id"])
        categories = {c["id"]: c["name"] for c in self.storage.get_categories()}

        if not tickets:
            print("\n У вас пока нет заявок.")
            return

        print(f"\n--- Мои заявки ({len(tickets)} шт.) ---")
        for i, t in enumerate(tickets, 1):
            status_emoji = {"Новая": "", "В работе": "⚙️", "Выполнена": "✅", "Отменена": "❌"}
            emoji = status_emoji.get(t["status"], "📄")
            cat_name = categories.get(t["category_id"], "Неизвестно")
            print(f"\n  {i}. {emoji} [{t['status']}] #{t['id']}")
            print(f"     Категория: {cat_name}")
            print(f"     Тема: {t['title']}")
            print(f"     Создана: {t['created_at']}")
            if t["updated_at"]:
                print(f"     Обновлено: {t['updated_at']}")

    def _edit_ticket(self):
        """Редактирование заявки"""
        tickets = self.storage.get_tickets_by_employee(self.current_employee["id"])
        active_tickets = [t for t in tickets if t["status"] not in ("Выполнена", "Отменена")]

        if not active_tickets:
            print("\nНет заявок для редактирования.")
            return

        print("\n--- Редактирование заявки ---")
        for i, t in enumerate(active_tickets, 1):
            print(f"  {i}. #{t['id']} — {t['title']} [{t['status']}]")

        choice = input("\nНомер заявки: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(active_tickets):
            print("Неверный номер.")
            return

        ticket = active_tickets[int(choice) - 1]

        print(f"\nТекущая тема: {ticket['title']}")
        new_title = input("Новая тема (Enter — без изменений): ").strip()
        if new_title:
            ticket["title"] = new_title

        print(f"\nТекущее описание: {ticket['description']}")
        new_desc = input("Новое описание (Enter — без изменений): ").strip()
        if new_desc:
            ticket["description"] = new_desc

        self.storage.update_ticket(ticket["id"], title=ticket["title"], description=ticket["description"])
        print("✅ Заявка обновлена!")

    def _cancel_ticket(self):
        """Отмена заявки"""
        tickets = self.storage.get_tickets_by_employee(self.current_employee["id"])
        active_tickets = [t for t in tickets if t["status"] == "Новая"]

        if not active_tickets:
            print("\nНет заявок для отмены (можно отменить только 'Новые').")
            return

        print("\n--- Отмена заявки ---")
        for i, t in enumerate(active_tickets, 1):
            print(f"  {i}. #{t['id']} — {t['title']}")

        choice = input("\nНомер заявки для отмены: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(active_tickets):
            print("Неверный номер.")
            return

        ticket = active_tickets[int(choice) - 1]
        confirm = input(f"Отменить заявку #{ticket['id']}? (да/нет): ").strip().lower()

        if confirm in ("да", "yes", "y"):
            self.storage.cancel_ticket(ticket["id"])
            print("✅ Заявка отменена.")
        else:
            print("Отмена отменена 😊")