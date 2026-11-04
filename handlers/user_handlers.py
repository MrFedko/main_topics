import glob
import os

from aiogram import types, F as f, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import FSInputFile, InputMediaPhoto
from magic_filter import F as MF
from PIL import Image
from loader import dataBase, messageBuilder, client
from .menuLists import list_start_menu, list_topics_by_restaurant, list_questions
from data.config import settings
from .keyboards import menu_cd, back_button_final

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await list_start_menu(message)

@router.callback_query(
    menu_cd.filter(MF.level == 0), flags={"chat_action": "typing"}
)
async def start_menu_callback(
        call: types.CallbackQuery,
        callback_data: menu_cd,
        state: FSMContext,
):
    await state.clear()
    await list_start_menu(call)


@router.message(Command("upload"))
async def cmd_reboot(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Данные обновлены, фотографии загружены, всё готово!")
    await list_start_menu(message)


@router.callback_query(
    menu_cd.filter(MF.level == 1), flags={"chat_action": "typing"}
)
async def topics_by_restaurant_callback(
        call: types.CallbackQuery,
        callback_data: menu_cd,
        state: FSMContext,
):
    await state.update_data(restaurant_sheet_id=callback_data.restaurant_sheet_id)
    await list_topics_by_restaurant(call, callback_data)


@router.callback_query(
    menu_cd.filter(MF.level == 2), flags={"chat_action": "typing"}
)
async def questions_by_topic_callback(
        call: types.CallbackQuery,
        callback_data: menu_cd,
        state: FSMContext,
):
    await state.update_data(topic_id=callback_data.topic_id)
    await list_questions(call, callback_data)


@router.callback_query(
    menu_cd.filter(MF.level == 3), flags={"chat_action": "typing"}
)
async def answer_by_question_callback(
        call: types.CallbackQuery,
        callback_data: menu_cd,
        state: FSMContext,
):
    import asyncio

    MAX_CAPTION_LENGTH = 1024
    # список для хранения ID сообщений
    sent_messages = []

    # 🔴 сначала удалим старые сообщения (если были)
    old_data = await state.get_data()
    old_messages = old_data.get("extra_messages", [])

    for msg_id in old_messages:
        try:
            await call.bot.delete_message(call.message.chat.id, msg_id)
        except:
            pass

    await state.update_data(extra_messages=[])
    question_id = callback_data.question_id
    answer = dataBase.get_answer_by_id(question_id)
    text = messageBuilder.build_answer_text(answer)
    if len(text) <= MAX_CAPTION_LENGTH:
        await call.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_button_final(callback_data)
        )
    else:
        chunks = [
            text[i:i + MAX_CAPTION_LENGTH]
            for i in range(0, len(text), MAX_CAPTION_LENGTH)
        ]

        await call.message.edit_text(
            chunks[0],
            parse_mode="HTML",
        )
        sent_messages.append(call.message.message_id)

        for i, chunk in enumerate(chunks[1:]):
            if not chunk.strip():
                continue

            is_last = i == len(chunks[1:]) - 1

            msg = await call.message.answer(chunk, parse_mode="HTML",
                                            reply_markup=back_button_final(callback_data) if is_last else None)
            sent_messages.append(msg.message_id if not is_last else None)

            await asyncio.sleep(0.05)

        # 💾 сохраняем ID сообщений
    await state.update_data(extra_messages=sent_messages)
