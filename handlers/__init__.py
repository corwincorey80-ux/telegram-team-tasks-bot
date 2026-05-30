from aiogram import Router

from handlers.add import router as add_router
from handlers.list_tasks import router as list_router
from handlers.start import router as start_router

# Главный роутер: подключаем все обработчики команд
main_router = Router()
main_router.include_router(start_router)
main_router.include_router(add_router)
main_router.include_router(list_router)
