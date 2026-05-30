import csv
import io
from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from database.repository import Task, TaskRepository

router = Router(name="list")


def _format_tasks_list(tasks: List[Task]) -> str:
    """Форматируем задачи для вывода в чат."""
    lines = []
    for task in tasks:
        lines.append(
            f"#{task.id} | {task.created_at}\n"
            f"{task.text}\n"
            f"Автор: {task.user}\n"
        )
    return "\n".join(lines)


@router.message(Command("list"))
async def cmd_list(message: Message, task_repo: TaskRepository) -> None:
    """Команда /list — показать все задачи в сообщении."""
    tasks = task_repo.get_all_tasks()

    if not tasks:
        await message.answer("Список задач пуст. Добавьте первую: /add")
        return

    text = _format_tasks_list(tasks)
    # Telegram ограничивает длину сообщения (~4096 символов)
    if len(text) > 4000:
        await message.answer(
            f"Задач слишком много для одного сообщения ({len(tasks)} шт.). "
            "Используйте /list_csv"
        )
        return

    await message.answer(text)


@router.message(Command("list_csv"))
async def cmd_list_csv(message: Message, task_repo: TaskRepository) -> None:
    """Команда /list_csv — отправить файл CSV со всеми задачами."""
    tasks = task_repo.get_all_tasks()

    if not tasks:
        await message.answer("Список задач пуст. Добавьте первую: /add")
        return

    # Пишем CSV в память (без создания файла на диске)
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";", lineterminator="\n")
    writer.writerow(["id", "text", "user", "created_at"])
    for task in tasks:
        writer.writerow([task.id, task.text, task.user, task.created_at])

    # Кодируем в байты для отправки файла
    csv_bytes = buffer.getvalue().encode("utf-8-sig")  # BOM для Excel
    document = BufferedInputFile(csv_bytes, filename="tasks.csv")

    await message.answer_document(
        document=document,
        caption=f"Экспорт задач: {len(tasks)} шт.",
    )
