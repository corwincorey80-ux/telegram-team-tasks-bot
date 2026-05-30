import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные из файла .env в корне проекта
load_dotenv()

# Корневая папка проекта (на уровень выше пакета config)
BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    """Настройки бота: токен и путь к базе данных."""

    bot_token: str
    db_path: Path = BASE_DIR / "tasks.db"


def _get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError(
            "Не задан BOT_TOKEN. Создайте файл .env по образцу .env.example"
        )
    return token


settings = Settings(bot_token=_get_bot_token())
