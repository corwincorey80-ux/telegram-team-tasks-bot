from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="start")


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Команда /start — приветствие и краткая справка."""
    await message.answer(
        "Привет! Я бот для общего списка задач команды.\n\n"
        "Доступные команды:\n"
        "/add — добавить задачу\n"
        "/list — показать все задачи\n"
        "/list_csv — получить список в файле CSV"
    )
