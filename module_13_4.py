# Домашнее задание по теме "Машина состояний"
# Ваша задача:
# Цель: получить навык работы с состояниями в телеграм-боте.
# Задача "Цепочка вопросов":
# Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека.
# Группа состояний:
# 1. Импортируйте классы State и StateGroup из aiogram.dispatcher.filters.state.
# 2. Создайте класс UserState наследованный от StateGroup.
# 3. Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).
# Эта группа(класс) будет использоваться в цепочке вызовов message_handler'ов.
# Напишите следующие функции для обработки состояний:
# Функцию set_age(message):
# 1. Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
# 2. Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
# 3. После ожидать ввода возраста в атрибут UserState.age при помощи метода set.
# Функцию set_growth(message, state):
# 1. Оберните её в message_handler, который реагирует на переданное состояние UserState.age.
# 2. Эта функция должна обновлять данные в состоянии age на message.text (написанное пользователем сообщение).
# Используйте метод update_data.
# 3. Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
# 4. После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
# Функцию set_weight(message, state):
# 1. Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
# 2. Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение).
# Используйте метод update_data.
# 3. Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
# 4. После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
# Функцию send_calories(message, state):
# 1. Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
# 2. Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение).
# Используйте метод update_data.
# 3. Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
# 4. Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий
# (для женщин или мужчин - на ваше усмотрение). Данные для формулы берите из ранее объявленной
# переменной data по ключам age, growth и weight соответственно.
# 5. Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
# 6. Финишируйте машину состояний методом finish().
# !В течение написания этих функций помните, что они асинхронны
# и все функции и методы должны запускаться с оператором await.
#
# При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import asyncio

api = "7750189712:AAGBJgxYN-8ofmWh39xTbtheJPsTemgNzu8"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    # Объекты класса State
    age = State()
    growth = State()
    weight = State()

# этот handler перехватывает команду start
@dp.message_handler(commands = ['start']) # с параметром commands реагирует на команды
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью")

# этот handler перехватывает сообщения с текстом Calories
@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text) # запись возраста
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text) # запись роста
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text) # запись веса

    data = await state.get_data() # словарь данных машины состояний
    man_cl = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    woman_cl = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    await message.answer(f"Ваша норма калорий, если вы мужчина - {man_cl}, если вы женщина - {woman_cl}")
    await state.finish() # обязательно закрыть состояние

# В конце кода, чтобы сначала специфические какие-либо handler отработали, а потом этот
@dp.message_handler()   # без параметра реагирует на все
async def all_message(message):
    await message.answer('Для начала работы введите команду /start')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
