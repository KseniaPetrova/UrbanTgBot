from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup
btCalc = KeyboardButton(text='Рассчитать')
btInfo = KeyboardButton(text='Информация')
kb.add(btCalc)
kb.add(btInfo)

keyboard = [[btCalc], [btInfo]]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)