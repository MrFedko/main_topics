from aiogram.types import CallbackQuery, Message
from typing import Union
from data.lexicon import lexicon
from .keyboards import start_keyboard, topics_keyboard, menu_cd, questions_keyboard


async def list_start_menu(message: Union[CallbackQuery, Message], **kwargs):
    text = lexicon["/start"].format(name=message.from_user.first_name)
    markup = start_keyboard()

    if isinstance(message, Message):
        await message.answer(text, reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        if call.message.photo:
            await call.message.edit_caption(
                caption=text,
                reply_markup=markup,
                parse_mode="HTML"
            )
        else:
            await call.message.edit_text(
                text,
                reply_markup=markup,
                parse_mode="HTML"
            )

async def list_topics_by_restaurant(call: CallbackQuery, callback_data: menu_cd, **kwargs):
    markup = topics_keyboard(callback_data)
    text = "Выберите интересующий вопрос"
    await call.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode="HTML"
        )

async def list_questions(call: CallbackQuery, callback_data: menu_cd, **kwargs):
    # This function is a placeholder for listing questions based on the topic.
    text = "Список вопросов по выбранной теме."
    markup = questions_keyboard(callback_data)
    await call.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode="HTML"
    )
