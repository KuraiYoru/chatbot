from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from states import Register
from aiogram.dispatcher import FSMContext
from database import work_with_bd
from loader import bot
from aiogram.dispatcher.filters import Text
from keyboards.default import checker_button
from aiogram.types import ReplyKeyboardRemove
import json


@dp.message_handler(text='/register')
async def register_(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}! Ты начал регистрацию!\nВведи имя:", reply_markup=checker_button)
    await Register.name.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Регистрация отменена!', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: len(message.text) > 15, state=Register.name)
async def process_age_invalid(message: types.Message):
    await message.reply("Имя не должно содержать более 15 символов")

@dp.message_handler(state=Register.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Register.next()
    await message.reply("Введи возраст: ")



@dp.message_handler(lambda message: not message.text.isdigit() or len(message.text) > 2, state=Register.age)
async def process_age_invalid(message: types.Message):
    await message.reply("Сообщение должно содержать целое число, не превышающее сотни!")

@ dp.message_handler(lambda message: message.text.isdigit(), state=Register.age)
async def process_age(message: types.Message, state: FSMContext):
    await Register.next()
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply("Расскажи о себе: (Описание не должно быть длинее 1000 симолов)")


@dp.message_handler(lambda message: len(message.text) > 1000, state=Register.description)
async def process_age_invalid(message: types.Message):
    await message.reply("Описание слишком длинное!")

@dp.message_handler(state=Register.description)
async def cmd_create_dem(message: types.Message, state: FSMContext):
    await Register.next()
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply("Отправь картинку для своего профиля: ")

@dp.message_handler(state=Register.picture)
async def process_age_invalid(message: types.Message):
    await message.reply("Что-то не так! Убедитесь, что отправили именно картинку!\nОтправьте картинку:")

@dp.message_handler(state=Register.picture, content_types=['photo'])
async def cmd_create_dem(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    picture = data['photo']
    await message.answer('Регистрация успешно завершена!', reply_markup=ReplyKeyboardRemove())
    work_with_bd.register(message.from_user.id)
    data = await state.get_data()
    name = data.get('name')
    years = data.get('age')
    description = data.get('description')
    work_with_bd.set_info(picture, description, str(message.from_user.id), name, years, '@' + str(message.from_user.username))
    await bot.send_photo(chat_id=message.chat.id, photo=picture, caption=f'''Имя: {name}\nВозраст: {years}\nОбо мне: {description}''', reply_markup=ReplyKeyboardRemove())
    await state.finish()
