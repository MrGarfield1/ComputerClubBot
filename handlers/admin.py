from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from sql_bd import *
import buttons


# ==========================================================================
# Стать админом
async def admin_becomeadmin(message: types.Message):
    with open("admins.txt") as file:
        content = file.read()
    if str(message.from_user.id) in content:
        await message.reply('Вы уже являетесь администратором')
    else:
        with open("admins.txt", 'a') as file:
            file.write(str(message.from_user.id))
            file.write(" ")
        await message.reply('Теперь вы администратор', reply_markup=buttons.greet_btnAdmin)


# ==========================================================================
# Кнопка для показа инлайн-кнопок с функциями админа
async def admin_start(message: types.Message):
    with open("admins.txt") as file:
        content = file.read()
    if str(message.from_user.id) in content:
        await bot.send_message(message.from_user.id, 'Функции администратора:', reply_markup=buttons.greet_inladmin)
    else:
        await message.reply('Эта функция только для администраторов')


# ==========================================================================
# Изменение цены категории компьютеров
class ChangePrice(StatesGroup):
    category = State()
    price = State()


# Инлайн-кнопка(колбэк-кнопка)
async def changeprice_start_inline(call: types.CallbackQuery):
    await ChangePrice.category.set()
    await call.message.reply('Введите категорию компьютера')


async def changeprice_category(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    info = cursor.execute('SELECT * FROM КатегорияКомпьютера WHERE Категория=?', tuple(data.values()))
    if info.fetchone() is None:
        await message.reply('Такой категории нет')
        await state.finish()
    else:
        await ChangePrice.next()
        await message.reply('Введите новую цену')


async def changeprice_price(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = message.text

        cursor.execute("EXEC Изменение_стоимости_тарифа ?, ?", tuple(data.values()))
        connection.commit()

        await state.finish()

        await message.reply('Цена успешно изменена')
    except:
        await message.reply("Ой! Что-то пошло не так")
        await state.finish()


# ==========================================================================
# Добавление новой категории компьютеров
class AddCategory(StatesGroup):
    category = State()
    price = State()


# Инлайн-кнопка(колбэк-кнопка)
async def addcategory_start_inline(call: types.CallbackQuery):
    await AddCategory.category.set()
    await call.message.reply('Введите название категории компьютеров')


async def addcategory_category(message: types.Message, state=FSMContext):
    if '_' in message.text:
        await message.reply('В категории не должно быть символа "_"')
        await state.finish()
    else:
        async with state.proxy() as data:
            data['category'] = message.text
        info = cursor.execute('SELECT * FROM КатегорияКомпьютера WHERE Категория=?', tuple(data.values()))
        if info.fetchone() is None:
            await AddCategory.next()
            await message.reply('Введите стоимость часа игры')
        else:
            await message.reply('Такая категория есть')
            await state.finish()


async def addcategory_price(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = message.text

        cursor.execute("INSERT INTO [КатегорияКомпьютера] VALUES (?, ?)", tuple(data.values()))
        connection.commit()

        await state.finish()

        await message.reply('Категория добавлена')
    except:
        await message.reply("Ой! Что-то пошло не так")
        await state.finish()


# ==========================================================================
# Добавление компьютера по введенной категории
class AddComputer(StatesGroup):
    category = State()


async def addcomputer_start_inline(call: types.CallbackQuery):
    await AddComputer.category.set()
    await call.message.answer('Выберите категорию компьютера', reply_markup=buttons.AddingACategory())


async def addcomputer_computer(call: types.CallbackQuery, state=FSMContext):
    try:
        cursor.execute("SELECT Категория FROM КатегорияКомпьютера")
        results = cursor.fetchall()

        action = call.data.split("_")[1]
        for row in results:
            if action == str(row[0]):
                async with state.proxy() as data:
                    data['category'] = str(row[0])

        cursor.execute("EXEC Добавление_компьютера ?", tuple(data.values()))
        connection.commit()

        await state.finish()
        await call.message.reply('Компьютер добавлен')
    except:
        await state.finish()
        await call.message.reply("Ой! Что-то пошло не так")


# ==========================================================================
# Вывод всех компьютеров
async def viewcomputer_start_inline(call: types.CallbackQuery):
    try:
        cursor.execute("SELECT * FROM ВсеКомпьютеры")
        results = cursor.fetchall()
        txt = ''
        for row in results:
            txt = txt + 'Инвентарный номер: ' + str(row[0]) + '\n' + 'Категория: ' + str(row[1]) + '\n\n'
        await call.message.answer(txt)

    except:
        await call.message.reply("Ой! Что-то пошло не так")


# ==========================================================================
# Операции с играми
async def gameoperations_start_inline(call: types.CallbackQuery):
    await call.message.answer('Операции с играми:', reply_markup=buttons.greet_inladmingame)


# ==========================================================================
# Добавление игры
class AddGame(StatesGroup):
    name = State()
    genre = State()
    developer = State()
    date = State()


# Инлайн-кнопка(колбэк-кнопка)
async def addgame_start_inline(call: types.CallbackQuery):
    await AddGame.name.set()
    await call.message.answer('Введите название игры')


async def addgame_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await AddGame.next()
    await message.reply('Введите жанр игры', reply_markup=buttons.greet_inladminempty)


# Инлайн кнопка оставить поле жанра пустым
async def addgame_emptygenre(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['genre'] = None
    await AddGame.next()
    await call.message.reply('Введите разрабочика игры', reply_markup=buttons.greet_inladminempty)


async def addgame_genre(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['genre'] = message.text
    await AddGame.next()
    await message.reply('Введите разрабочика игры', reply_markup=buttons.greet_inladminempty)


# Инлайн кнопка оставить поле разработчика пустым
async def addgame_emptydeveloper(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['developer'] = None
    await AddGame.next()
    await call.message.reply('Введите дату выхода игры\nВ формате день-месяц-год',
                             reply_markup=buttons.greet_inladminempty)


async def addgame_developer(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['developer'] = message.text
    await AddGame.next()
    await message.reply('Введите дату выхода игры\nВ формате день-месяц-год', reply_markup=buttons.greet_inladminempty)


# Инлайн кнопка оставить поле даты выхода игры пустым
async def addgame_emptydate(call: types.CallbackQuery, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['data'] = None
        cursor.execute("INSERT INTO [Игра] VALUES (?, ?, ?, ?)", tuple(data.values()))
        connection.commit()

        await state.finish()
        await call.message.reply('Игры добавлена')
    except:
        await state.finish()
        await call.message.reply("Ой! Что-то пошло не так")


async def addgame_date(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = message.text

        cursor.execute("INSERT INTO [Игра] VALUES (?, ?, ?, ?)", tuple(data.values()))
        connection.commit()

        await state.finish()
        await message.reply('Игра добавлена')
    except:
        await state.finish()
        await message.reply("Ой! Что-то пошло не так")


# ==========================================================================
# Добавление категории игре
class AddCategoryGame(StatesGroup):
    category = State()
    name = State()


# Инлайн-кнопка(колбэк-кнопка)
async def addcategorygame_start_inline(call: types.CallbackQuery):
    await AddCategoryGame.category.set()
    await call.message.answer('Выберите категорию компьютера', reply_markup=buttons.AddingACategory())


async def addcategorygame_category(call: types.CallbackQuery, state=FSMContext):
    try:
        cursor.execute("SELECT Категория FROM КатегорияКомпьютера")
        results = cursor.fetchall()

        action = call.data.split("_")[1]
        for row in results:
            if action == str(row[0]):
                async with state.proxy() as data:
                    data['category'] = str(row[0])

        await AddCategoryGame.next()
        await call.message.reply('Введите название игры')
    except:
        await state.finish()
        await call.message.reply("Ой! Что-то пошло не так")


async def addcategorygame_name(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text

        cursor.execute("EXEC Добавление_категории_игре ?, ?", tuple(data.values()))
        connection.commit()

        await state.finish()
        await message.reply('Категория игре добавлена')
    except:
        await state.finish()
        await message.reply("Ой! Что-то пошло не так")


# ==========================================================================
# Изменение игры
class ChangeGame(StatesGroup):
    name = State()
    cell = State()
    cellchange = State()


# Инлайн-кнопка(колбэк-кнопка)
async def changegame_start_inline(call: types.CallbackQuery):
    await ChangeGame.name.set()
    await call.message.answer('Введите название игры:')


async def changegame_ganre(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text

        cursor.execute("SELECT * FROM ВсеИгры WHERE НазваниеИгры=?", tuple(data.values()))
        results = cursor.fetchall()

        txt = ''
        for row in results:
            txt = txt + 'Название игры: ' + str(row[0]) + '\n'
            if str(row[1]) != 'NULL' and str(row[1]) != 'None':
                txt += 'Жанр игры: ' + str(row[1]) + '\n'
            else:
                txt += 'Жанр игры не указан' + '\n'
            if str(row[2]) != 'NULL' and str(row[2]) != 'None':
                txt += 'Разработчик игры: ' + str(row[2]) + '\n'
            else:
                txt += 'Разработчик игры не указан' + '\n'
            if str(row[3]) != 'NULL' and str(row[3]) != 'None':
                txt += 'Дата выхода игры: ' + str(row[3]) + '\n'
            else:
                txt += 'Дата выхода игры не указана' + '\n'
            txt += '\n'

        await ChangeGame.next()
        await message.answer(txt)
        await message.answer('Что вы хотите изменить:', reply_markup=buttons.greet_inladminchangegame)
    except:
        await state.finish()
        await message.reply("Ой! Что-то пошло не так")


async def changegame_cell(call: types.CallbackQuery, state=FSMContext):
    try:
        action = call.data
        if action == 'Admin_Game_Genre':
            async with state.proxy() as data:
                data['cell'] = 'Жанр'
            await call.message.reply('Введите жанр игры:')
        elif action == 'Admin_Game_Developer':
            async with state.proxy() as data:
                data['cell'] = 'Разработчик'
            await call.message.reply('Введите разработчика игры:')
        elif action == 'Admin_Game_Date':
            async with state.proxy() as data:
                data['cell'] = 'Дата выхода'
            await call.message.reply('Введите дату выхода игры:')

        await ChangeGame.next()
    except:
        await state.finish()
        await call.message.reply("Ой! Что-то пошло не так")


async def changegame_cellchange(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['cellchange'] = message.text

        cursor.execute("EXEC Изменение_игры ?, ?, ?", tuple(data.values()))
        connection.commit()

        await state.finish()
        await message.reply('Игра изменена')
    except:
        await state.finish()
        await message.reply("Ой! Что-то пошло не так")


# ==========================================================================
# Удаление игры
class DeleteGame(StatesGroup):
    name = State()


# Инлайн-кнопка(колбэк-кнопка)
async def deletegame_start_inline(call: types.CallbackQuery):
    await DeleteGame.name.set()
    await call.message.answer('Введите название игры:')


async def deletegame_name(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text

        info = cursor.execute('SELECT * FROM Игра WHERE НазваниеИгры=?', tuple(data.values()))
        if info.fetchone() is None:
            await state.finish()
            await message.answer('Такой игры нет')
        else:
            cursor.execute("EXEC Удаление_игр ?", tuple(data.values()))
            connection.commit()
            await state.finish()
            await message.answer('Игра удалена')
    except:
        await state.finish()
        await message.reply("Ой! Что-то пошло не так")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_becomeadmin, Text(equals="Стать админом"), state=None)
    dp.register_message_handler(admin_start, Text(equals="Функции администратора"), state=None)
    dp.register_callback_query_handler(changeprice_start_inline, text="Admin_Price")
    dp.register_message_handler(changeprice_category, content_types=['text'], state=ChangePrice.category)
    dp.register_message_handler(changeprice_price, state=ChangePrice.price)
    dp.register_callback_query_handler(addcategory_start_inline, text="Admin_Category")
    dp.register_message_handler(addcategory_category, content_types=['text'], state=AddCategory.category)
    dp.register_message_handler(addcategory_price, state=AddCategory.price)
    dp.register_callback_query_handler(addcomputer_start_inline, text="Admin_Computer", state=None)
    dp.register_callback_query_handler(addcomputer_computer, Text(startswith="Category_"), state=AddComputer.category)
    dp.register_callback_query_handler(viewcomputer_start_inline, text="Admin_ViewComputer")
    dp.register_callback_query_handler(gameoperations_start_inline, text="Admin_Game")
    dp.register_callback_query_handler(addgame_start_inline, text="Admin_NewGame")
    dp.register_message_handler(addgame_name, state=AddGame.name)
    dp.register_callback_query_handler(addgame_emptygenre, text="Admin_Empty", state=AddGame.genre)
    dp.register_message_handler(addgame_genre, state=AddGame.genre)
    dp.register_callback_query_handler(addgame_emptydeveloper, text="Admin_Empty", state=AddGame.developer)
    dp.register_message_handler(addgame_developer, state=AddGame.developer)
    dp.register_callback_query_handler(addgame_emptydate, text="Admin_Empty", state=AddGame.date)
    dp.register_message_handler(addgame_date, state=AddGame.date)
    dp.register_callback_query_handler(addcategorygame_start_inline, text="Admin_CategoryGame")
    dp.register_callback_query_handler(addcategorygame_category, Text(startswith="Category_"),
                                       state=AddCategoryGame.category)
    dp.register_message_handler(addcategorygame_name, state=AddCategoryGame.name)
    dp.register_callback_query_handler(changegame_start_inline, text="Admin_ChangeGame")
    dp.register_message_handler(changegame_ganre, content_types=['text'], state=ChangeGame.name)
    dp.register_callback_query_handler(changegame_cell, Text(startswith="Admin_Game_"), state=ChangeGame.cell)
    dp.register_message_handler(changegame_cellchange, state=ChangeGame.cellchange)
    dp.register_callback_query_handler(deletegame_start_inline, text="Admin_DeleteGame")
    dp.register_message_handler(deletegame_name, content_types=['text'], state=DeleteGame.name)
