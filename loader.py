from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main.config import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
db = Dispatcher(bot, storage=storage)



