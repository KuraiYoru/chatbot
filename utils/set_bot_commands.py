from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'старт'),
        types.BotCommand('help', 'помощь'),
        types.BotCommand('register', 'регистрация'),
        types.BotCommand('send_user', 'Отправить профиль пользователя'),
        types.BotCommand('cancel', 'Отмена регистрации'),
    ])