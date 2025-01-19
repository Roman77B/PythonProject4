# Цель: научится создавать Inline клавиатуры и кнопки на них в Telegram-bot.
# Задача "Ещё больше выбора":
# Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать'
# присылалась Inline-клавиатруа.
# Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
# С текстом 'Рассчитать норму калорий' и callback_data='calories'
# С текстом 'Формулы расчёта' и callback_data='formulas'
# Создайте новую функцию main_menu(message), которая:
# Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
# Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'
# Создайте новую функцию get_formulas(call), которая:
# Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
# Будет присылать сообщение с формулой Миффлина-Сан Жеора.
# Измените функцию set_age и декоратор для неё:
# Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
# Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.
# По итогу получится следующий алгоритм:
# Вводится команда /start
# На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
# В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий' и 'Формулы расчёта'
# По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
# По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний по цепочке.
#
# Пример результата выполнения программы:
# При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "###"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    # Объекты класса State
    age = State()
    growth = State()
    weight = State()

# клавиатура с кнопками
kb = ReplyKeyboardMarkup(resize_keyboard = True)
btn1 = KeyboardButton(text = 'Рассчитать')
kb.add(btn1)
btn2 = KeyboardButton(text = 'Информация')
kb.add(btn2)

# этот handler перехватывает команду start
@dp.message_handler(commands = ['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью",
                         reply_markup = kb)  # здесь в ответ появится клавиатура kb

# inline клавиатура
kbinl = InlineKeyboardMarkup()
btn3 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
kbinl.add(btn3)
btn4 = InlineKeyboardButton(text = 'Формула расчета', callback_data = 'formulas')
kbinl.add(btn4)

# для обработки кнопки 'Формула расчета' инлайн клавиатуры
@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Формулы расчета:\n'
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161\n')
    await call.answer()

# этот handler перехватывает сообщения с текстом Рассчитать
@dp.message_handler(text = 'Рассчитать')
async def start(message):
    await message.answer("Рады вас видеть!", reply_markup = kbinl) # в ответ inline клавиатура kb

# для обработки кнопки 'Информация' инлайн клавиатуры
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

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
