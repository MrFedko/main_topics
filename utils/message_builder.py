class MessageBuilder:
    def __init__(self):
        self.names = {
            "answer": "Ответ",
            "restaurant": "Ресторан",
            "topic": "Тема",
            "question": "Вопрос",
            "restrictions": "Условия и ограничения",
            "url": "Актуальный источник / URL",
            "date_control": "Дата проверки",
            "responsible_position": "Ответственный / должность",
            "responsible_name": "Контакт ответственного",
            "approval_is_required": "Требуется ли согласование",
            "approval_position": "Кто согласовывает",
            "approval_contact": "Контакт для согласования",
            "approval_period": "Период проверки",
            "next_approve": "Следующая проверка",
            "answer_status": "Статус ответа",
            "notes": "Примечания",
        }
        self.EXCLUDED_KEYS = {"id", "question"}


    def build_answer_text(self, info: dict) -> str:
        text = f"""<b>{info['question']}</b>\n\n"""
        for key, value in self.names.items():
            if key not in self.EXCLUDED_KEYS and info[key]:
                    text += f"<b>{self.names[key]}:</b>\n{info[key]}\n\n"
        return text
