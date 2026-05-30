import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные из файла .env в корне проекта
load_dotenv()

# Корневая папка проекта (на уровень выше пакета config)
BASE_DIR = Path(__file__).resolve().parent.parent


def _get_db_path() -> Path:
    """
    Локально — tasks.db в папке проекта.
    На Amvera — в /data (persistenceMount), иначе БД сбросится при деплое.
    """
    if "AMVERA" in os.environ:
        return Path("/data/tasks.db")
    return BASE_DIR / "tasks.db"


@dataclass(frozen=True)
class Settings:
    """Настройки бота: токен и путь к базе данных."""

    bot_token: str
    db_path: Path


def _get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError(
            "Не задан BOT_TOKEN. Создайте файл .env по образцу .env.example"
        )
    return token


settings = Settings(bot_token=_get_bot_token(), db_path=_get_db_path())
