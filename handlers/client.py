from aiogram import Dispatcher, types 
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from sql_bd import *
import buttons

#===========================================================
#Регистрация клиента
class Clients(StatesGroup):
    nickname = State()
    email = State()
    pasword = State()
    balance = State()

#Инлайн-кнопка(колбэк-кнопка)
async def clients_start_inline(call: types.CallbackQuery):
    llist=[]
    llist.append(call.from_user.username)
    info = cursor.execute('SELECT * FROM Клиент WHERE Никнейм=?', llist)
    if info.fetchone() is None: 
        await Clients.nickname.set()
        await call.message.answer('Введите почту')
    else:
        await call.message.answer("Вы уже зарегистрированы")
        await bot.send_message(call.from_user.id, 'Вот ваши возможности:', reply_markup=buttons.greet_inlfunctions)

async def clients_start(message: types.Message):
    llist=[]
    llist.append(message.from_user.username)
    info = cursor.execute('SELECT * FROM Клиент WHERE Никнейм=?', llist)
    if info.fetchone() is None:
        await Clients.nickname.set()
        await message.reply('Введите почту')
    else:
        await message.reply("Вы уже зарегистрированы")
        await bot.send_message(message.from_user.id, 'Вот ваши возможности:', reply_markup=buttons.greet_inlfunctions)

async def client_nickname(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.from_user.username
    await Clients.next()

    llist=[]
    llist.append(message.text)
    info = cursor.execute('SELECT * FROM Клиент WHERE Почта=?', llist)

    if info.fetchone() is None:  
        async with state.proxy() as data:
            data['email'] = message.text
        await Clients.next()

        await message.reply("Введите пароль(минимум 5 символов)")
    else:
        await state.finish()
        await message.reply("Такая почта уже есть")

async def client_pasword(message: types.Message, state=FSMContext):
    try:
        if len(str(message.text))>=5:
            async with state.proxy() as data:
                data['pasword'] = message.text
            await Clients.next()

            async with state.proxy() as data:
                data['balance'] = 0

            cursor.execute("INSERT INTO [Клиент] VALUES (?, ?, ?, ?)", tuple(data.values()))
            connection.commit()

            await state.finish()

            await message.reply('Регистрация прошла успешно')

            await bot.send_message(message.from_user.id, 'Вот ваши возможности:', reply_markup=buttons.greet_inlfunctions)
        else:
            await state.finish()
            await message.reply('Пароль меньше 5 символов')
    except:
        await message.reply("Ой! Что-то пошло не так")
        await state.finish()       

#===========================================================
#Пополнение кошелька
class Walet(StatesGroup):
    nickname = State()
    sum = State()    

#Инлайн-кнопка(колбэк-кнопка)
async def walet_start_inline(call: types.CallbackQuery):
    await Walet.nickname.set()
    await call.message.answer('Введите сумму пополнения')

async def walet_start(message: types.Message):
    await Walet.nickname.set()
    await message.reply('Введите сумму пополнения')

async def walet_sum(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['nickname'] = message.from_user.username
        await Walet.next()

        if int(message.text)>0:
            async with state.proxy() as data:
                data['sum'] = message.text

            cursor.execute("EXEC Пополнение_в_кошельке ?, ?", tuple(data.values()))
            connection.commit()

            await state.finish()    

            await message.reply('Успешно пополнено')
        else:
            await state.finish()
            await message.reply("Введите сумму пополнения больше 0")
    except:
        await message.reply("Ой! Что-то пошло не так")
        await state.finish()

#===========================================================
#Баланс кошелька
#Инлайн-кнопка(колбэк-кнопка)
async def balance_start_inline(call: types.CallbackQuery):
    try:
        llist=[]
        llist.append(call.from_user.username)

        cursor.execute("SELECT БалансКошелька FROM Клиент WHERE Никнейм=?", llist)
        results = cursor.fetchall()

        for row in results:
            balance= str(row[0])

        await call.message.answer('Баланс '+call.from_user.username+': '+balance+' руб.') 
    except:
        await call.message.answer("Ой! Что-то пошло не так") 

async def balance_start(message: types.Message):
    try:
        llist=[]
        llist.append(message.from_user.username)

        cursor.execute("SELECT БалансКошелька FROM Клиент WHERE Никнейм=?", llist)
        results = cursor.fetchall()

        for row in results:
            balance= str(row[0])

        await message.reply('Баланс '+message.from_user.username+': '+balance+' руб.') 
    except:
        await message.reply("Ой! Что-то пошло не так")

#===========================================================
#Вывод всех категорий компьютеров
#Инлайн-кнопка(колбэк-кнопка)
async def category_start_inline(call: types.CallbackQuery):
    try:
        cursor.execute("SELECT Категория, ЦенаЗаЧасИгры FROM КатегорияКомпьютера")
        results = cursor.fetchall()
        txt=''
        for row in results:
            txt=txt+'Категория: '+str(row[0])+'\nЦена: '+str(row[1])+' руб.'+'\n\n'
        await call.message.answer(txt)
    except:
        await call.message.answer("Ой! Что-то пошло не так")

async def category_start(message: types.Message):
    try:
        cursor.execute("SELECT Категория, ЦенаЗаЧасИгры FROM КатегорияКомпьютера")
        results = cursor.fetchall()

        txt=''
        for row in results:
            txt=txt+'Категория: '+str(row[0])+'\nЦена: '+str(row[1])+' руб.'+'\n\n'

        await message.reply(txt)
    except:
        await message.reply("Ой! Что-то пошло не так")

#===========================================================
#Покупка сеанса
class Session(StatesGroup):
    nickname = State()
    category = State()
    timen = State()
    timek = State()

#Инлайн-кнопка(колбэк-кнопка)
async def session_start_inline(call: types.CallbackQuery):
    await Session.nickname.set()
    await call.message.answer('Выберите категорию компьютера', reply_markup=buttons.AddingACategory())

async def session_start(message: types.Message):
    await Session.nickname.set()
    await message.reply('Выберите категорию компьютера', reply_markup=buttons.AddingACategory())

#Инлайн-кнопка(колбэк-кнопка)
async def session_category(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['nickname'] = call.from_user.username
    await Session.next()

    cursor.execute("SELECT Категория FROM КатегорияКомпьютера")
    results = cursor.fetchall()

    action = call.data.split("_")[1]
    for row in results:
        if action == str(row[0]):
            async with state.proxy() as data:
                data['category'] = str(row[0])
            await Session.next()
            await call.message.reply("Введите время начала\nВ формате день-месяц-год часы:минуты")          

async def session_timen(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['timen'] = message.text
    await Session.next()
    await message.reply("Введите время окончания\nВ формате день-месяц-год часы:минуты")

async def session_timek(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['timek'] = message.text

        cursor.execute("EXEC Заказ_сеанса ?, ?, ?, ?", tuple(data.values()))
        connection.commit()

        await state.finish()

        await message.reply('Сеанс куплен')
    except:
        await message.reply("Ой! Что-то пошло не так")
        await state.finish()       

#==========================================================================
#Вывод всех купленных сеансов пользователя
#Инлайн-кнопка(колбэк-кнопка)
async def sessionclient_start_inline(call: types.CallbackQuery):
    try:
        llist=[]
        llist.append(call.from_user.username)

        cursor.execute("EXEC Просмотр_сеансов_пользователя ?", llist)
        results = cursor.fetchall()

        txt=''
        for row in results:
            txt=txt+'Цена: '+str(row[0])+'\n'+'Номер компьютера: '+str(row[1])+'\n'+'Категория компьютера: '+str(row[2])+'\n''Время начала: '+str(row[3])+'\n'+'Время окончания: '+str(row[4])+'\n'+'Время покупки: '+str(row[5])+'\n\n\n'

        await call.message.answer(txt)
    except:
        await call.message.answer("Ой! Что-то пошло не так")

async def sessionclient_start(message: types.Message):
    try:
        llist=[]
        llist.append(message.from_user.username)

        cursor.execute("EXEC Просмотр_сеансов_пользователя ?", llist)
        results = cursor.fetchall()

        txt=''
        for row in results:
            txt=txt+'Цена: '+str(row[0])+'\n'+'Номер компьютера: '+str(row[1])+'\n'+'Категория компьютера: '+str(row[2])+'\n''Время начала: '+str(row[3])+'\n'+'Время окончания: '+str(row[4])+'\n'+'Время покупки: '+str(row[5])+'\n\n\n'

        await message.reply(txt) 
    except:
        await message.reply("Ой! Что-то пошло не так")

#==========================================================================
#Вывод всех игр, установленных на компьютерах
#Инлайн-кнопка(колбэк-кнопка)
async def allgames_start_inline(call: types.CallbackQuery):
    try:
        cursor.execute("SELECT * FROM КатегорияКомпьютера")
        results = cursor.fetchall()

        txt=''
        for i in results:
            txt+='Название категории: '+str(i[1])+"\n"+'Игры:\n'     
            llist=[]
            llist.append(str(i[1]))
            cursor.execute("SELECT * FROM ВсеИгры WHERE Категория=?", llist)
            results1 = cursor.fetchall()
            for j in results1: 
                txt+=str(j[0])+'\n' 
            txt+='\n'        
    
        await call.message.answer(txt)
    except:
        await call.message.answer("Ой! Что-то пошло не так")

async def allgames_start(message: types.Message):
    try:
        cursor.execute("SELECT * FROM КатегорияКомпьютера")
        results = cursor.fetchall()

        txt=''
        for i in results:
            txt+='Название категории: '+str(i[1])+"\n"+'Игры:\n'     
            llist=[]
            llist.append(str(i[1]))
            cursor.execute("SELECT * FROM ВсеИгры WHERE Категория=?", llist)
            results1 = cursor.fetchall()
            for j in results1: 
                txt+=str(j[0])+'\n' 
            txt+='\n'      
        await message.reply(txt)
    except:
        await message.reply("Ой! Что-то пошло не так")

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(clients_start_inline, text="registration")
    dp.register_message_handler(clients_start, commands='registration')
    dp.register_message_handler(client_nickname, content_types=['text'], state=Clients.nickname)
    dp.register_message_handler(client_pasword, state=Clients.pasword)
    dp.register_callback_query_handler(walet_start_inline, text="top_up")
    dp.register_message_handler(walet_start, commands='top_up')
    dp.register_message_handler(walet_sum, content_types=['text'], state=Walet.nickname)
    dp.register_callback_query_handler(balance_start_inline, text="balance")
    dp.register_message_handler(balance_start, commands='balance')
    dp.register_callback_query_handler(category_start_inline, text="computer_categories")
    dp.register_message_handler(category_start, commands='computer_categories')
    dp.register_callback_query_handler(session_start_inline, text="session")
    dp.register_message_handler(session_start, commands='session')
    dp.register_callback_query_handler(session_category, Text(startswith="Category_"), state=Session.nickname)
    dp.register_message_handler(session_timen, state=Session.timen)
    dp.register_message_handler(session_timek, state=Session.timek)
    dp.register_callback_query_handler(sessionclient_start_inline, text="all_sessions")
    dp.register_message_handler(sessionclient_start, commands='all_sessions')
    dp.register_callback_query_handler(allgames_start_inline, text="all_games")
    dp.register_message_handler(allgames_start, commands='all_games')
