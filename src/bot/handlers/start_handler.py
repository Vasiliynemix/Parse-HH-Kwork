import os

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from src.bot.fsm_logic import FSMSettingsParse
from src.bot.keyboards.keyboards import keyboard
from src.parser.parseHH import ParseHH

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.set_state(FSMSettingsParse.start)
    await message.answer(f'Привет, {message.from_user.username}\nДля запуска парсера нажми на кнопку ниже',
                         reply_markup=keyboard.kb.get_start_kb())


@router.message(F.text == 'Отменить настройку')
async def settings_parser(message: Message, state: FSMContext):
    await state.set_state(FSMSettingsParse.start)
    await message.answer(f'Привет, {message.from_user.username}\nДля запуска парсера нажми на кнопку ниже',
                         reply_markup=keyboard.kb.get_start_kb())


@router.message(F.text == 'Запустить парсер')
async def get_name_for_parser(message: Message, state: FSMContext):
    await state.set_state(FSMSettingsParse.name)
    await message.answer('Введите профессию, которую хотите спарсить\n\n'
                         'Вы можете отменить настройку, нажав кнопку "Отменить настройку"',
                         reply_markup=keyboard.kb.get_prev_cancel_kb())


@router.message(FSMSettingsParse.name)
async def get_price_for_parser(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSMSettingsParse.price)
    await message.answer('Введите зарплату, от которой хотите парсить выбранную профессию(руб)\n'
                         'Вы можете отменить настройку, нажав кнопку "Отменить настройку"',
                         reply_markup=keyboard.kb.get_cancel_kb())


@router.message(FSMSettingsParse.price, F.text == 'Назад')
async def prev_fsm(message: Message, state: FSMContext):
    await state.set_state(FSMSettingsParse.name)
    await message.answer('Снова введите профессию\n\n'
                         'Вы можете отменить настройку, нажав кнопку "Отменить настройку"',
                         reply_markup=keyboard.kb.get_prev_cancel_kb())


@router.message(FSMSettingsParse.price)
async def get_price_for_parser(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(FSMSettingsParse.result)
    await message.answer('Проверить настройки парсера\n'
                         'Вы можете отменить настройку, нажав кнопку "Отменить настройку"',
                         reply_markup=keyboard.kb.get_result_settings())


@router.message(FSMSettingsParse.result, F.text == 'Назад')
async def prev_fsm(message: Message, state: FSMContext):
    await state.set_state(FSMSettingsParse.price)
    await message.answer('Снова введите зарплату\n\n'
                         'Вы можете отменить настройку, нажав кнопку "Отменить настройку"',
                         reply_markup=keyboard.kb.get_prev_cancel_kb())


@router.message(FSMSettingsParse.result, F.text == 'Ваши настройки парсера')
async def get_settings_for_parser(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSMSettingsParse.run)
    await message.answer(f'Профессия: {data["name"]}\n'
                         f'Цена от: {data["price"]}\n\n'
                         f'Начать парсинг👇',
                         reply_markup=keyboard.ikb.run_parse())


@router.callback_query(FSMSettingsParse.run, lambda c: c.data == 'run_parse')
async def run_parser(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    await state.set_state(FSMSettingsParse.document)
    await ParseHH(callback=call, name=data['name'], price=data['price']).parse()
    await call.message.answer(f'Парсер запущен!\n\nname = {data["name"]}\nprice = {data["price"]}',
                              reply_markup=keyboard.kb.get_result_doc())


@router.message(FSMSettingsParse.document, F.text == 'Получить данные👇')
async def set_document(message: Message, state: FSMContext):
    await state.set_state(FSMSettingsParse.start)
    path = os.path.abspath('hh_data.csv')
    await message.answer('Спасибо, что пользовались мной\n'
                         'Вот данные в csv👇')
    await message.answer_document(FSInputFile(path), reply_markup=keyboard.kb.get_start_kb())
    os.remove(path)
