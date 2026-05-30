from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.repository import TaskRepository
from keyboards.common import cancel_keyboard

router = Router(name="add")


class AddTaskStates(StatesGroup):
    """Состояния диалога: ждём текст задачи от пользователя."""

    waiting_for_text = State()


def _format_user(message: Message) -> str:
    """Имя автора для поля user в базе."""
    if message.from_user:
        if message.from_user.username:
            return f"@{message.from_user.username}"
        name = message.from_user.full_name or "unknown"
        return f"{name} (id:{message.from_user.id})"
    return "unknown"


@router.message(Command("add"))
async def cmd_add(
    message: Message, state: FSMContext, task_repo: TaskRepository
) -> None:
    """
    Команда /add — просим ввести текст задачи.
    Можно также: /add Купить молоко — тогда текст берётся из команды.
    """
    # Текст после команды, например: /add Позвонить клиенту
    args = message.text.split(maxsplit=1) if message.text else []
    if len(args) > 1 and args[1].strip():
        task = task_repo.add_task(text=args[1], user=_format_user(message))
        await message.answer(
            f"Задача #{task.id} добавлена:\n{task.text}\n"
            f"Автор: {task.user}\n"
            f"Дата: {task.created_at}"
        )
        return

    await state.set_state(AddTaskStates.waiting_for_text)
    await message.answer(
        "Напишите текст задачи одним сообщением.\n"
        "Или нажмите «Отмена», чтобы выйти.",
        reply_markup=cancel_keyboard(),
    )


@router.message(AddTaskStates.waiting_for_text, F.text == "Отмена")
async def cancel_add(message: Message, state: FSMContext) -> None:
    """Пользователь нажал «Отмена» — выходим из режима добавления."""
    await state.clear()
    await message.answer("Добавление отменено.", reply_markup=None)


@router.message(AddTaskStates.waiting_for_text)
async def save_task_text(
    message: Message, state: FSMContext, task_repo: TaskRepository
) -> None:
    """Сохраняем текст задачи в базу."""
    if not message.text or not message.text.strip():
        await message.answer("Текст не может быть пустым. Введите задачу ещё раз.")
        return

    task = task_repo.add_task(text=message.text, user=_format_user(message))
    await state.clear()
    await message.answer(
        f"Задача #{task.id} добавлена:\n{task.text}\n"
        f"Автор: {task.user}\n"
        f"Дата: {task.created_at}",
        reply_markup=None,
    )