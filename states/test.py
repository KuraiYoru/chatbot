from aiogram.dispatcher.filters.state import StatesGroup, State

class Register(StatesGroup):
    name = State()
    age = State()
    description = State()
    picture = State()