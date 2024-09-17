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
import asyncio
from config import TELEGRAM_BOT_TOKEN
from calorie_calculator import UserState, set_age, set_growth, set_weight, send_calories

api = TELEGRAM_BOT_TOKEN
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


async def hello_start(_):  # функция для меня
    await bot.send_message(chat_id='1327261756', text='Бот запущен')


@dp.message_handler(commands='start')
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')  # Задача "Бот поддержки (Начало)"
    await message.answer('Привет! Я бот помогающий твоему здоровью.')  # Задача "Он мне ответил!"

@dp.message_handler(text='Calories')  # Задача "Цепочка вопросов
async def start_calories(message):
    await set_age(message)

@dp.message_handler(state=UserState.age)  # Задача "Цепочка вопросов
async def continue_calories(message, state):
    await set_growth(message, state)

@dp.message_handler(state=UserState.growth)  # Задача "Цепочка вопросов
async def continue_calories(message, state):
    await set_weight(message, state)

@dp.message_handler(state=UserState.weight)  # Задача "Цепочка вопросов
async def complete_calories(message, state):
    await send_calories(message, state)

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')  # Задача "Бот поддержки (Начало)"
    await message.answer('Введите команду /start, чтобы начать общение.')  # Задача "Он мне ответил!"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=hello_start)