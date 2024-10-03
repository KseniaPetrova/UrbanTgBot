"""
Задача "Продуктовая база":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните ранее написанный код для Telegram-бота:
Создайте файл crud_functions.py и напишите там следующие функции:
initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
title(название продукта) - текст (не пустой)
description(описание) - тест
price(цена) - целое число (не пустой)
get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

Изменения в Telegram-бот:
В самом начале запускайте ранее написанную функцию get_all_products.
Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию get_all_products. Полученные записи используйте в выводимой надписи: "Название: <title> | Описание: <description> | Цена: <price>"
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
"""
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL,
    image_path TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    )
    ''')
    connection.commit()


def fill_db():
    cursor.execute('SELECT COUNT(*) FROM Products')
    if cursor.fetchone()[0] == 0:
        products = [
            ("Витамины В12", "Витаминный комплекс против выпадения волос", 100, 'pictures/swanson-b-12-complex.jpg'),
            ("Витамины В125", "Способствует здоровью нервной системы", 200, 'pictures/swanson-b-125-complex.jpg'),
            ("Витамины В100", "Отлично подходит для энергетического обмена", 300, 'pictures/swanson-balance-b-100-complex.jpg'),
            ("Витамины С", "Витаминный комплекс для иммунитета", 400, 'pictures/swanson-vitamin-c-complex.jpg')
        ]
        cursor.executemany("INSERT INTO Products (title, description, price, image_path) VALUES (?, ?, ?, ?)",
                       products)
        connection.commit()


def get_all_products():
    cursor.execute("SELECT title, description, price, image_path FROM Products")
    products_db = cursor.fetchall()
    connection.close()
    return products_db

def add_user(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?)",
                   (f"{username}", f"{email}", f"{age}", "1000"))
    connection.commit()

def is_included(username):
    users = cursor.execute(f"SELECT username FROM Users WHERE username = ?",
                           (username,)).fetchone()
    connection.commit()
    return users is not None  # функция возвращает users[0]. Если пользователь существует, это будет его имя пользователя. Если пользователя нет, попытка доступа к users[0] вызовет исключение TypeError, так как users будет равен None.

if __name__ == "__main__":
    initiate_db()
    fill_db()
    connection.close()










