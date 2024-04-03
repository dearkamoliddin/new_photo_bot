from aiogram.dispatcher.filters.state import StatesGroup

from loader import dp, db
from aiogram import types
from states.user import RegisterState
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'])
async def user_start(message: types.Message):
    if db.get_user_by_chat_id(chat_id=message.chat.id):
        text = "Assalomu aleykum, xush kelibsiz!"
        await message.answer(text=text)
    else:
        text = "Assalomu aleykum, ismingizni kiriting"
        await message.answer(text=text)
    await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text, chat_id=message.chat.id)
    text = "Telifon raqam"
    await message.answer(text=text)
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    text = "Manzil"
    await message.answer(text=text)
    await RegisterState.location.set()


@dp.message_handler(state=RegisterState.location)
async def get_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)

    data = await state.get_data()
    if db.add_user(data):
        text = "Successfully registered ✅"
    else:
        text = "Bot has some problems"
    await message.answer(text=text)
    await state.finish()
