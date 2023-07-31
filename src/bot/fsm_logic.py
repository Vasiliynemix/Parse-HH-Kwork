from aiogram.fsm.state import StatesGroup, State


class FSMSettingsParse(StatesGroup):
    start = State()
    name = State()
    price = State()
    result = State()
    run = State()
    document = State()
