# Telegram-бот: общий список задач

Командный бот на [aiogram 3](https://docs.aiogram.dev/) с хранением задач в SQLite.

## Команды

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и справка |
| `/add` | Добавить задачу |
| `/list` | Показать все задачи |
| `/list_csv` | Скачать список в CSV |

## Запуск

```bash
pip install -r requirements.txt
copy .env.example .env
# Укажите BOT_TOKEN в .env
python main.py
```

## Структура

- `main.py` — точка входа
- `handlers/` — обработчики команд
- `database/` — работа с SQLite
- `config/` — настройки
- `keyboards/` — клавиатуры
