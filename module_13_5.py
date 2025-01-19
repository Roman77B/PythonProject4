# Цель: научится создавать клавиатуры и кнопки на них в Telegram-bot.
# Задача "Меньше текста, больше кликов":
# Необходимо дополнить код предыдущей задачи, чтобы вопросы о параметрах тела
# для расчёта калорий выдавались по нажатию кнопки.
# Измените massage_handler для функции set_age.
# Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а не на 'Calories'.
# Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней
# со следующим текстом: 'Рассчитать' и 'Информация'.
# Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства
# при помощи параметра resize_keyboard.
# Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup.
# В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками.
# При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция set_age,
# с которой начинается работа машины состояний для age, growth и weight.
# Пример результата выполнения программы:
# Клавиатура по команде /start:++
# После нажатия на кнопку 'Рассчитать':
# Примечания:
# При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!
# Успехов!

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "7750189712:AAGBJgxYN-8ofmWh39xTbtheJPsTemgNzu8"
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
                         reply_markup=kb)  # здесь в ответ появится клавиатура kb

# этот handler перехватывает сообщения с текстом Calories
@dp.message_handler(text = 'Рассчитать')
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
