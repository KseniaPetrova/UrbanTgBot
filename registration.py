"""
Задача "Регистрация покупателей":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число (не пустой)
balance - целое число (не пустой)
add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.

Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
Создайте цепочку изменений состояний RegistrationState.
Фукнции цепочки состояний RegistrationState:
sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
"""


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from config import TELEGRAM_BOT_TOKEN
from crud_functions import is_included, add_user

api = TELEGRAM_BOT_TOKEN
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text="Регистрация")
async def sing_up(message :types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message :types.Message, state :FSMContext):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message :types.Message, state :FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message :types.Message, state :FSMContext):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    add_user(user_data['username'], user_data['email'], user_data['age'])
    await message.answer('Вы успешно зарегистрированы!')
    await state.finish()










