from dataclasses import dataclass

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dataclass
class ReplyKeyboard:
    @staticmethod
    def get_start_kb():
        start_kb = [
            [KeyboardButton(text='Запустить парсер')]
        ]
        return ReplyKeyboardMarkup(keyboard=start_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Нажмите на кнопку ниже для запуска👇',
                                   one_time_keyboard=True)

    @staticmethod
    def get_cancel_kb():
        cancel_kb = [
            [KeyboardButton(text='Назад')],
            [KeyboardButton(text='Отменить настройку')]
        ]
        return ReplyKeyboardMarkup(keyboard=cancel_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='если хотите что-то изменить нажмите кнопку "Назад"👇',
                                   one_time_keyboard=True)

    @staticmethod
    def get_prev_cancel_kb():
        cancel_kb = [
            [KeyboardButton(text='Отменить настройку')]
        ]
        return ReplyKeyboardMarkup(keyboard=cancel_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='если хотите отменить нажмите "Отменить настройку"👇',
                                   one_time_keyboard=True)

    @staticmethod
    def get_result_settings():
        get_result_kb = [
            [KeyboardButton(text='Ваши настройки парсера')],
            [KeyboardButton(text='Назад'), KeyboardButton(text='Отменить настройку')],
        ]
        return ReplyKeyboardMarkup(keyboard=get_result_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Нажмите на нужную кнопку ниже👇',
                                   one_time_keyboard=True)

    @staticmethod
    def get_result_doc():
        get_doc_kb = [
            [KeyboardButton(text='Получить данные👇')]
        ]
        return ReplyKeyboardMarkup(keyboard=get_doc_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Нажмите на нужную кнопку ниже👇',
                                   one_time_keyboard=True)


@dataclass
class InlineKeyboard:
    @staticmethod
    def run_parse():
        run_ikb = InlineKeyboardBuilder()
        run_ikb.button(text='Запуск!', callback_data='run_parse')
        run_ikb.adjust(1)
        return run_ikb.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True)


@dataclass
class Keyboard:
    kb: ReplyKeyboard() = ReplyKeyboard
    ikb: InlineKeyboard() = InlineKeyboard


keyboard: Keyboard = Keyboard()
