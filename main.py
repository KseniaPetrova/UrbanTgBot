"""Задача "Бот поддержки (Начало)":"""
"""К коду из подготовительного видео напишите две асинхронные функции:
start(message) - печатает строку в консоли 'Привет! Я бот помогающий твоему здоровью.' . Запускается только когда написана команда '/start' в чате с ботом. (используйте соответствующий декоратор)
all_massages(message) - печатает строку в консоли 'Введите команду /start, чтобы начать общение.'. Запускается при любом обращении не описанном ранее. (используйте соответствующий декоратор)
Запустите ваш Telegram-бот и проверьте его на работоспособность."""
"""Задача "Он мне ответил!":
Измените функции start и all_messages так, чтобы вместо вывода в консоль строки отправлялись в чате телеграм.
Запустите ваш Telegram-бот и проверьте его на работоспособность."""
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from config import TELEGRAM_BOT_TOKEN, MY_ID
from calorie_calculator import UserState, set_age, set_growth, set_weight, send_calories
from exa_key import reply_markup
from inline_key import inLineKb

api = TELEGRAM_BOT_TOKEN
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


async def hello_start(_):  # функция для меня
    await bot.send_message(chat_id=MY_ID, text='Бот запущен')


@dp.message_handler(commands='start')
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=reply_markup)


# @dp.message_handler(text='Рассчитать')
# async def start_calories(message):
#     await set_age(message)

@dp.callback_query_handler(text='calories')  # Задача "Ещё больше выбора"
async def start_calories(call):
    await set_age(call)

@dp.message_handler(state=UserState.age)
async def continue_calories(message, state):
    await set_growth(message, state)

@dp.message_handler(state=UserState.growth)
async def continue_calories(message, state):
    await set_weight(message, state)

@dp.message_handler(state=UserState.weight)
async def complete_calories(message, state):
    await send_calories(message, state)

@dp.message_handler(text='Рассчитать')  # Задача "Ещё больше выбора"
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inLineKb)

@dp.callback_query_handler(text='formulas')  # Задача "Ещё больше выбора"
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=hello_start)