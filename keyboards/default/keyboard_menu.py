from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton('/cancel')

checker_button = ReplyKeyboardMarkup(resize_keyboard=True)
checker_button.add(b1)
t1 = InlineKeyboardButton('❤', callback_data='like')
t2 = InlineKeyboardButton('👎🏻', callback_data='dislike')

lesson_btn = InlineKeyboardMarkup().row(t1, t2)