from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from sql_bd import *

inlreg = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Регистрация", callback_data="registration"))

inlfunctions = [InlineKeyboardButton(text="Пополнить", callback_data="top_up"),
                InlineKeyboardButton(text="Баланс", callback_data="balance"),
                InlineKeyboardButton(text="Категории компьютеров", callback_data="computer_categories"),
                InlineKeyboardButton(text="Все игры", callback_data="all_games"),
                InlineKeyboardButton(text="Сеанс", callback_data="session"),
                InlineKeyboardButton(text="Все сеансы", callback_data="all_sessions")]
greet_inlfunctions = InlineKeyboardMarkup(row_width=2).add(*inlfunctions)

btnAdmin = KeyboardButton("Функции администратора")
greet_btnAdmin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnAdmin)

inladmin = [InlineKeyboardButton(text="Изменить цену категории", callback_data="Admin_Price"),
            InlineKeyboardButton(text="Новая категория", callback_data="Admin_Category"),
            InlineKeyboardButton(text="Новый компьютер", callback_data="Admin_Computer"),
            InlineKeyboardButton(text="Все компьютеры", callback_data="Admin_ViewComputer"),
            InlineKeyboardButton(text="Новая игра", callback_data="Admin_Game"),
            InlineKeyboardButton(text="Все игры (подробно)", callback_data="Admin_GameDetail")]
greet_inladmin = InlineKeyboardMarkup(row_width=2).add(*inladmin)

#Инлайн кнопки для вывода из бд категорий компьютеров
def AddingACategory():
    cursor.execute("SELECT Категория FROM КатегорияКомпьютера")
    results = cursor.fetchall()
    inlcategories=[]
    for row in results:
        inlcategories.append(InlineKeyboardButton(text=str(row[0]), callback_data=f'Category_{row[0]}'))
    greet_inlcategories=InlineKeyboardMarkup(row_width=3).add(*inlcategories)
    return greet_inlcategories

#Инлайн кнопка оставить поле не заполненным (NULL)
greet_inladminempty = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Не заполнять", callback_data="Admin_Empty"))
