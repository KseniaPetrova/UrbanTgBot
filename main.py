"""Задача "Бот поддержки (Начало)":"""
"""К коду из подготовительного видео напишите две асинхронные функции:
start(message) - печатает строку в консоли 'Привет! Я бот помогающий твоему здоровью.' . Запускается только когда написана команда '/start' в чате с ботом. (используйте соответствующий декоратор)
all_massages(message) - печатает строку в консоли 'Введите команду /start, чтобы начать общение.'. Запускается при любом обращении не описанном ранее. (используйте соответствующий декоратор)
Запустите ваш Telegram-бот и проверьте его на работоспособность."""
"""Задача "Он мне ответил!":
Измените функции start и all_messages так, чтобы вместо вывода в консоль строки отправлялись в чате телеграм.
Запустите ваш Telegram-бот и проверьте его на работоспособность."""
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN, MY_ID
from calorie_calculator import UserState, set_age, set_growth, set_weight, send_calories
from exa_key import kb
from inline_key import inLineKb, inLineKbBuy
from crud_functions import initiate_db, get_all_products

api = TELEGRAM_BOT_TOKEN
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


async def hello_start(_):  # функция для меня
    await bot.send_message(chat_id=MY_ID, text='Бот запущен')

# async def db_start():
#     initiate_db()
#     products = get_all_products()

@dp.message_handler(commands='start')
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


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

@dp.message_handler(text='Купить')  # Задача "Витамины для всех!"
async def get_buying_list(message):
    # products = [
    #     ("Продукт 1", "Описание 1", 100, 'pictures/swanson-b-12-complex.jpg'),
    #     ("Продукт 2", "Описание 2", 200, 'pictures/swanson-b-125-complex.jpg'),
    #     ("Продукт 3", "Описание 3", 300, 'pictures/swanson-balance-b-100-complex.jpg'),
    #     ("Продукт 4", "Описание 4", 400, 'pictures/swanson-vitamin-c-complex.jpg')
    # ]

    # for product in products:
    #     product_name, description, price, image_path = product
    #     with open(image_path, 'rb') as img:
    #         await message.answer_photo(img,
    #                                    f'Название: {product_name} | Описание: {description} | Цена: {price}')

    products = get_all_products()

    for title, description, price, image_path in products:
        with open(image_path, 'rb') as img:
            await message.answer_photo(img, f'Название: {title} | Описание: {description} | Цена: {price}')

    await message.answer('Выберите продукт для покупки:', reply_markup=inLineKbBuy)


@dp.callback_query_handler(text='product_buying')  # Задача "Витамины для всех!"
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=hello_start)