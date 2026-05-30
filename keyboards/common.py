from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура с одной кнопкой «Отмена».
    Показываем её, когда ждём текст новой задачи.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
