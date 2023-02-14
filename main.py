import requests
import telebot
from dotenv import load_dotenv
import os
from telebot import types
from get_material import *
from materials import *

load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN_API'))


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    This function serves as the starting point for the bot's interaction with the user. It displays a set of options for the user to choose from.

    Parameters:
    message (telebot.types.Message): A Message object that represents the incoming message from the user.
    """
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton('Добавить материал'))
    markup.row(telebot.types.KeyboardButton('Списать материал'))
    markup.row(telebot.types.KeyboardButton('Просмотр количества материала'))
    markup.row(telebot.types.KeyboardButton('Создать новый матерал'))
    bot.send_message(message.chat.id, "Добро пожаловать в начальное меню", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def handle_menu_button(message):
    """
    This function is used to return back to the main menu when the "Назад в меню" button is pressed.
The main menu is displayed by calling the start_message function.
    """
    start_message(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Добавить материал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Добавить профиль')
        button_2 = telebot.types.KeyboardButton('Добавить светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Добавить драйвера')
        button_4 = telebot.types.KeyboardButton('Добавить крышки')
        button_5 = telebot.types.KeyboardButton('Добавить систему крепления')
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(message.chat.id,
                         "Выберите одну из опций",
                         reply_markup=markup)
    elif message.text in list(ADD_MATERIALS.keys()):
        chapter = ADD_MATERIALS[message.text]
        response = requests.get(f'http://127.0.0.1:9000/api/{ADD_MATERIALS[message.text]}/')
        data = response.json()
        bot.send_message(message.chat.id, "Пожалуйста, введите "
                                        "наименование и количество, которое хотите добавить")
        bot.send_message(message.chat.id, get_all_materials(data, ADD_MATERIALS[message.text]))
        bot.register_next_step_handler(message, add_material_get_name_material, chapter, bot)


    if message.text == 'Списать материал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Списать профиль')
        button_2 = telebot.types.KeyboardButton('Списать светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Списать драйвера')
        button_4 = telebot.types.KeyboardButton('Списать крышки')
        button_5 = telebot.types.KeyboardButton('Списать систему крепления')
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(message.chat.id,
                         "Выберите категорию",
                         reply_markup=markup)
    elif message.text in list(DEL_MATERIALS.keys()):
        chapter = DEL_MATERIALS[message.text]
        response = requests.get(f'http://127.0.0.1:9000/api/{DEL_MATERIALS[message.text]}/')
        data = response.json()
        bot.send_message(message.chat.id, "Пожалуйста, введите наименование и количество, которое хотите"
                                          " списать")
        bot.send_message(message.chat.id, get_all_materials(data, DEL_MATERIALS[message.text]))
        bot.register_next_step_handler(message, del_material_get_name_material, chapter, bot)




    if message.text == 'Просмотр количества материала':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Профиль')
        button_2 = telebot.types.KeyboardButton('Светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Драйвера')
        button_4 = telebot.types.KeyboardButton('Крышки')
        button_5 = telebot.types.KeyboardButton('Система крепления')
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(message.chat.id,
                'Menu: \n1. Профиль \n2. Светодиодные модули 2 \n3. Драйвера \n4. Крышки \n5. Система крепления',
                reply_markup=markup)
    elif message.text in list(MATERIALS.keys()):
        response = requests.get(f'http://127.0.0.1:9000/api/{MATERIALS[message.text]}/')
        data = response.json()
        bot.send_message(message.chat.id, get_all_materials(data, MATERIALS[message.text]))




    if message.text == 'Создать новый матерал':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        button_1 = telebot.types.KeyboardButton('Категория профиль')
        button_2 = telebot.types.KeyboardButton('Категория светодиодные модули')
        button_3 = telebot.types.KeyboardButton('Категория драйвера')
        button_4 = telebot.types.KeyboardButton('Категория крышки')
        button_5 = telebot.types.KeyboardButton('Категория система крепления')
        button_6 = types.KeyboardButton('Назад в меню')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
        bot.send_message(message.chat.id,
                         "Выбирайте категорию",
                         reply_markup=markup)
    elif message.text in list(CREATE_MATERIALS.keys()):
        chapter = CREATE_MATERIALS[message.text]
        bot.send_message(message.chat.id, "Пожалуйста, введите "
                                        "наименование материала, которое хотите создать")
        bot.register_next_step_handler(message, create_material_get_name_material, chapter, bot)

if __name__ == "__main__":
    bot.polling()
