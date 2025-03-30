# Здесь хранятся все обработчики
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery # Импортируем для обработки сообщений
from aiogram.filters import CommandStart, Command # Импортируем фильтры
from aiogram.fsm.state import State, StatesGroup # Импортируем все для регистрации и состояний
from aiogram.fsm.context import FSMContext # Импортируем все для регистрации и состояний

import app.keyboards as kb

router = Router()

class Register(StatesGroup): # Делаем регистрацию
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup=kb.main) # Выодит сообщение
    await message.reply('Как дела?') # Отвечает на твое сообщение

@router.message(Command('help')) # Команда help
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')

@router.message(F.text == 'Каталог') # Если пользователь напишет конкретное сообщение
async def catalog(message: Message):
    await message.answer('Выбериет категорию товара', reply_markup=kb.catalog)

@router.callback_query(F.data == 't-shirt')
async def t_shirt(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True) # Отправляем уведомление, show_alert - чтобы появилось уведмоление с кнопкой окей
    await callback.message.answer('Вы выбрали категорию футболок') # Отправляем сообщение

@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введиет ваше имя')
# Регистрируем команду, даем первое состояние на имя и ждем ответа

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')
# Берет написанное пользователем имя и сохраняем в name=message.text, даем новое состояние на возраст и запрашиваем возраст

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('Введите ваш номер', reply_markup=kb.getnumber)

@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nВаш номер: {data["number"]}')
    await state.clear()

# reply_markup - прицепить клавиатуру