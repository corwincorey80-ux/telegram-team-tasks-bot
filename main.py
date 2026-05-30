"""
Точка входа: запуск Telegram-бота для общего списка задач.

Перед запуском:
1. pip install -r requirements.txt
2. Скопируйте .env.example в .env и укажите BOT_TOKEN от @BotFather
3. python main.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from database.repository import TaskRepository, init_db
from handlers import main_router

# Логи в консоль — удобно при отладке
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Создаём таблицу tasks при первом запуске
    init_db(settings.db_path)
    task_repo = TaskRepository(settings.db_path)

    bot = Bot(token=settings.bot_token)
    # Хранилище состояний FSM (для диалога /add) — в памяти
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    # task_repo передаётся в хендлеры по имени параметра task_repo
    await dp.start_polling(bot, task_repo=task_repo)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
