from aiogram import Dispatcher, types 
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from sql_bd import *
import buttons

#Команды /start и /help
async def command_start(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        if message.from_user.username:
            with open("admins.txt") as file:
                content = file.read()
            if str(message.from_user.id) in content:
                await bot.send_message(message.from_user.id, 'Привет, '+message.from_user.username+'!', reply_markup=buttons.greet_btnAdmin)
            else:
                await bot.send_message(message.from_user.id, 'Привет, '+message.from_user.username+'!')
            llist=[]
            llist.append(message.from_user.username)
            info = cursor.execute('SELECT * FROM Клиент WHERE Никнейм=?', llist)
            if info.fetchone() is None:
                await bot.send_message(message.from_user.id, 'Пожалуйста, зарегистрируйтесь для продолжения работы', reply_markup=buttons.inlreg)
            else:
                await bot.send_message(message.from_user.id, 'Вот ваши возможности:', reply_markup=buttons.greet_inlfunctions)
        else:
            await bot.send_message(message.from_user.id, 'У вас нет никнейма')
    except:
        await message.reply('Ой! Что-то пошло не так')

#Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        pass
    else:
        await state.finish()
        await message.reply('Действие отменено')

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'], state="*")
    dp.register_message_handler(cancel_handler, commands='cancel', state="*")
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")