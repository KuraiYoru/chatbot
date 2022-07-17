import json

from aiogram import types
from loader import dp
from database import work_with_bd
from loader import bot
import random
from keyboards.default import lesson_btn
from aiogram.dispatcher.filters import Text

@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! \n Твой айди: {message.from_user.id}")
    work_with_bd.register(message.from_user.id)

@dp.message_handler(text='/help')
async def command_help(message: types.Message):
    await message.answer(f"Lo, {message.from_user.full_name}! \n Твой айди: {message.from_user.id}")


@dp.message_handler(text='/send_user')
async def profile(message: types.Message):
    if not work_with_bd.check_register(message.from_user.id):
        await message.answer('Для начала пройдите регистрацию и убедитесь, что в вашем телеграмм профиле установлен тег: /register')
    else:
        all_id = work_with_bd.all_id()
        if f"{message.from_user.id}" in all_id:
            del all_id[all_id.index(f"{message.from_user.id}")]
        if len(all_id) == 0:
            await message.answer('Вы пока единственный пользователь, дождитесь регистрации еще кого-нибудь')
        else:
            user_id = random.choice(all_id)
            data = work_with_bd.send_profile(user_id)
            dictionary = json.loads(data[1])
            name, age, description = dictionary['name'], dictionary['age'], data[2]
            await bot.send_photo(chat_id=message.chat.id, photo=data[3], caption=f'''Имя: {name}
Возраст: {age}
Обо мне: {description}''', reply_markup=lesson_btn)
            work_with_bd.set_current_id(user_id, str(message.from_user.id))

@dp.callback_query_handler(Text(startswith='like'))
async def process_callback_kb1btn1(callback: types.CallbackQuery):
    if not work_with_bd.check_register(callback.from_user.id):
        await callback.answer('Для начала пройдите регистрацию и убедитесь, что в вашем телеграмм профиле установлен тег: /register')
    else:
        user_id = work_with_bd.get_current_id(str(callback.from_user.id))
        work_with_bd.liked_person(callback.from_user.id, user_id)
        all_id = work_with_bd.all_id()
        if f"{callback.from_user.id}" in all_id:
            del all_id[all_id.index(f"{callback.from_user.id}")]
        user_id = random.choice(all_id)
        data = work_with_bd.send_profile(user_id)
        dictionary = json.loads(data[1])
        name, age, description = dictionary['name'], dictionary['age'], data[2]
        await bot.send_photo(chat_id=callback.from_user.id, photo=data[3], caption=f'''Имя: {name}
Возраст: {age}
Обо мне: {description}''', reply_markup=lesson_btn)
        work_with_bd.set_current_id(user_id, str(callback.from_user.id))

@dp.callback_query_handler(Text(startswith='dislike'))
async def process_callback_kb1btn1(callback: types.CallbackQuery):
    if not work_with_bd.check_register(callback.from_user.id):
        await callback.answer('Для начала пройдите регистрацию и убедитесь, что в вашем телеграмм профиле установлен тег: /register')
    else:
        all_id = work_with_bd.all_id()
        if f"{callback.from_user.id}" in all_id:
            del all_id[all_id.index(f"{callback.from_user.id}")]
        user_id = random.choice(all_id)
        data = work_with_bd.send_profile(user_id)
        dictionary = json.loads(data[1])
        name, age, description = dictionary['name'], dictionary['age'], data[2]
        await bot.send_photo(chat_id=callback.from_user.id, photo=data[3], caption=f'''Имя: {name}
Возраст: {age}
Обо мне: {description}''', reply_markup=lesson_btn)
        work_with_bd.set_current_id(user_id, str(callback.from_user.id))


@dp.message_handler(text='/check')
async def profile(message: types.Message):
    data = work_with_bd.get_liked(message.from_user.id)
    for person in data:
        if str(message.from_user.id) in work_with_bd.get_liked(person):
            await message.answer('Твоя анкета понравилась данному пользователю!')
            data = work_with_bd.send_profile(person)
            dictionary = json.loads(data[1])
            teg = work_with_bd.check_register(person)
            name, age, description = dictionary['name'], dictionary['age'], data[2]
            await bot.send_photo(chat_id=message.from_user.id, photo=data[3], caption=f'''Имя: {name}
Возраст: {age}
Обо мне: {description}
{teg}''')
        else:
            await message.answer('Похоже твоя анкета ещё никому не приглянулась :(')


