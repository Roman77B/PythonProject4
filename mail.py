from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "7750189712:AAGBJgxYN-8ofmWh39xTbtheJPsTemgNzu8"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup() # клавиатура
button = KeyboardButton(text = 'Информация') # кнопка
kb.add(button) # добавить кнопку
# kb.row kb.insert также методы для добавления кнопок
button2 = KeyboardButton(text = 'Начало') # кнопка
kb.add(button2)

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer("Привет!", reply_markup = kb) # здесь в ответ появится клавиатура kb

# для кнопки 'Информация' точно такой же обработчик с текстом получается нужен
@dp.message_handler(text = ['Информация'])
async def inform(message):
    await message.answer('Информация о боте')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)