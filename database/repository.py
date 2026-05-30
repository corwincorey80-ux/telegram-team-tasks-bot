import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class Task:
    """Одна задача из таблицы tasks."""

    id: int
    text: str
    user: str
    created_at: str


def init_db(db_path: Path) -> None:
    """
    Создаёт файл базы и таблицу tasks, если их ещё нет.
    Вызывается один раз при старте бота.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


class TaskRepository:
    """Все операции с задачами в SQLite."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def add_task(self, text: str, user: str) -> Task:
        """Добавляет задачу и возвращает созданную запись."""
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
                (text.strip(), user, created_at),
            )
            task_id = cursor.lastrowid
            conn.commit()
        return Task(id=task_id, text=text.strip(), user=user, created_at=created_at)

    def get_all_tasks(self) -> List[Task]:
        """Возвращает все задачи, от старых к новым."""
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, text, user, created_at FROM tasks ORDER BY id ASC"
            ).fetchall()
        return [Task(**dict(row)) for row in rows]

    def get_task_count(self) -> int:
        """Сколько задач в базе (удобно для проверок)."""
        with sqlite3.connect(self._db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()
        return int(row[0]) if row else 0
