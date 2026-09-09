class RequestManager:
    def __init__(self):
        # Хранилище заявок (словарь, где ключ - ID заявки)
        self.requests = {}
        # Счетчик для генерации уникальных ID
        self.current_id = 1

    # 1. СОЗДАНИЕ ЗАЯВКИ
    def create_request(self, user_id, title, description, priority="Средний"):
        """
        Создает новую заявку.
        :param user_id: ID пользователя, создающего заявку
        :param title: Заголовок
        :param description: Описание проблемы
        :param priority: Приоритет (Низкий, Средний, Высокий)
        :return: ID новой заявки
        """
        new_id = self.current_id
        self.requests[new_id] = {
            "id": new_id,
            "user_id": user_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "Создана",  # Статусы: Создана, В работе, Завершена, Отменена
            "created_at": "2023-10-01 12:00"  # Для простоты заглушка, можно подключить datetime
        }
        self.current_id += 1
        print(f"✓ Заявка #{new_id} успешно создана!")
        return new_id

    # 2. РЕДАКТИРОВАНИЕ ЗАЯВКИ
    def edit_request(self, request_id, user_id, new_title=None, new_description=None, new_priority=None):
        """
        Редактирует поля существующей заявки (только если она не в статусе "Завершена" или "Отменена").
        """
        # Проверяем, существует ли заявка
        if request_id not in self.requests:
            print(f"✗ Ошибка: Заявка #{request_id} не найдена.")
            return False

        req = self.requests[request_id]

        # Проверяем, что пользователь имеет права (является автором)
        if req["user_id"] != user_id:
            print(f"✗ Ошибка: У вас нет прав на редактирование заявки #{request_id}.")
            return False

        # Проверяем статус (нельзя редактировать завершенные или отмененные)
        if req["status"] in ["Завершена", "Отменена"]:
            print(f"✗ Ошибка: Нельзя редактировать заявку в статусе '{req['status']}'.")
            return False

        # Применяем изменения (если новые значения переданы)
        if new_title is not None:
            req["title"] = new_title
        if new_description is not None:
            req["description"] = new_description
        if new_priority is not None:
            req["priority"] = new_priority

        print(f"✓ Заявка #{request_id} успешно обновлена!")
        return True

    # 3. ПРОСМОТР СВОИХ ЗАЯВОК (с фильтрацией по статусу)
    def view_my_requests(self, user_id, status_filter=None):
        """
        Показывает все заявки пользователя. 
        Можно отфильтровать по статусу (например, только "В работе").
        """
        user_requests = []
        for req in self.requests.values():
            if req["user_id"] == user_id:
                if status_filter is None or req["status"] == status_filter:
                    user_requests.append(req)

        if not user_requests:
            print(f"ℹ Заявок не найдено для пользователя {user_id}.")
            return user_requests

        print(f"\n--- Заявки пользователя {user_id} (всего: {len(user_requests)}) ---")
        for req in user_requests:
            print(f"#{req['id']} | {req['title']} | Статус: {req['status']} | Приоритет: {req['priority']}")
        print("----------------------------------------\n")
        return user_requests

    # 4. ОТМЕНА ЗАЯВКИ
    def cancel_request(self, request_id, user_id):
        """
        Отменяет заявку (меняет статус на "Отменена").
        Только автор может отменить, и только если она не завершена.
        """
        if request_id not in self.requests:
            print(f"✗ Ошибка: Заявка #{request_id} не найдена.")
            return False

        req = self.requests[request_id]

        if req["user_id"] != user_id:
            print(f"✗ Ошибка: Вы не являетесь автором заявки #{request_id}.")
            return False

        if req["status"] == "Завершена":
            print(f"✗ Ошибка: Нельзя отменить завершенную заявку.")
            return False

        if req["status"] == "Отменена":
            print(f"ℹ Заявка #{request_id} уже была отменена ранее.")
            return True

        # Меняем статус
        req["status"] = "Отменена"
        print(f"✓ Заявка #{request_id} успешно отменена.")
        return True


# ============================================
# БЛОК ТЕСТИРОВАНИЯ (пример использования)
# ============================================
if __name__ == "__main__":
    # Создаем экземпляр менеджера
    manager = RequestManager()

    # 1. Создаем заявки от пользователей
    manager.create_request(user_id=101, title="Сломалась мышь", description="Левый клик не работает", priority="Высокий")
    manager.create_request(user_id=101, title="Нет доступа к папке", description="Отказано в доступе к сетевой папке /home")
    manager.create_request(user_id=102, title="Запросить софт", description="Нужна лицензия на Photoshop")

    # 2. Просмотр заявок пользователя 101
    manager.view_my_requests(user_id=101)

    # 3. Редактирование заявки (пользователь 101 правит свою заявку #1)
    manager.edit_request(request_id=1, user_id=101, new_title="Сломалась беспроводная мышь", new_priority="Средний")

    # 4. Просмотр после редактирования
    manager.view_my_requests(user_id=101)

    # 5. Отмена заявки #2 пользователем 101
    manager.cancel_request(request_id=2, user_id=101)

    # 6. Попытка отменить чужую заявку (пользователь 102 пытается отменить заявку #1)
    manager.cancel_request(request_id=1, user_id=102)

    # 7. Финальный просмотр статусов
    manager.view_my_requests(user_id=101)