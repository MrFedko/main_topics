from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from data.config import settings
from loader import dataBase


class menu_cd(CallbackData, prefix="show_menu"):
    level: int = 0
    restaurant_sheet_id: int = 0
    topic_id: int = 0
    question_id: int = 0


def start_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    list_buttons = list(settings.worksheet_ids.keys())
    buttons = []
    for name in list_buttons:
        buttons.append(
            InlineKeyboardButton(
                text=name,
                callback_data=menu_cd(
                    level=1,
                    restaurant_sheet_id=settings.worksheet_ids[name]
                ).pack()
            )
        )
    markup.row(*buttons, width=1)
    return markup.as_markup()


def topics_keyboard(callback_data: menu_cd) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = []
    restaurant_sheet_id = callback_data.restaurant_sheet_id
    rest_name = settings.rests_by_worksheet_ids[restaurant_sheet_id]
    topics = dataBase.get_topics_by_restaurant(rest_name)
    for topic in topics:
        buttons.append(
            InlineKeyboardButton(
                text=topic,
                callback_data=menu_cd(
                    level=2,
                    restaurant_sheet_id=restaurant_sheet_id,
                    topic_id= dataBase.get_topic_id_by_name(topic)
                ).pack()
            )
        )
    markup.row(*buttons, width=1)
    back_button = InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data=menu_cd(
            level=0
        ).pack()
    )
    markup.row(back_button)
    return markup.as_markup()


def questions_keyboard(callback_data: menu_cd) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    buttons = []
    restaurant_name = settings.rests_by_worksheet_ids[callback_data.restaurant_sheet_id]
    topic_name = dataBase.get_topic_name_by_id(callback_data.topic_id)
    questions = dataBase.get_questions(restaurant_name, topic_name)
    for question in questions:
        buttons.append(
            InlineKeyboardButton(
                text=question[1],
                callback_data=menu_cd(
                    level=3,
                    restaurant_sheet_id=callback_data.restaurant_sheet_id,
                    topic_id=callback_data.topic_id,
                    question_id=question[0]
                ).pack()
            )
        )
    markup.row(*buttons, width=1)
    back_button = InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data=menu_cd(
            level=1,
            restaurant_sheet_id=callback_data.restaurant_sheet_id
        ).pack()
    )
    markup.row(back_button)
    return markup.as_markup()


def back_button_final(callback_data: menu_cd) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    back_button = InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data=menu_cd(
            level=2,
            restaurant_sheet_id=callback_data.restaurant_sheet_id,
            topic_id=callback_data.topic_id,
        ).pack()
    )
    markup.row(back_button)
    return markup.as_markup()
