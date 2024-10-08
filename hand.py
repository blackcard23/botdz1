from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import html
import requests

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Показать пользователей')]
    ], resize_keyboard=True)
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEoBpJmuP4XesCjSajNXKME7j-ytQPJlwACp0gAArnd4Eq_SzLemAhcvzUE')
    await message.answer(f'''
Ку, {html.bold(message.from_user.first_name)}
id: {message.from_user.id}
''', reply_markup=kb)


@router.message(F.text == 'Показать пользователей')
async def users_handler(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Лимит 5'), KeyboardButton(text='Лимит 10')],
        [KeyboardButton(text='Лимит 12')]
    ], resize_keyboard=True)

    await message.answer('Выберите лимит пользователей:', reply_markup=kb)


@router.message(F.text.startswith('Лимит '))
async def limit_handler(message: Message):
    limit_text = message.text.replace('Лимит ', '')

    try:
        limit = int(limit_text)
        data = requests.get(f'https://reqres.in/api/users?per_page={limit}').json()
        users = data.get('data', [])
        answer = ''

        for user in users:
            answer += f'{user.get("id")}. {user.get("first_name")} {user.get("last_name")}\n'

        await message.answer(answer)
    except ValueError:
        await message.answer('Неверный лимит')


@router.message(F.text)
async def user_id_handler(message: Message):
    user_id = int(message.text)
    data = requests.get(f'https://reqres.in/api/users/{user_id}').json()

    user = data.get('data', {})
    if user:
        answer = f'{user.get("id")}. {user.get("first_name")} {user.get("last_name")}\n'
        await message.answer(answer)
    else:
        await message.answer('Нет такого пользователя')

